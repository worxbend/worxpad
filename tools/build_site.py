#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Builds the microsite in _site/ and checks it.

    build_site.py               build once; exit 1 when any check fails
    build_site.py --serve 8000  build, serve _site on 127.0.0.1:8000, rebuild when a source changes

What goes into _site/:
- the .html, .css, .js and .svg files of site/ (site/README.md stays behind);
- every file a page names as images/<group>/<file>, copied from docs/images/<group>/<file> at build
  time, so a new render needs no change here;
- resized WebP copies of the PNG renders when Pillow is installed. Without Pillow the
  <source type="image/webp"> lines are dropped and the page falls back to the PNGs.

The build fails when a page names a file that does not exist, when a picture in docs/images/renders,
cad or pcb is neither shown nor listed in SKIP, when a local link or #anchor does not resolve, when a
link into github.com/worxbend/worxpad names a path or heading that is not in this checkout, when an
image lacks its size or alt text or its size differs from the picture's, when the page loads a script
or stylesheet from another site (Google Fonts excepted), or when headings skip a level.
The site is built in a staging folder and moved into place only when every check passes.

Adapted from macropad/.github/scripts/build_site.py.
"""
import argparse
import re
import shutil
import struct
import sys
import threading
import time
from functools import partial
from html.parser import HTMLParser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from check_docs import heading_anchors

REPO_ROOT = Path(__file__).resolve().parents[1]
SITE = REPO_ROOT / "site"
IMAGES = REPO_ROOT / "docs" / "images"
OUTPUT = REPO_ROOT / "_site"
STAGING = REPO_ROOT / "_site.staging"
# --serve builds in a folder of its own, so a `make site` run at the same time cannot collide with it.
SERVE_STAGING = REPO_ROOT / "_site.staging-serve"
WEBP_CACHE = REPO_ROOT / ".build" / "site-webp"

PUBLISHED_SUFFIXES = {".html", ".css", ".js", ".svg"}
# Pictures that may stay off the page, each with a one-line reason, keyed as "group/file".
# Every other picture in these folders (at any depth, any letter case) must be shown.
SKIP: dict[str, str] = {
    "renders/turntable.gif": "the page plays turntable.mp4 instead: the same 72 frames in a sixth of the bytes",
}
CHECKED_GROUPS = ("renders", "cad", "pcb")
PICTURE_SUFFIXES = {".png", ".gif", ".jpg", ".jpeg", ".webp", ".svg"}

WEBP_QUALITY = 82
# One authored pattern: a <source> for WebP copies on a line of its own. Without Pillow it is removed.
WEBP_SOURCE_LINE = re.compile(r'^[ \t]*<source type="image/webp"[^>]*>[ \t]*\n', re.MULTILINE)
LINK_ATTRIBUTES = {"src", "href", "srcset", "poster"}
REPOSITORY = "https://github.com/worxbend/worxpad"
REPOSITORY_LINK = re.compile(re.escape(REPOSITORY) + r"(?:/(blob|tree)/main/([^#?]+?))?/?(?:#(.*))?$")
EXTERNAL = re.compile(r"^(?:[a-z][a-z0-9+.-]*:|//)", re.IGNORECASE)
# The one outside stylesheet the page may load. No outside script is allowed at all.
ALLOWED_STYLESHEET = "https://fonts.googleapis.com/css2?"
VOID_ELEMENTS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
# CSS pixels per unit of an SVG's root width and height, as a browser sizes the picture.
SVG_UNITS = {"": 1.0, "px": 1.0, "mm": 96 / 25.4, "cm": 96 / 2.54, "in": 96.0, "pt": 96 / 72}
SVG_LENGTH = re.compile(r"^\s*([\d.]+)\s*([a-z]*)\s*$")


# ---------------------------------------------------------------- reading pages

class PageScan(HTMLParser):
    """What the checks need from one page: references, ids, images and headings, in document order."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []  # href, src, srcset and poster values: must resolve
        self.shown: list[str] = []  # pictures the page displays: <img src>, its WebP <source>, <video> sources
        self.outside_resources: list[str] = []  # <script src> and stylesheets from another site
        self._webp_in_picture: list[str] = []
        self._in_video = False
        self.ids: list[str] = []
        self.images: list[tuple[int, dict[str, str], bool]] = []  # line, attributes, inside aria-hidden
        self.headings: list[tuple[int, int]] = []  # line, level
        self._hidden_stack: list[tuple[str, bool]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {name: value or "" for name, value in attrs}
        hidden = attributes.get("aria-hidden") == "true" or bool(self._hidden_stack and self._hidden_stack[-1][1])
        for name, value in attributes.items():
            if name in LINK_ATTRIBUTES:
                self.links += srcset_urls(value) if name == "srcset" else [value]
        if "id" in attributes:
            self.ids.append(attributes["id"])
        self._collect_shown(tag, attributes)
        self._collect_outside(tag, attributes)
        if tag == "img":
            self.images.append((self.getpos()[0], attributes, hidden))
        if re.fullmatch(r"h[1-6]", tag):
            self.headings.append((self.getpos()[0], int(tag[1])))
        if tag not in VOID_ELEMENTS:
            self._hidden_stack.append((tag, hidden))

    def _collect_shown(self, tag: str, attributes: dict[str, str]) -> None:
        if tag == "picture":
            self._webp_in_picture = []
        elif tag == "video":
            self._in_video = True
        elif tag == "source" and self._in_video:
            self.shown.append(attributes.get("src", ""))
        elif tag == "source" and attributes.get("type") == "image/webp":
            self._webp_in_picture += srcset_urls(attributes.get("srcset", ""))
        elif tag == "img":
            src = attributes.get("src", "")
            self.shown.append(src)
            self.shown += [w for w in self._webp_in_picture if (webp_source(w) or ("",))[0] == src]
            self._webp_in_picture = []

    def _collect_outside(self, tag: str, attributes: dict[str, str]) -> None:
        if tag == "script" and attributes.get("src") and EXTERNAL.match(attributes["src"]):
            self.outside_resources.append(attributes["src"])
        is_stylesheet = tag == "link" and "stylesheet" in attributes.get("rel", "").split()
        href = attributes.get("href", "")
        if is_stylesheet and EXTERNAL.match(href) and not href.startswith(ALLOWED_STYLESHEET):
            self.outside_resources.append(href)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag not in VOID_ELEMENTS:
            self._hidden_stack.pop()

    def handle_endtag(self, tag: str) -> None:
        if tag == "video":
            self._in_video = False
        for depth in range(len(self._hidden_stack) - 1, -1, -1):
            if self._hidden_stack[depth][0] == tag:
                del self._hidden_stack[depth:]
                return


def scan(html: str) -> PageScan:
    page = PageScan()
    page.feed(html)
    page.close()
    return page


def srcset_urls(srcset: str) -> list[str]:
    return [candidate.split()[0] for candidate in srcset.split(",") if candidate.strip()]


def image_references(page: PageScan) -> set[str]:
    """Every file the page names under images/, shown or only linked."""
    return {link for link in page.links if link.startswith("images/")}


def webp_source(reference: str) -> tuple[str, int] | None:
    """images/renders/top-960.webp -> (images/renders/top.png, 960). None for anything else."""
    if not reference.endswith(".webp"):
        return None
    stem, _, width = reference.removesuffix(".webp").rpartition("-")
    return (f"{stem}.png", int(width)) if width.isdigit() else None


def source_of(reference: str) -> str:
    """The docs/images file a reference comes from: the PNG for a WebP copy, else itself."""
    resized = webp_source(reference)
    return resized[0] if resized else reference


def header_size(header: bytes) -> tuple[int, int] | None:
    """Width and height from the first 24 bytes of a PNG (IHDR) or a GIF; None for anything else."""
    if header.startswith(b"\x89PNG") and len(header) >= 24:
        return struct.unpack(">II", header[16:24])
    if header.startswith(b"GIF") and len(header) >= 10:
        return struct.unpack("<HH", header[6:10])
    return None


def svg_length(text: str) -> int | None:
    match = SVG_LENGTH.match(text)
    if not match or match.group(2) not in SVG_UNITS:
        return None
    return round(float(match.group(1)) * SVG_UNITS[match.group(2)])


def svg_size(head: str) -> tuple[int, int] | None:
    """The size in CSS pixels a browser gives an SVG: its root width and height (KiCad writes mm)."""
    root = re.search(r"<svg\b[^>]*>", head)
    if not root:
        return None
    lengths = [re.search(rf'\s{name}="([^"]+)"', root.group(0)) for name in ("width", "height")]
    if not all(lengths):
        return None
    size = tuple(svg_length(match.group(1)) for match in lengths)
    return size if None not in size else None


def picture_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as file:
        head = file.read(4096)
    size = svg_size(head.decode("utf-8", "replace")) if path.suffix.lower() == ".svg" else header_size(head)
    if size is None:
        raise ValueError(f"{path.relative_to(REPO_ROOT)}: size not readable (PNG, GIF or SVG with width and height)")
    return size


# ---------------------------------------------------------------- picture checks

def missing_pictures(references: set[str]) -> list[str]:
    problems = []
    for reference in sorted(references):
        path = IMAGES / source_of(reference).removeprefix("images/")
        if not path.is_file():
            problems.append(f"{reference} does not exist under docs/images")
            continue
        resized = webp_source(reference)
        if resized and resized[1] > picture_size(path)[0]:
            problems.append(f"{reference} is wider than {source_of(reference)}; never upscale")
    return problems


def all_pictures() -> set[str]:
    return {path.relative_to(IMAGES).as_posix()
            for group in CHECKED_GROUPS for path in (IMAGES / group).rglob("*")
            if path.is_file() and path.suffix.lower() in PICTURE_SUFFIXES}


def unshown_pictures(displayed: set[str]) -> list[str]:
    """displayed: what a page shows (PageScan.shown). A link to a picture does not show it."""
    shown = {source_of(reference).removeprefix("images/") for reference in displayed}
    pictures = all_pictures()
    problems = [f"docs/images/{name} is not shown on the page (a link does not count); show it or add it to SKIP with a reason"
                for name in sorted(pictures - shown - SKIP.keys())]
    for name, reason in SKIP.items():
        if name not in pictures:
            problems.append(f"SKIP names {name}, which is not under docs/images")
        if name in shown:
            problems.append(f"SKIP names {name}, but the page shows it; remove it from SKIP")
        if not reason.strip() or "\n" in reason:
            problems.append(f"SKIP reason for {name} must be one non-empty line")
    return problems


# ---------------------------------------------------------------- page checks on the built site

def repository_link_problem(url: str) -> str | None:
    match = REPOSITORY_LINK.match(url)
    if not match:
        return None if not url.startswith(REPOSITORY) else f"{url}: not a main-branch blob or tree link"
    kind, path, anchor = match.groups()
    target = REPO_ROOT / path if kind else REPO_ROOT / "README.md"
    if kind and not (target.is_dir() if kind == "tree" else target.is_file()):
        return f"{url}: {path} does not exist in this checkout"
    if anchor and target.suffix == ".md" and anchor not in heading_anchors(target):
        return f"{url}: {target.relative_to(REPO_ROOT)} has no heading for #{anchor}"
    return None


def link_problems(root: Path, page_path: Path, page: PageScan, ids: set[str]) -> list[str]:
    problems = []
    for reference in page.links:
        if not reference or reference.startswith(("mailto:", "data:")):
            continue
        if EXTERNAL.match(reference):
            problem = repository_link_problem(reference)
            problems += [problem] if problem else []
            continue
        path_part, _, anchor = reference.partition("#")
        target = (page_path.parent / path_part).resolve() if path_part else page_path
        if not target.is_file() or root.resolve() not in target.parents:
            problems.append(f"{reference} does not resolve to a file in the site")
        elif anchor and (target != page_path or anchor not in ids):
            problems.append(f"{reference}: no element with id {anchor!r}")
    return problems


def size_problem(root: Path, attributes: dict[str, str]) -> str | None:
    """The width and height attributes must be the picture's own, or the page reserves the wrong box."""
    src = attributes.get("src", "")
    path = root / src
    if not src.startswith("images/") or not path.is_file():
        return None
    size = picture_size(path)
    stated = (attributes.get("width"), attributes.get("height"))
    if stated != (str(size[0]), str(size[1])):
        return f"width/height {stated[0]} x {stated[1]}, but {src} is {size[0]} x {size[1]}"
    return None


def image_problems(page: PageScan, root: Path | None = None) -> list[str]:
    problems = []
    for index, (line, attributes, hidden) in enumerate(page.images):
        where = f"line {line} <img src={attributes.get('src', '?')!r}>"
        problems += [f"{where} has no {needed}" for needed in ("width", "height", "alt") if needed not in attributes]
        mismatch = size_problem(root, attributes) if root else None
        if mismatch:
            problems.append(f"{where}: {mismatch}")
        if attributes.get("alt") == "" and not hidden:
            problems.append(f"{where}: empty alt is allowed only inside aria-hidden=\"true\"")
        if index > 0 and attributes.get("loading") != "lazy":
            problems.append(f"{where}: every image after the first needs loading=\"lazy\"")
    return problems


def heading_problems(page: PageScan) -> list[str]:
    levels = [level for _, level in page.headings]
    problems = [] if levels.count(1) == 1 else [f"{levels.count(1)} h1 elements; a page has exactly one"]
    previous = 0
    for line, level in page.headings:
        if level > previous + 1:
            problems.append(f"line {line}: h{level} follows h{previous}")
        previous = level
    return problems


def duplicate_ids(page: PageScan) -> list[str]:
    seen, problems = set(), []
    for element_id in page.ids:
        if element_id in seen:
            problems.append(f"id {element_id!r} is used twice")
        seen.add(element_id)
    return problems


def check_built_pages(root: Path) -> list[str]:
    problems = []
    for path in sorted(root.glob("*.html")):
        page = scan(path.read_text(encoding="utf-8"))
        found = (link_problems(root, path.resolve(), page, set(page.ids)) + image_problems(page, root)
                 + heading_problems(page) + duplicate_ids(page)
                 + [f"loads {url} from another site; only Google Fonts is allowed" for url in page.outside_resources])
        problems += [f"{path.name}: {problem}" for problem in found]
    return problems


# ---------------------------------------------------------------- WebP copies

def load_pillow():
    try:
        from PIL import Image
    except ImportError:
        return None
    return Image


def write_webp(image_module, reference: str, target: Path) -> None:
    """Resized copy of a PNG, cached in .build/ so a rebuild only encodes what changed."""
    source_reference, width = webp_source(reference)
    source = IMAGES / source_reference.removeprefix("images/")
    cached = WEBP_CACHE / reference.removeprefix("images/")
    if not cached.is_file() or cached.stat().st_mtime < source.stat().st_mtime:
        cached.parent.mkdir(parents=True, exist_ok=True)
        with image_module.open(source) as image:
            if image.width != width:
                image = image.resize((width, round(image.height * width / image.width)), image_module.LANCZOS)
            image.save(cached, "WEBP", quality=WEBP_QUALITY, method=6)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(cached, target)


# ---------------------------------------------------------------- the build

def self_check() -> list[str]:
    """The patterns and readers must do what they are for, or a green build means nothing.
    Plain comparisons rather than assert, so `python -O` cannot switch them off."""
    picture = ('<picture>\n  <source type="image/webp" srcset="images/cad/a-700.webp 700w, images/cad/b-700.webp 700w">\n'
               '  <img src="images/cad/a.png" alt="">\n</picture>\n')
    sample = scan(picture + '<a href="images/pcb/x.svg">x</a><video><source src="images/renders/t.mp4"></video>'
                  '<script src="https://cdn.example/x.js"></script><link rel="stylesheet" href="https://x.org/a.css">'
                  '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo">')
    hidden = scan('<div aria-hidden="true"><img alt=""></div><img alt="">')
    checks = [
        (image_references(sample), {"images/cad/a.png", "images/cad/a-700.webp", "images/cad/b-700.webp",
                                    "images/pcb/x.svg", "images/renders/t.mp4"}),
        (sorted(sample.shown), ["images/cad/a-700.webp", "images/cad/a.png", "images/renders/t.mp4"]),
        (sample.outside_resources, ["https://cdn.example/x.js", "https://x.org/a.css"]),
        (webp_source("images/pcb/bare-top-784.webp"), ("images/pcb/bare-top.png", 784)),
        (webp_source("images/cad/a.png"), None),
        (WEBP_SOURCE_LINE.sub("", picture), '<picture>\n  <img src="images/cad/a.png" alt="">\n</picture>\n'),
        ([inside for _, _, inside in hidden.images], [True, False]),
        (heading_problems(scan("<h1>a</h1><h3>b</h3>")), ["line 1: h3 follows h1"]),
        (heading_problems(scan("<h2>a</h2>")), ["0 h1 elements; a page has exactly one", "line 1: h2 follows h0"]),
        (REPOSITORY_LINK.match(REPOSITORY + "/tree/main/pcb/fab").groups(), ("tree", "pcb/fab", None)),
        (repository_link_problem(REPOSITORY + "/blob/main/no-such-file.md"),
         f"{REPOSITORY}/blob/main/no-such-file.md: no-such-file.md does not exist in this checkout"),
        (header_size(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR" + struct.pack(">II", 3, 2)), (3, 2)),
        (header_size(b"GIF89a" + struct.pack("<HH", 5, 4)), (5, 4)),
        (svg_size('<?xml?>\n<svg\n  version="1.1"\n  width="120.6500mm" height="80.2894mm" viewBox="0 0 1 1">'), (456, 303)),
        (svg_size('<svg width="100%" height="10">'), None),
    ]
    return [f"self-check {index}: got {got!r}, expected {expected!r}"
            for index, (got, expected) in enumerate(checks) if got != expected]


def copy_site_files(destination: Path) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir()
    for path in SITE.rglob("*"):
        if path.is_file() and path.suffix in PUBLISHED_SUFFIXES:
            target = destination / path.relative_to(SITE)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
    (destination / ".nojekyll").touch()


def write_pages(destination: Path, sources: dict[Path, str], with_webp: bool) -> list[str]:
    """The pages, without WebP sources when there are no WebP copies."""
    problems = []
    for page, html in sources.items():
        if not with_webp:
            html = WEBP_SOURCE_LINE.sub("", html)
            if "image/webp" in html:
                problems.append(f"{page.name}: a WebP <source> is not on a line of its own")
        (destination / page.name).write_text(html, encoding="utf-8")
    return problems


def copy_pictures(destination: Path, references: set[str], image_module) -> None:
    for reference in sorted(references):
        target = destination / reference
        if webp_source(reference):
            if image_module is not None:
                write_webp(image_module, reference, target)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(IMAGES / reference.removeprefix("images/"), target)


def build(destination: Path) -> tuple[list[str], str]:
    """Builds into destination. Returns the problems found and a one-line summary."""
    broken = self_check()
    if broken:
        return broken, ""
    sources = {page: page.read_text(encoding="utf-8") for page in sorted(SITE.glob("*.html"))}
    scans = [scan(html) for html in sources.values()]
    references = set().union(*(image_references(page) for page in scans))
    displayed = set().union(*(set(page.shown) for page in scans))
    problems = missing_pictures(references) + unshown_pictures(displayed)
    if problems:
        return problems, ""

    copy_site_files(destination)
    image_module = load_pillow()
    if image_module is None:
        print("build_site: Pillow not installed, WebP copies skipped")
    problems += write_pages(destination, sources, with_webp=image_module is not None)
    copy_pictures(destination, references, image_module)
    problems += check_built_pages(destination)

    files = sum(1 for reference in references if not webp_source(reference))
    webp = sum(1 for reference in references if webp_source(reference)) if image_module else 0
    summary = f"build_site: {len(sources)} page, {files} pictures and files, {webp} WebP copies, {len(SKIP)} skipped"
    return problems, summary


def build_and_publish(staging: Path = STAGING) -> bool:
    """Builds into the staging folder and replaces _site only when every check passes."""
    try:
        problems, summary = build(staging)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    if problems:
        for problem in problems:
            print(f"build_site: {problem}")
        shutil.rmtree(staging, ignore_errors=True)
        return False
    retired = staging.with_name(staging.name + ".old")
    shutil.rmtree(retired, ignore_errors=True)
    if OUTPUT.exists():
        OUTPUT.rename(retired)
    staging.rename(OUTPUT)
    shutil.rmtree(retired, ignore_errors=True)
    print(f"{summary} -> {OUTPUT.relative_to(REPO_ROOT)}")
    return True


# ---------------------------------------------------------------- the local loop

def source_state() -> dict[Path, float]:
    """Everything a build reads. A change to this script itself needs a restart of the server."""
    # The Markdown files the page links to with #anchors; not the whole tree, which holds firmware/.build.
    markdown = [*REPO_ROOT.glob("*.md"), *REPO_ROOT.glob("*/README.md"), *(REPO_ROOT / "docs").glob("*.md")]
    watched = [*SITE.rglob("*"), *IMAGES.rglob("*"), *markdown]
    return {path: path.stat().st_mtime for path in watched if path.is_file()}


def watch_and_rebuild() -> None:
    state = source_state()
    while True:
        time.sleep(1)
        current = source_state()
        if current != state:
            state = current
            print("build_site: change seen, rebuilding")
            try:
                if not build_and_publish(SERVE_STAGING):
                    print("build_site: still serving the last good build")
            except Exception as error:  # a broken edit must not stop the server
                print(f"build_site: rebuild failed: {error!r}; still serving the last good build")


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args) -> None:
        if not str(args[1] if len(args) > 1 else "").startswith(("2", "3")):
            super().log_message(format, *args)

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


def serve(port: int) -> int:
    sys.stdout.reconfigure(line_buffering=True)  # rebuild messages appear at once, even when piped
    if not build_and_publish(SERVE_STAGING) and not OUTPUT.is_dir():
        return 1
    threading.Thread(target=watch_and_rebuild, daemon=True).start()
    handler = partial(QuietHandler, directory=str(OUTPUT))
    with ThreadingHTTPServer(("127.0.0.1", port), handler) as server:
        print(f"build_site: serving http://127.0.0.1:{port}/ and rebuilding on change. Ctrl+C stops.")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--serve", type=int, metavar="PORT", help="serve _site on 127.0.0.1 and rebuild on change")
    arguments = parser.parse_args()
    if arguments.serve:
        return serve(arguments.serve)
    return 0 if build_and_publish() else 1


if __name__ == "__main__":
    sys.exit(main())
