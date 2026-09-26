"""NoiseMap concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Coordinates in mm. Road surface at Z = 0, curb face at X = 0, sidewalk at X < 0 (top at Z = 150),
street running along Y. A street pole stands 450 mm behind the curb. The node is a standard
FieldNode core on the back of the pole with its 6 W panel as a hood, and a microphone head on a
short arm toward the street, with the microphone about 4 m above the ground (the height used for
strategic noise maps). Street, pole and person are grey context shown only in the hero and the
blueprint isometric; they carry no BOM number.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
from build123d import Box, Cylinder, Sphere, Pos, Rot, Solid, Plane, Vector
import concept
from concept import Part, render_all, human_figure

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# ---------------- street context ----------------
SW = 150.0                      # sidewalk top above road
POLE_X, POLE_R = -450.0, 57.0   # 114 mm (4.5 in) steel street pole
POLE_TOP = SW + 5000.0
MIC_Z = SW + 4000.0             # microphone about 4.0 m above the sidewalk
ENC_Z = SW + 3450.0             # FieldNode enclosure center height


def tube3(a, b, r):
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def band(z, r_in=POLE_R + 1, w=30.0):
    return Pos(POLE_X, 0, z) * (Cylinder(r_in + 4, w) - Cylinder(r_in, w + 2))


sidewalk = Pos(-1100, 0, SW / 2) * Box(2200, 2400, SW)
road = Pos(700, 0, -30) * Box(1400, 2400, 60)
street = sidewalk + road
pole = Pos(POLE_X, 0, SW + 2500) * Cylinder(POLE_R, 5000)

person = human_figure(1750.0, x=-1350.0, y=-700.0, z=SW)
person.name = "Person, 1.75 m"

# ---------------- NoiseMap parts ----------------
# 1 FieldNode enclosure, IP65 polycarbonate about 200 (H) x 150 (W) x 90 (D) mm, on the back of the pole
ENC_H, ENC_W, ENC_D, WALL = 200.0, 150.0, 90.0, 3.0
enc_x = POLE_X - POLE_R - 22 - ENC_D / 2
enclosure = (Pos(enc_x, 0, ENC_Z) * (Box(ENC_D, ENC_W, ENC_H) - Box(ENC_D - 2 * WALL, ENC_W - 2 * WALL, ENC_H - 2 * WALL))
             + Pos(enc_x + ENC_D / 2 + 5, 0, ENC_Z) * Box(10, 70, ENC_H - 30))

# 2 FieldNode power and radio board (MPPT charger, STM32WL LoRaWAN, flash, M12 ports) plus whip antenna
board = Pos(enc_x + ENC_D / 2 - WALL - 8, 0, ENC_Z + 25) * Box(8, 120, 120)
antenna = Pos(enc_x - 20, 45, ENC_Z - ENC_H / 2 - 70) * Cylinder(6, 140)

# 3 LiFePO4 cell, 32700 size, lying in the enclosure base
cell = Pos(enc_x - 10, 0, ENC_Z - 60) * Rot(90, 0, 0) * Cylinder(16, 70)

# 4 Solar panel, 6 W, about 290 x 200 x 17 mm, above the enclosure as a sun and rain hood
PANEL_Z = ENC_Z + ENC_H / 2 + 110
panel = Pos(enc_x - 40, 0, PANEL_Z) * Rot(0, -35, 0) * Box(200, 290, 17)

# 5 Panel tilt bracket: two flat-bar posts from the enclosure rail to the panel
bracket = (tube3((enc_x + ENC_D / 2 + 5, -110, ENC_Z + ENC_H / 2 - 20), (enc_x + 10, -110, PANEL_Z + 22), 6)
           + tube3((enc_x + ENC_D / 2 + 5, 110, ENC_Z + ENC_H / 2 - 20), (enc_x + 10, 110, PANEL_Z + 22), 6))

# 6 FieldNode pole mounting kit: back plate V-blocks and two stainless band clamps
mount = band(ENC_Z - 60) + band(ENC_Z + 60) + Pos(POLE_X - POLE_R - 8, 0, ENC_Z) * Box(16, 60, 170)

# 7 Microphone arm: 25 mm aluminium tube reaching about 400 mm toward the street, own band clamp
ARM_Z = MIC_Z - 210.0
ARM_X1 = POLE_X + POLE_R + 400.0
arm = (tube3((POLE_X + POLE_R, 0, ARM_Z), (ARM_X1, 0, ARM_Z), 12.5)
       + Pos(POLE_X + POLE_R + 5, 0, ARM_Z) * Box(10, 60, 90)
       + band(ARM_Z))

# 8 Microphone head housing: printed ASA tube 40 mm OD, 150 mm tall, with drip skirt
HEAD_Z0 = ARM_Z + 12.5
HEAD_H = 150.0
head = (Pos(ARM_X1, 0, HEAD_Z0 + HEAD_H / 2) * (Cylinder(20, HEAD_H) - Pos(0, 0, 3) * Cylinder(17, HEAD_H))
        + Pos(ARM_X1, 0, HEAD_Z0 + HEAD_H - 20) * (Cylinder(32, 4) - Cylinder(20, 6)))

# 9 MEMS microphone on a small board at the top of the tube, port facing up
mic = (Pos(ARM_X1, 0, HEAD_Z0 + HEAD_H - 4) * Cylinder(15, 2)
       + Pos(ARM_X1, 0, HEAD_Z0 + HEAD_H - 1.5) * Box(4, 3.5, 2))

# 10 Level processor board (Cortex-M4F class) inside the tube
proc = Pos(ARM_X1, 0, HEAD_Z0 + 65) * Box(10, 26, 70)

# 11 Foam windscreen, 90 mm ball bored to slide over the head tube, with a bird spike
WS_Z = HEAD_Z0 + HEAD_H + 10
windscreen = Pos(ARM_X1, 0, WS_Z) * Sphere(45) - Pos(ARM_X1, 0, WS_Z - 25) * Cylinder(20.5, 50)
spike = tube3((ARM_X1, 0, WS_Z + 40), (ARM_X1, 0, WS_Z + 150), 1.5)

# 12 M12 sensor cable: enclosure port, round the pole, along the arm into the head
cable = (tube3((enc_x + 20, -45, ENC_Z + ENC_H / 2), (POLE_X - 20, -POLE_R - 8, ARM_Z - 60), 3.5)
         + tube3((POLE_X - 20, -POLE_R - 8, ARM_Z - 60), (POLE_X + POLE_R + 20, -18, ARM_Z - 20), 3.5)
         + tube3((POLE_X + POLE_R + 20, -18, ARM_Z - 20), (ARM_X1 - 25, -18, ARM_Z - 20), 3.5)
         + tube3((ARM_X1 - 25, -18, ARM_Z - 20), (ARM_X1, -18, HEAD_Z0 + 10), 3.5))

parts = [
    Part("FieldNode enclosure, IP65", enclosure, "#E5E7EB", 1, (-300, 0, 0)),
    Part("FieldNode power and radio board", board + antenna, "#16A34A", 2, (-620, 0, 60)),
    Part("LiFePO4 cell, 6 Ah", cell, "#C2410C", 3, (-480, 0, -240)),
    Part("Solar panel, 6 W", panel, "#1E3A8A", 4, (200, 0, 420)),
    Part("Panel tilt bracket", bracket, "#6B7280", 5, (-150, 0, 180)),
    Part("Pole mounting kit and clamps", mount, "#94A3B8", 6, (0, -300, -120)),
    Part("Microphone arm, aluminium", arm, "#A16207", 7, (0, 0, -60)),
    Part("Microphone head housing, ASA", head, "#0F766E", 8, (300, 0, 0)),
    Part("MEMS microphone, I2S", mic, "#7C3AED", 9, (300, 0, 260)),
    Part("Level processor, M4F class", proc, "#2563EB", 10, (500, 0, 60)),
    Part("Foam windscreen and bird spike", windscreen + spike, "#374151", 11, (300, 0, 480)),
    Part("Sensor cable, M12", cable, "#111827", 12, (0, -320, -200)),
]

context = [
    Part("Street pole, 5 m", pole, "#9CA3AF"),
    Part("Sidewalk and road", street, "#B8BDC4"),
    person,
]

# Shift everything so the node sits near the origin.
SHIFT = Pos(-POLE_X, 0, -(ENC_Z + MIC_Z) / 2)
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

    ax.text(0.15, 1.25, "Data: levels leave the head, audio never does", fontsize=9.5, fontweight="bold", color=INK)
    row(0.2, [("MEMS microphone", "24-bit I2S at 48 kHz\nabout 1.2 Mbit/s"),
              ("Level processor", "A and C weighting,\nFast time weighting"),
              ("Levels over M12", "1 s LAF and LCeq values\nabout 0.1 kbit/s, UART"),
              ("FieldNode core", "15 min record, 22 bytes\n1 min LAeq, L10, L90, max"),
              ("TwinKit or city server", "levels and device\nhealth only")],
        [7, 4, 1.5, 1.5])
    branch(0, 0.2, "Samples overwritten in RAM\nabout every 20 ms, never stored")
    branch(1, 0.2, "Link capped at 9.6 kbit/s,\nfar too slow for raw audio")

    ax.text(0.15, -2.55, "Energy per day (estimates, about 21 mW continuous load)", fontsize=9.5, fontweight="bold", color=INK)
    row(-3.6, [("6 W panel", "about 9 Wh/day nominal\nat 1.5 sun hours (winter)"),
               ("MPPT charger", "about 7.2 Wh/day in\nabout 5.8 Wh/day stored"),
               ("LiFePO4 cell", "19 Wh, about 15 Wh usable\nabout 30 days in the dark"),
               ("Node load", "about 0.51 Wh/day\nhead about 95 %, core 5 %")],
        [7, 4.5, 1.5])
    branch(0, -3.6, "Heat, dust, street shade\nabout 20 % derating")
    branch(1, -3.6, "Charger and cell\nabout 20 % loss")
    branch(2, -3.6, "Winter surplus about 5 Wh/day\n(cell full, charger throttles)")

    fig.text(0.01, 0.97, "NoiseMap: data and energy flow", fontsize=10, fontweight="bold", color=INK, va="top")
    fig.text(0.01, 0.93, "CONCEPT, NOT FOR FABRICATION. Values are estimates to be checked at TRL 3.",
             fontsize=6.5, color="#B45309", va="top")
    fig.savefig(out, facecolor="white", bbox_inches="tight"); plt.close(fig)


if __name__ == "__main__":
    import os
    os.chdir(ROOT)
    concept.ROOT = ROOT
    render_all(
        parts, project="NoiseMap", title="Level-only noise node concept", dwg_no="NSM-DWG-010",
        key_figures=["Microphone about 4 m above ground, 0.45 m off the pole",
                     "LAeq, LAFmax, L10, L90, LCeq; 15 min records",
                     "Audio never leaves the head; levels only",
                     "About 21 mW; about 30 days without sun (est.)",
                     "Range about 35 to 115 dBA (estimate)",
                     "Parts about $171 vs $100 budget (indicative)"],
        date="2026-09-25",
        scale_figure=False, context=context,
        cut_exclude=["Solar panel, 6 W", "Panel tilt bracket", "Pole mounting kit and clamps", "Sensor cable, M12"],
    )
    data_and_energy_flow(ROOT / "media" / "flow.png")
    for d in (ROOT / "media").glob("_views*"):
        shutil.rmtree(d, ignore_errors=True)
