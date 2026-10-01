"""NoiseMap concept media (TRL 3), built from the parametric model in cad/src/model.py.

Run from the repo root:  python cad/src/concept_media.py
Main dimensions and interfaces only; not for fabrication.

The model has the street pole on the Z axis with the sidewalk surface at z = 0 and the street
toward +X. The FieldNode core hangs on the back of the pole, and the microphone head sits on its
own arm toward the street, 4.0 m above the sidewalk and 0.45 m from the pole face. Street, pole
and a 1.75 m person are grey context shown only in the hero and the blueprint isometric; they
carry no BOM number. The scene is shifted down so the node sits near Z = 0, which keeps the
kit's cutaway on the node.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build123d import Box, Pos
import concept
from concept import Part, render_all, human_figure
from model import PARAMS as P, derived, build_parts, pole

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

D = derived(P)
CURB_X = D["r"] + 450.0            # curb 0.45 m in front of the pole face
SW = 150.0                          # curb height; road surface at z = -150

parts = [Part(name, shape, colour, bom, explode) for _, name, shape, colour, bom, explode in build_parts()]
for _p in parts:                    # keep the level processor board inside the frame of the exploded view
    if _p.name.startswith("Level processor"):
        _p.explode = (380, 0, -140)
sidewalk = Pos(CURB_X - 1100, 0, -SW / 2) * Box(2200, 2400, SW)
road = Pos(CURB_X + 700, 0, -SW - 30) * Box(1400, 2400, 60)
person = human_figure(1750.0, x=-900.0, y=-700.0, z=0.0)
person.name = "Person, 1.75 m"
context = [Part("Street pole, 114 mm", pole(P, -SW, 5000.0), "#9CA3AF"),
           Part("Sidewalk and road", sidewalk + road, "#B8BDC4"), person]

SHIFT = Pos(0, 0, -(P["enc_z0"] + P["mic_z"]) / 2)
for _p in parts + context:
    _p.shape = SHIFT * _p.shape


def data_and_energy_flow(out):
    """Two-row flow: data (what leaves the head and the node) and daily energy (estimates)."""
    INK, ACCENT, LOSS = "#111827", "#0F766E", "#C2410C"
    fig, ax = plt.subplots(figsize=(15, 6.2), dpi=160)
    ax.set_xlim(0, 15); ax.set_ylim(-6.3, 1.6); ax.set_axis_off()

    def row(y, stages, lw):
        for i, (name, val) in enumerate(stages):
            x = i * 3 + 0.3
            ax.add_patch(FancyBboxPatch((x - 0.15, y - 0.55), 2.4, 1.3, boxstyle="round,pad=0.02,rounding_size=0.12",
                                        fc="#F0FDFA", ec=ACCENT, lw=1.4))
            ax.text(x + 1.05, y + 0.35, name, ha="center", va="center", fontsize=8.5, fontweight="bold", color=INK)
            ax.text(x + 1.05, y - 0.15, val, ha="center", va="center", fontsize=8, color=ACCENT, linespacing=1.3)
            if i < len(stages) - 1:
                ax.add_patch(FancyArrowPatch((x + 2.3, y + 0.1), (x + 2.8, y + 0.1), arrowstyle="-|>",
                                             mutation_scale=14, lw=lw[i], color=ACCENT, alpha=0.6))

    def branch(i, y, text):
        x = i * 3 + 0.3 + 1.05
        ax.add_patch(FancyArrowPatch((x, y - 0.6), (x, y - 1.35), arrowstyle="-|>", mutation_scale=12,
                                     lw=2.5, color=LOSS, alpha=0.6))
        ax.text(x, y - 1.7, text, ha="center", va="center", fontsize=8, color=LOSS, linespacing=1.3)

    ax.text(0.15, 1.25, "Data: the head firmware sends levels only", fontsize=9.5, fontweight="bold", color=INK)
    row(0.2, [("MEMS microphone", "24-bit I2S or PDM, 48 kHz\n1.15 Mbit/s, RAM only"),
              ("Level processor", "A and C weighting,\nFast time weighting"),
              ("Levels over M12", "12-byte frame each second\n120 bit/s on a 9.6 kbit/s UART"),
              ("FieldNode core", "15 min record, 22 bytes\n1 min LAeq, L10, L90, max"),
              ("TwinKit or city server", "levels and device\nhealth only")],
        [7, 4, 1.5, 1.5])
    branch(0, 0.2, "Samples overwritten in RAM\nabout every 20 ms, never stored")
    branch(1, 0.2, "UART 150 times too slow for raw\naudio; privacy rests on firmware")

    ax.text(0.15, -2.55, "Energy per day (NSM-CAL-001 estimates, 12.2 mW design load)", fontsize=9.5, fontweight="bold", color=INK)
    row(-3.6, [("6 W panel", "9.0 Wh/day nominal\nat 1.5 sun hours"),
               ("MPPT charger", "7.2 Wh/day in\n5.81 Wh/day stored"),
               ("LiFePO4 cell", "19 Wh, 15.4 Wh usable\n53 days without sun"),
               ("Node load", "0.29 Wh/day\nhead 95 %, core 5 %")],
        [7, 4.5, 1.5])
    branch(0, -3.6, "Heat, dust, street shade\nabout 20 % derating")
    branch(1, -3.6, "Charger and cell\nabout 19 % loss")
    branch(2, -3.6, "Surplus about 5.5 Wh/day\n(cell full, charger throttles)")

    fig.text(0.01, 0.97, "NoiseMap: data and energy flow", fontsize=10, fontweight="bold", color=INK, va="top")
    fig.text(0.01, 0.93, "CONCEPT, NOT FOR FABRICATION. Values are paper estimates from NSM-CAL-001.",
             fontsize=6.5, color="#B45309", va="top")
    fig.savefig(out, facecolor="white", bbox_inches="tight"); plt.close(fig)


if __name__ == "__main__":
    import os
    os.chdir(ROOT)
    concept.ROOT = ROOT
    render_all(
        parts, project="NoiseMap", title="Level-only noise node concept", dwg_no="NSM-DWG-010",
        key_figures=["Microphone 4.0 m up, 0.45 m off the pole face",
                     "LAeq, LAFmax, L10, L90, LCeq; 22-byte 15 min records",
                     "Head sends levels only; audio stays in its RAM",
                     "12.2 mW; 53 days without sun (NSM-CAL-001)",
                     "Range 34.9 (27.9 with IM72D128) to 113 dBA",
                     "NoiseMap parts $62 vs $100; node $188 with FieldNode"],
        date="2026-09-25",
        scale_figure=False, context=context,
        cut_exclude=["Solar panel, 6 W", "Panel tilt bracket", "Street pole adapter, V-blocks and bands", "Sensor cable, M12"],
    )
    data_and_energy_flow(ROOT / "media" / "flow.png")
    for d in (ROOT / "media").glob("_views*"):
        shutil.rmtree(d, ignore_errors=True)
