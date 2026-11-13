# Case order package (case revision A)

Everything needed to order the worxpad case parts that are machined. The STEP files, drawings and
`jlccnc/hole_table.csv` are copied and merged by `tools/order_package.py` (`make order`) from `cad/exports/`;
this page, the two `ORDER_NOTES.md` and `hardware.csv` are written by hand.

**Nothing has been milled.** The package is not ready to order; the blockers are at the top of
[`jlccnc/ORDER_NOTES.md`](jlccnc/ORDER_NOTES.md), and [`production/README.md`](../../production/README.md)
lists every file with its state.

| Order | Where | Folder |
|---|---|---|
| Top shell, bottom shell, 2 knobs (6061-T6, bead blast, black anodise) and the RF insert (black POM), per unit | [JLCCNC](https://jlccnc.com), or [PCBWay CNC](https://www.pcbway.com/rapid-prototyping/cnc-machining/) with the same files | [`jlccnc/`](jlccnc/ORDER_NOTES.md); [`pcbway/`](pcbway/ORDER_NOTES.md) for what differs |
| Screws, set screws, feet | any hardware shop; feet at DigiKey | [`hardware.csv`](hardware.csv) |

The resin keycaps and button caps (JLC3DP), the lens (laser shop) and every bought part are in
[docs/ordering-case.md](../../docs/ordering-case.md) and [docs/bom-hand.csv](../../docs/bom-hand.csv).

## Rebuild

```sh
make cad      # cad/exports: checks, STEP, drawings, hole tables
make order    # this folder's generated files and the order index in production/
```
