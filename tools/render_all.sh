#!/usr/bin/env bash
# Product renders of worxpad into docs/images/renders/. Run from anywhere: bash tools/render_all.sh
#
# Steps:
#   1. tools/render/export_meshes.py (case venv) meshes every case part and reference shape, CNC and FDM.
#   2. When pcb/production/worxpad-pcb.step exists, tools/render/pcb_step_to_stl.py (FreeCAD flatpak) meshes it
#      and the renders use that board instead of the reference slab.
#   3. tools/render/status_screen.py (case venv) draws the status screen from the default keymap.
#   4. tools/render/scene.py (Blender flatpak, Cycles on the CPU) renders the stills and the turntable frames.
#   5. ffmpeg turns the frames into turntable.mp4 and turntable.gif.
# Needs: cad/.venv (uv, build123d 0.13.0), flatpak org.blender.Blender 5.2 and org.freecad.FreeCAD 1.1,
# ffmpeg, ImageMagick. Scratch goes to tools/render/.build/ (inside the repository, because the flatpak
# sandboxes cannot see /tmp). Exit status: 0 when every picture was written, non-zero on the first failure.
set -Eeuo pipefail
trap 'printf "render_all.sh: failed at line %s\n" "$LINENO" >&2' ERR

readonly REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
readonly BUILD="$REPO/tools/render/.build"
readonly OUT="$REPO/docs/images/renders"
readonly PCB_STEP="$REPO/pcb/production/worxpad-pcb.step"
readonly CAD_PYTHON="$REPO/cad/.venv/bin/python"
readonly STILLS=(hero top side exploded underside closeup fdm)
readonly BLENDER=(flatpak run org.blender.Blender -b --factory-startup --python-exit-code 1
  --python "$REPO/tools/render/scene.py" --)
readonly FREECAD=(flatpak run --command=freecadcmd org.freecad.FreeCAD)
readonly GIF_WIDTH=480

require() {
  local tool
  for tool in "$@"; do
    command -v "$tool" >/dev/null || { printf 'render_all.sh: %s not found\n' "$tool" >&2; exit 1; }
  done
  [[ -x "$CAD_PYTHON" ]] || { printf 'render_all.sh: %s missing; make cad/.venv with uv first\n' "$CAD_PYTHON" >&2; exit 1; }
}

pcb_meshes() {
  local target="$BUILD/meshes/pcb_step"
  rm -rf -- "$target"
  if [[ ! -f "$PCB_STEP" ]]; then
    printf 'no %s; the renders use the reference board from the case package\n' "${PCB_STEP#"$REPO"/}"
    return
  fi
  "${FREECAD[@]}" "$REPO/tools/render/pcb_step_to_stl.py" --pass "$PCB_STEP" "$BUILD/meshes/manifest.json" "$target"
  # freecadcmd exits 0 even when the script raises, so check for its output
  [[ -f "$target/board.stl" ]] || { printf 'render_all.sh: PCB STEP conversion wrote no board.stl\n' >&2; exit 1; }
}

turntable_movies() {
  local frames="$BUILD/turntable"
  ffmpeg -loglevel error -y -framerate 24 -i "$frames/frame_%04d.png" -c:v libx264 -pix_fmt yuv420p -crf 20 \
    -movflags +faststart "$OUT/turntable.mp4"
  ffmpeg -loglevel error -y -framerate 24 -i "$frames/frame_%04d.png" \
    -vf "fps=12,scale=$GIF_WIDTH:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=128[p];[b][p]paletteuse=dither=bayer" \
    "$OUT/turntable.gif"
}

check_outputs() {
  local name missing=0
  for name in "${STILLS[@]/%/.png}" status_screen.png turntable.mp4 turntable.gif; do
    [[ -s "$OUT/$name" ]] || { printf 'render_all.sh: %s was not written\n' "$name" >&2; missing=1; }
  done
  local frames=("$BUILD"/turntable/frame_*.png)
  [[ ${#frames[@]} -eq 72 ]] || { printf 'render_all.sh: %d turntable frames, expected 72\n' "${#frames[@]}" >&2; missing=1; }
  return "$missing"
}

main() {
  require flatpak ffmpeg magick
  mkdir -p -- "$BUILD" "$OUT"
  local started=$SECONDS

  "$CAD_PYTHON" "$REPO/tools/render/export_meshes.py" "$BUILD/meshes" | tail -n 1
  pcb_meshes
  "$CAD_PYTHON" "$REPO/tools/render/status_screen.py" "$BUILD/status_screen.png"
  magick "$BUILD/status_screen.png" -filter point -resize 300% "$OUT/status_screen.png"

  "${BLENDER[@]}" "$BUILD/meshes" "$BUILD/status_screen.png" "$OUT" "${STILLS[@]}" | grep '^rendered'
  rm -rf -- "$BUILD/turntable"
  "${BLENDER[@]}" "$BUILD/meshes" "$BUILD/status_screen.png" "$BUILD" turntable | grep '^rendered'
  turntable_movies
  check_outputs

  printf 'wrote %s in %d s\n' "${OUT#"$REPO"/}" "$((SECONDS - started))"
}

main "$@"
