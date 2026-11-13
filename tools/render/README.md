# Product renders

`bash tools/render_all.sh` writes every picture in `docs/images/renders/`. The pictures are renders of the
CAD model, not photos. Nothing has been milled, printed or assembled.

| File | What it shows |
| --- | --- |
| `hero.png` | CNC unit, three-quarter view on black |
| `top.png` | Plan view square to the deck |
| `side.png` | Left side, orthographic, standing on its feet: the wedge |
| `exploded.png` | Knobs, keycaps, lens, top shell, display, PCB with parts, battery, bottom shell, feet |
| `underside.png` | Bottom shell and feet |
| `closeup.png` | Knobs, display and buttons |
| `fdm.png` | FDM prototype in a light PETG colour |
| `status_screen.png` | The status screen drawn for the display, 3 x scale |
| `turntable.mp4`, `turntable.gif` | One turn, 72 frames at 24 frames per second |

## How it works

1. `export_meshes.py` runs in `cad/.venv`. It meshes the same solids that `cad/exports/assembly.step` holds
   (case parts and the reference shapes of bought parts), for the CNC and the FDM variant, and writes
   `manifest.json` with the standing pose, the display's active area and the lens mask window.
2. `pcb_step_to_stl.py` runs in the FreeCAD flatpak, only when the PCB build has written its finished board
   STEP (pcb/production/worxpad-pcb.step). That board replaces the reference board, and any part models in it
   replace the reference part shapes.
3. `status_screen.py` draws the 240 x 240 screen with Pillow. It reads the Edit layer from the default keymap and
   copies the layout and colours of `firmware/zmk/src/status_screen.c`. It is a drawing of what the firmware
   should show; the firmware has never run on a panel.
4. `scene.py` runs in the Blender flatpak with Cycles on the CPU: 64 samples per still at 1920 x 1280, 16 per
   turntable frame at 800 x 536, both denoised.
5. `ffmpeg` turns the frames into the MP4 and the GIF.

The last full run took 907 s (about 15 minutes) on 16 CPU threads that other jobs were also using
(load average about 37).

Scratch files go to `tools/render/.build/`, which git ignores.

## Limits

- Materials are proposals for the look: bead-blasted black anodised aluminium, black PBT keycaps, clear PMMA
  lens with a painted border, light PETG for the print. No finish or colour has been ordered.
- Bought parts are block shapes drawn from data sheet sizes, not vendor models.
- The PCB is a plain green slab until the PCB build writes a finished board STEP.
- LVGL's Bluetooth symbol is written as "BT" on the drawn screen. The status bar shows a sample state:
  profile 1 connected, 84 %.
