"""NoiseMap prototype build plan pictures (NSM-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|layouts|joints|steps|wiring ...]
With no argument it draws everything. Every picture is drawn from cad/src/model.py
(build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/NSM-DWG-101 to 106        making sketches for the made components
    docs/05-build-plan/saddle-blank.png    flat blank of the arm saddle with every cut and hole
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/wiring.png          block-level wiring of the head (matplotlib)
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import PARAMS as P, build_components, derived, pole, patch_svg_export, zcyl  # noqa: E402

patch_svg_export()
OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-01"
D = derived(P)
C = build_components(P)


def S(*ks):
    from build123d import Compound
    shapes = [C[k].shape for k in ks]
    return shapes[0] if len(shapes) == 1 else Compound(shapes)


FN = [k for k in C if k.startswith("fn_")]
COL = {"core": "#9CA3AF", "plate": "#A8A29E", "vblock": "#57534E", "band": "#94A3B8", "saddle": "#A16207",
       "flange": "#4B5563", "tube": "#B45309", "head": "#0F766E", "cap": "#115E59", "mic": "#7C3AED",
       "proc": "#2563EB", "ws": "#374151", "spike": "#6B7280", "cable": "#111827", "lanyard": "#DC2626",
       "bolt": "#111827", "pole": "#9CA3AF", "gland": "#1F2937", "membrane": "#F59E0B"}
AZ, AH = D["arm_z"], D["head_x"]


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def pole_part(z0=3150, z1=4050):
    return part("Street pole (site)", pole(P, z0, z1), COL["pole"])


def core():
    return part("FieldNode core, built to FND-BLD-001", S(*FN), COL["core"])


def cut_box(sh, x0, x1, y0, y1, z0, z1):
    from build123d import Box, Pos
    return sh & (Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0))


def cut_part(p, z0, z1):
    return part(p.name, cut_box(p.shape, -400, 400, -400, 400, z0, z1), p.color)


# ----------------------------------------------------------------- overview
def overview():
    items = [
        ("FieldNode core, built to its own plan", S(*FN), COL["core"], (-120, 0, 0)),
        ("Street pole V-blocks (2) and screws", S("vblock_low", "vblock_up", "vb_screws"), COL["vblock"], (70, 0, 0)),
        ("Head housing", S("head"), COL["head"], (260, 0, 0)),
        ("Microphone board, gasket, membrane", S("mic", "gasket", "mic_screws", "membrane"), COL["mic"], (260, 0, -240)),
        ("Level processor board", S("proc"), COL["proc"], (260, 0, -350)),
        ("Bottom cap and cable gland", S("cap", "cap_screws", "gland"), COL["cap"], (260, 0, -470)),
        ("Sensor cable", S("cable"), COL["cable"], (0, 260, -60)),
        ("Arm tube", S("tube"), COL["tube"], (40, 0, 0)),
        ("Arm saddle", S("saddle"), COL["saddle"], (-60, 0, 0)),
        ("Tube flange, screws, cross bolt", S("flange", "flange_fix"), COL["flange"], (-10, 0, 0)),
        ("Bird spike", S("spike"), COL["spike"], (260, 0, 300)),
        ("Foam windscreen", S("windscreen"), COL["ws"], (260, 0, 170)),
        ("Band clamps, street pole adapter (2)", S("vb_bands"), COL["band"], (260, 0, 0)),
        ("Band clamps, arm saddle (2)", S("s_bands"), COL["band"], (-200, 0, 0)),
        ("Safety lanyard", S("lanyard"), COL["lanyard"], (-120, 0, 90)),
    ]
    parts = [part(n, s, c, e) for n, s, c, e in items]
    return bv.overview(parts, OUT / "overview.png", "NoiseMap prototype: every component, pulled apart",
                       subtitle="Numbered in build order. Seen from the street side, above. The pole is not shown",
                       elev=16, azim=-60, size=(11, 8.5), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def at_origin(sh):
    from build123d import Pos
    c = sh.bounding_box().center()
    return Pos(-c.X, -c.Y, -c.Z) * sh


def rod_view():
    """The spike drawn as a 12-sided prism with its thread and blunt end marked, so that every
    view has outlines (a plain cylinder has none side on)."""
    import build123d as b
    L = P["spike"][0] + P["skirt_dz"] + P["skirt"][1] + 6
    rod = b.extrude(b.RegularPolygon(1.5, 12), L - 8) + b.Pos(0, 0, -8) * b.extrude(b.RegularPolygon(1.25, 12), 8)
    return at_origin(rod)


def sheets():
    base = dict(project="NoiseMap", date=DATE)
    out = []
    vb = P["vb"]
    zl = D["clamps"][0]
    plate = part("FieldNode back plate", C["fn_plate"].shape, COL["plate"])
    out.append(bv.component_sheet(
        Part("V-block", C["vblock_low"].shape, COL["vblock"]), [cut_part(plate, zl - 60, zl + 60), part("Pole", pole(P, zl - 40, zl + 40), COL["pole"])],
        dwg_no="NSM-DWG-101", title="NoiseMap street pole V-block (make 2): making sketch",
        material="Aluminium flat bar 70 x 16 mm, 6082 or 6061 class", view_shape=at_origin(C["vblock_low"].shape),
        inset_view=(60, 50),
        notes=["Make two. Saw 112 mm off 70 x 16 mm bar; saw and file the width",
               "  to 63 mm. The 112 x 16 face is the back; file it flat.",
               "Scribe a 90 degree V on both 112 x 63 faces with a 45 degree square:",
               "  106 mm wide at the front face, point 10 mm from the back face.",
               "Saw just inside both lines, file to the lines; keep the faces flat.",
               "Rebate each back corner 9 mm wide and 2 mm deep, full height:",
               "  the band passes under it. Round the front outer corners 3 mm.",
               "Drill four 14 mm lightening holes through: 15 mm from the back",
               "  at 37 mm each side, and 35 mm from the back at 45 mm each side.",
               "Drill 3.3 mm, 14 deep, tap M4 12 deep in the back face at 18 mm",
               "  each side of centre, half way up (8 mm).",
               "Fit: two M4 countersunk screws from the box side of the FieldNode",
               "  back plate. A 114 mm pole touches both V faces 40 mm off centre.",
               "Check: on a 114 mm tube the block must not rock."],
        **base))
    out.append(bv.component_sheet(
        Part("Arm saddle", C["saddle"].shape, COL["saddle"]), [part("Pole", pole(P, AZ - 120, AZ + 120), COL["pole"]),
                                                                part("Bands", C["s_bands"].shape, COL["band"]),
                                                                part("Flange", C["flange"].shape, COL["flange"]),
                                                                part("Tube", C["tube"].shape, COL["tube"])],
        dwg_no="NSM-DWG-102", title="NoiseMap arm saddle: making sketch",
        material="Aluminium sheet 2.5 mm, 5052-H32 (bends without cracking)", view_shape=at_origin(C["saddle"].shape),
        inset_view=(25, -35),
        notes=["A channel: web 114 wide x 124 tall, two flanges standing 65 out",
               "  (outside sizes). Blank 114 wide; the bending shop sets its length.",
               "Cut a 90 degree V in each end of the blank (these become the",
               "  flanges): 109 mm wide at the end, point 54.5 mm in from the end.",
               "Web: four band slots 3 x 15 at 52 mm each side of centre, centred",
               "  40 mm above and below the middle; chain drill 3 mm, file square.",
               "Web: three 5.5 mm holes on a 45 mm circle round the middle, one",
               "  straight up, for the tube flange.",
               "Bend both flanges 90 degrees the same way, inside radius about 3.",
               "Deburr and round the V edges so they cannot score the pole.",
               "Fit: the pole bears on the four V edges; each band runs round",
               "  the pole, through two slots and across the outside of the web.",
               "Check: on a 114 mm tube all four V edges touch and it does not rock."],
        **base))
    out.append(bv.component_sheet(
        Part("Arm tube", C["tube"].shape, COL["tube"]), [part("Saddle", C["saddle"].shape, COL["saddle"]),
                                                         part("Flange", C["flange"].shape, COL["flange"]),
                                                         part("Head", C["head"].shape, COL["head"])],
        dwg_no="NSM-DWG-103", title="NoiseMap arm tube: making sketch",
        material="Aluminium round tube 25 x 2 mm, 6063", view_shape=at_origin(C["tube"].shape), inset_view=(25, -60),
        notes=[f"Cut {D['arm_len']:.0f} mm of 25 x 2 mm tube; square and deburr both ends.",
               "Mark one end as the pole end.",
               f"Drill 4.6 mm straight through, top to bottom, {P['flange'][4] / 2:.1f} mm from",
               "  the pole end (the flange cross bolt).",
               "Drill 4.6 mm straight through, in the same plane, 12.5 mm from",
               "  the far end (the head cross bolt).",
               "Drill both holes on a drill press with the tube in a V-block so",
               "  each hole passes through the centre line.",
               "Fit: the pole end goes 25 mm into the tube flange's socket, the",
               "  far end 25 mm into the head's socket; one bolt through each.",
               "Check: both holes line up when you sight along the tube."],
        **base))
    hz = AZ
    out.append(bv.component_sheet(
        Part("Head housing", C["head"].shape, COL["head"]), [part("Tube", C["tube"].shape, COL["tube"]),
                                                             part("Windscreen", C["windscreen"].shape, COL["ws"], alpha=0.5),
                                                             part("Cap", C["cap"].shape, COL["cap"])],
        dwg_no="NSM-DWG-104", title="NoiseMap head housing: making sketch",
        material="ASA, 3D printed, 4 walls, 40 % infill", view_shape=at_origin(C["head"].shape), inset_view=(20, -60),
        notes=["Tube 40 OD x 3 wall x 150 tall, closed at the top by a 2 mm plate",
               "  with a 3 mm acoustic port on the axis.",
               "Drip skirt 64 OD, its top 58 below the port; 45 degree cone under",
               "  it so it prints without support. Spike boss on it, 26 off the axis.",
               "Arm socket 33 OD, bore 25.4, 25 deep, its axis 120 below the port;",
               "  4.4 mm cross hole 12.5 in from its open end, top to bottom.",
               "Inside: two card guides with 1.8 mm slots for the processor board;",
               "  two 5 mm bosses under the top plate, 20 apart, for the mic board.",
               "Two 3.2 mm holes 4 above the open end for the cap screws.",
               "Print standing on the top plate, supports under the arm socket only.",
               "Press an M3 heat-set insert into the spike boss.",
               "Check: the port is clear; a 25 mm tube slides into the socket."],
        **base))
    out.append(bv.component_sheet(
        Part("Bottom cap", C["cap"].shape, COL["cap"]), [part("Head", C["head"].shape, COL["head"]),
                                                         part("Gland", C["gland"].shape, COL["gland"])],
        dwg_no="NSM-DWG-105", title="NoiseMap head bottom cap: making sketch",
        material="ASA, 3D printed, solid", view_shape=at_origin(C["cap"].shape), inset_view=(-25, -60),
        notes=["Disc 40 OD x 3 thick with a ring standing 8 on it: 34 OD, 3 wall.",
               "16 mm hole on the axis for the M16 cable gland.",
               "Two 2.8 mm holes across the ring, 4 up from the disc, opposite",
               "  each other, for the M3 screws (they self-tap into the ring).",
               "Print disc down; no supports.",
               "Fit: the ring slides into the open end of the head until the disc",
               "  meets the tube; two M3 x 6 screws through the head wall.",
               "The gland goes through the 16 mm hole from below, nut inside.",
               "Check: the ring slides in by hand; the screw holes line up."],
        **base))
    out.append(bv.component_sheet(
        Part("Bird spike", C["spike"].shape, COL["spike"]), [part("Head", C["head"].shape, COL["head"]),
                                                             part("Windscreen", C["windscreen"].shape, COL["ws"], alpha=0.5)],
        dwg_no="NSM-DWG-106", title="NoiseMap bird spike: making sketch",
        material="Stainless steel rod 3 mm, A2 (304)", view_shape=rod_view(), inset_view=(15, -60),
        notes=[f"Cut {P['spike'][0] + P['skirt_dz'] + P['skirt'][1] + 6:.0f} mm of 3 mm stainless rod.",
               "Cut an M3 thread 8 mm long on one end with a die.",
               "Round the other end slightly with a file: a blunt tip, not a point.",
               "Fit: screws into the heat-set insert in the skirt boss, 26 mm off",
               "  the head axis, and rises through the foam windscreen.",
               "Unscrew it before you lift the windscreen off.",
               "Check: it stands upright and its top is 160 mm above the port."],
        **base))
    return out


# ----------------------------------------------------------------- flat blank of the arm saddle
def layouts():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon, Rectangle
    INK, MUT, AC = "#111827", "#4B5563", "#0F766E"
    sw, sh, sdp, st = P["saddle"]
    web = sh - 2 * st                       # flat web between the bends (approximate; shop sets the allowance)
    fl = sdp - st
    L = web + 2 * fl
    v_depth = D["s_apex"] - D["s_tip"]
    v_half = D["s_half_mouth"]
    fig = plt.figure(figsize=(9.5, 11), dpi=150)
    ax = fig.add_axes([0.08, 0.06, 0.62, 0.86]); ax.set_aspect("equal"); ax.set_axis_off()
    # blank outline with the V notches at both ends (y up the page, 0 at the web centre)
    pts = [(-sw / 2, -L / 2), (-v_half, -L / 2), (0, -L / 2 + v_depth), (v_half, -L / 2), (sw / 2, -L / 2),
           (sw / 2, L / 2), (v_half, L / 2), (0, L / 2 - v_depth), (-v_half, L / 2), (-sw / 2, L / 2)]
    ax.add_patch(Polygon(pts, closed=True, fc="#FEF3C7", ec=INK, lw=1.2))
    for yb in (-web / 2, web / 2):
        ax.plot([-sw / 2, sw / 2], [yb, yb], color=AC, lw=0.8, ls=(0, (6, 3)))
    ax.text(sw / 2 + 4, web / 2, "bend line, 90 degrees", va="center", fontsize=7.5, color=AC)
    ax.text(sw / 2 + 4, -web / 2, "bend line, 90 degrees", va="center", fontsize=7.5, color=AC)
    ax.axvline(0, color=MUT, lw=0.5, ls=(0, (8, 3, 2, 3)))
    ax.plot([-sw / 2, sw / 2], [0, 0], color=MUT, lw=0.5, ls=(0, (8, 3, 2, 3)))
    sy, dz = P["s_slot_y"], P["s_band_dz"]
    for x in (-sy, sy):
        for z in (-dz, dz):
            ax.add_patch(Rectangle((x - 1.5, z - 7.5), 3, 15, fc="white", ec=INK, lw=1))
    pcd = P["flange"][5]
    for k in range(3):
        a = math.radians(90 + 120 * k)
        ax.add_patch(plt.Circle((pcd / 2 * math.cos(a), pcd / 2 * math.sin(a)), 2.75, fc="white", ec=INK, lw=1))
    ax.add_patch(plt.Circle((0, 0), pcd / 2, fc="none", ec=MUT, lw=0.5, ls=":"))
    # dimensions (text only, kept clear of the outline)
    ax.annotate("", xy=(-sw / 2, -L / 2 - 10), xytext=(sw / 2, -L / 2 - 10), arrowprops=dict(arrowstyle="<->", color=INK, lw=0.7))
    ax.text(0, -L / 2 - 14, f"{sw:.0f}", ha="center", va="top", fontsize=8, color=INK)
    ax.annotate("", xy=(-sw / 2 - 12, -web / 2), xytext=(-sw / 2 - 12, web / 2), arrowprops=dict(arrowstyle="<->", color=INK, lw=0.7))
    ax.text(-sw / 2 - 15, 0, f"web about {web:.0f}\nbetween bends", ha="right", va="center", fontsize=7.5, color=INK)
    ax.annotate("", xy=(-sw / 2 - 12, web / 2), xytext=(-sw / 2 - 12, L / 2), arrowprops=dict(arrowstyle="<->", color=INK, lw=0.7))
    ax.text(-sw / 2 - 15, (web / 2 + L / 2) / 2, f"flange\nabout {fl:.0f}", ha="right", va="center", fontsize=7.5, color=INK)
    ax.text(0, L / 2 - v_depth + 8, f"V point {v_depth:.1f}\nin from the end", ha="center", va="bottom", fontsize=7, color=INK,
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none"))
    ax.text(0, L / 2 + 3, f"V {2 * v_half:.0f} wide at the end", ha="center", va="bottom", fontsize=7.5, color=INK,
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none"))
    ax.text(sw / 2 + 4, dz - 4, f"slots 3 x 15 at {sy:.0f}\neach side, {dz:.0f} above\nand below the middle",
            ha="left", va="center", fontsize=7, color=INK, bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none"))
    ax.text(14, -20, f"three 5.5 holes,\n{pcd:.0f} circle", ha="left", va="top", fontsize=7, color=INK,
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none"))
    ax.set_xlim(-sw / 2 - 70, sw / 2 + 75); ax.set_ylim(-L / 2 - 26, L / 2 + 14)
    fig.text(0.04, 0.975, "Arm saddle: the flat blank before bending", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.04, 0.95, "2.5 mm 5052-H32 sheet, seen flat. Sizes in mm from the model; the bending shop sets the exact blank length\n"
             "for its bend allowance so that the flanges stand 65 out from the outside of the web.", fontsize=8.5, color=MUT, va="top")
    key = ["Cut the outline and both V notches", "  before bending.", "Slots: chain drill 3 mm, file square.",
           "Holes: 5.5 mm for the M5 flange", "  screws, one straight up.", "Bend both flanges the same way,",
           "  90 degrees, inside radius about 3.", "Deburr; round the V edges."]
    fig.text(0.72, 0.86, "Order of work", fontsize=9, fontweight="bold", color=INK, va="top")
    for i, t in enumerate(key):
        fig.text(0.72, 0.83 - i * 0.022, t, fontsize=8, color=INK, va="top")
    fig.text(0.04, 0.015, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    fig.text(0.96, 0.015, "github.com/BoujeeEnjinia1701/noisemap", fontsize=7, color=AC, ha="right", family="monospace")
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "saddle-blank.png", facecolor="white"); plt.close(fig)
    return OUT / "saddle-blank.png"


# ----------------------------------------------------------------- joints
def joints():
    out = []
    zl = D["clamps"][0]
    pl = pole(P, zl - 200, zl + 200)
    # 01 V-block, pole and band, seen from above, cut at the lower clamp
    bx_ = (-140, 80, -90, 90, zl - 7, zl + 4)
    out.append(bv.joint([
        part("Pole (site)", cut_box(pl, *bx_), COL["pole"]),
        part("FieldNode back plate", cut_box(C["fn_plate"].shape, *bx_), COL["plate"]),
        part("V-block", cut_box(C["vblock_low"].shape, *bx_), COL["vblock"]),
        part("Band, through the plate slots", cut_box(C["vb_bands"].shape, *bx_), COL["band"]),
        part("M4 countersunk screws", cut_box(C["vb_screws"].shape, *bx_), COL["bolt"])],
        OUT / "joint-01.png", "Joint 1: street pole V-block, pole and band (lower clamp)",
        subtitle="Cut level with the band, seen from above. The pole bears on both V faces; the band pulls it in",
        elev=82, azim=-90, size=(8, 6)))
    # 02 band rebate and plate slot, close up
    bx_ = (-100, -70, 30, 66, zl - 8, zl + 2)
    out.append(bv.joint([
        part("FieldNode back plate, slot", cut_box(C["fn_plate"].shape, *bx_), COL["plate"]),
        part("V-block, rebated corner", cut_box(C["vblock_low"].shape, *bx_), COL["vblock"]),
        part("Band", cut_box(C["vb_bands"].shape, *bx_), COL["band"])],
        OUT / "joint-02.png", "Joint 2: band through the rebate and the plate slot (one corner, cut at the band)",
        subtitle="Seen from above. The band comes along the V-block's side, runs under its rebate, through the slot and across the plate",
        elev=80, azim=-90, size=(8, 6)))
    # 03 arm saddle on the pole, cut at the upper arm band
    zb = AZ + P["s_band_dz"]
    bx_ = (-90, 140, -90, 90, zb - 7, zb + 4)
    out.append(bv.joint([
        part("Pole (site)", cut_box(pole(P, AZ - 200, AZ + 200), *bx_), COL["pole"]),
        part("Arm saddle, top flange and web", cut_box(C["saddle"].shape, -90, 140, -90, 90, zb - 7, AZ + 70), COL["saddle"]),
        part("Band, through the web slots", cut_box(C["s_bands"].shape, *bx_), COL["band"])],
        OUT / "joint-03.png", "Joint 3: arm saddle on the pole (upper band)",
        subtitle="Seen from above, cut through the pole at the band. The pole bears on the flange's V edges; the band crosses the web outside",
        elev=85, azim=-90, size=(8, 6)))
    # 04 flange, web and tube, cut open on the arm's centre plane
    bx_ = (80, 150, -40, 0.01, AZ - 45, AZ + 62)
    out.append(bv.joint([
        part("Arm saddle web (nuts on its inside)", cut_box(C["saddle"].shape, *bx_), COL["saddle"]),
        part("Tube flange", cut_box(C["flange"].shape, *bx_), COL["flange"]),
        part("Arm tube", cut_box(C["tube"].shape, *bx_), COL["tube"]),
        part("M5 screws, nuts and cross bolt", cut_box(C["flange_fix"].shape, *bx_), COL["bolt"])],
        OUT / "joint-04.png", "Joint 4: tube flange on the saddle web, arm tube in its socket (cut open)",
        subtitle="Seen from the side. Three M5 screws through flange and web, nuts inside the channel; one cross bolt holds the tube",
        elev=12, azim=70, size=(8, 6)))
    # 05 tube in the head socket
    bx_ = (440, 530, -40, 0.01, AZ - 40, AZ + 40)
    out.append(bv.joint([
        part("Head housing (socket)", cut_box(C["head"].shape, *bx_), COL["head"]),
        part("Arm tube", cut_box(C["tube"].shape, *bx_), COL["tube"]),
        part("M4 cross bolt and nut", cut_box(C["head_bolt"].shape, *bx_), COL["bolt"]),
        part("Processor board (in its guides)", cut_box(C["proc"].shape, *bx_), COL["proc"])],
        OUT / "joint-05.png", "Joint 5: arm tube in the head's socket (cut open)",
        subtitle="Cut on the centre line, seen from the side. The tube goes 25 mm in, to the bottom of the socket; one M4 bolt passes through both",
        elev=12, azim=70, size=(8, 6)))
    # 06 top of the head: membrane, port, gasket, microphone board
    ht = D["head_top"]
    bx_ = (AH - 24, AH + 24, -24, 0.01, ht - 9, ht + 4)
    out.append(bv.joint([
        part("Head top plate with port", cut_box(C["head"].shape, *bx_), COL["head"]),
        part("Acoustic membrane", cut_box(C["membrane"].shape, *bx_), COL["membrane"]),
        part("Gasket", cut_box(C["gasket"].shape, *bx_), "#F472B6"),
        part("Microphone board", cut_box(C["mic"].shape, *bx_), COL["mic"]),
        part("M2 screws", cut_box(C["mic_screws"].shape, *bx_), COL["bolt"])],
        OUT / "joint-06.png", "Joint 6: microphone under the port (top of the head, cut open)",
        subtitle="Cut on the centre line, seen from below. The gasket seals the board to the top plate; the membrane covers the port outside",
        elev=-10, azim=70, size=(8, 6)))
    # 07 bottom of the head: cap, gland, cable
    hb = D["head_bot"]
    bx_ = (AH - 30, AH + 30, -30, 0.01, hb - 30, hb + 20)
    out.append(bv.joint([
        part("Head housing", cut_box(C["head"].shape, *bx_), COL["head"]),
        part("Bottom cap", cut_box(C["cap"].shape, *bx_), COL["cap"]),
        part("M16 cable gland", cut_box(C["gland"].shape, *bx_), COL["gland"]),
        part("M3 cap screws", cut_box(C["cap_screws"].shape, *bx_), COL["bolt"]),
        part("Sensor cable", cut_box(C["cable"].shape, *bx_), COL["cable"])],
        OUT / "joint-07.png", "Joint 7: bottom cap and cable gland (cut open)",
        subtitle="Cut on the centre line, seen from the side. The cap's ring slides into the head and two M3 screws hold it; the gland nut sits inside the ring",
        elev=10, azim=70, size=(8, 6)))
    # 08 spike in the skirt boss, windscreen over the head
    bx_ = (AH - 50, AH + 0.01, -60, 60, ht - 80, ht + 170)
    out.append(bv.joint([
        part("Head housing and skirt", cut_box(C["head"].shape, *bx_), COL["head"]),
        part("Foam windscreen", cut_box(C["windscreen"].shape, *bx_), "#9CA3AF", alpha=1.0),
        part("Bird spike", cut_box(C["spike"].shape, *bx_), COL["spike"])],
        OUT / "joint-08.png", "Joint 8: windscreen and bird spike (cut open)",
        subtitle="Cut through the spike, seen from the street. The foam sits on the port; the spike screws into the skirt boss and rises through the foam",
        elev=8, azim=10, size=(8, 6)))
    return out


# ----------------------------------------------------------------- assembly steps
def steps():
    out = []

    def st(n, done, new, title, sub, **kw):
        out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    def mv(name, shape, color, e):
        return part(name, shape, color, e)
    fncore = core()
    st(1, [fncore], [mv("Upper V-block", C["vblock_up"].shape, COL["vblock"], (110, 0, 0)),
                     mv("Lower V-block", C["vblock_low"].shape, COL["vblock"], (110, 0, 0))],
       "street pole V-blocks onto the FieldNode back plate",
       "Seen from the pole side. Two M4 countersunk screws each, from the box side of the plate, threadlocker",
       elev=20, azim=20, label_done=True)
    head = part("Head housing", C["head"].shape, COL["head"])
    st(2, [head], [mv("Gasket and microphone board", S("gasket", "mic", "mic_screws"), COL["mic"], (0, 0, -200)),
                   mv("Acoustic membrane", C["membrane"].shape, COL["membrane"], (0, 0, 40))],
       "microphone board and membrane",
       "Board up the open end onto its bosses, gasket between, two M2 screws; membrane stuck over the port outside",
       elev=-15, azim=-60, label_done=True)
    hm = [head, part("Microphone board", S("gasket", "mic", "mic_screws", "membrane"), COL["mic"])]
    st(3, hm, [mv("Level processor board", C["proc"].shape, COL["proc"], (0, 0, -160))],
       "processor board into the card guides",
       "Solder the four short leads from the microphone board first; slide the board up the guides",
       elev=-15, azim=-60, label_done=False)
    hm2 = hm + [part("Processor", C["proc"].shape, COL["proc"])]
    st(4, hm2, [mv("Bottom cap, gland and cable", S("cap", "gland", "cap_screws"), COL["cap"], (0, 0, -90)),
                mv("Sensor cable end", cut_box(C["cable"].shape, AH - 40, AH + 40, -40, 40, D["head_bot"] - 80, D["head_bot"]),
                   COL["cable"], (0, 0, -90))],
       "cable through the gland; cap into the head",
       "Wire the cable to the processor, push the cap's ring into the head, two M3 screws; tighten the gland",
       elev=-15, azim=-60, label_done=False)
    sad = part("Arm saddle", C["saddle"].shape, COL["saddle"])
    st(5, [sad], [mv("Tube flange and M5 screws", S("flange", "flange_fix"), COL["flange"], (80, 0, 0))],
       "tube flange onto the arm saddle",
       "Flange on the outside of the web; three M5 screws, nyloc nuts inside the channel",
       elev=15, azim=-40, label_done=True)
    sf = [sad, part("Tube flange", S("flange", "flange_fix"), COL["flange"])]
    st(6, sf, [mv("Arm tube", C["tube"].shape, COL["tube"], (150, 0, 0))],
       "arm tube into the flange",
       "Push it to the bottom of the socket, holes lined up; M5 cross bolt and nyloc nut, then the set screw",
       elev=15, azim=-40, label_done=False)
    headfull = part("Head with boards and cap", S("head", "mic", "gasket", "membrane", "proc", "cap", "gland", "cap_screws"), COL["head"])
    sft = sf + [part("Arm tube", C["tube"].shape, COL["tube"])]
    st(7, sft, [mv("Head (with boards and cap)", S("head", "mic", "gasket", "membrane", "proc", "cap", "gland", "cap_screws", "head_bolt"),
                   COL["head"], (120, 0, 0))],
       "head onto the arm",
       "Socket over the tube end, port up and square; M4 cross bolt and nyloc nut",
       elev=15, azim=-40, label_done=False)
    arm_done = sft + [headfull]
    st(8, arm_done, [mv("Bird spike", C["spike"].shape, COL["spike"], (0, 0, 200)),
                     mv("Foam windscreen", C["windscreen"].shape, COL["ws"], (0, 0, 130))],
       "windscreen and bird spike",
       "Push the foam down over the head onto the port; screw the spike down through the foam into its boss",
       elev=15, azim=-40, label_done=False)
    pl = pole_part(3150, 4100)
    st(9, [], [mv("FieldNode core with V-blocks", S(*FN, "vblock_low", "vblock_up", "vb_screws"), COL["core"], (-140, 0, 0)),
               mv("Band clamps (2)", C["vb_bands"].shape, COL["band"], (0, 0, 0))],
       "FieldNode core onto the pole",
       "Pole in both V-blocks; each band round the pole, under the rebates, through the plate slots and across the plate",
       context=[pl], elev=20, azim=-130, label_done=False)
    arm_all = S("saddle", "flange", "flange_fix", "tube", "head", "mic", "gasket", "membrane", "proc", "cap", "gland",
                "cap_screws", "head_bolt", "spike", "windscreen")
    core_on = [part("FieldNode core", S(*FN, "vblock_low", "vblock_up", "vb_screws", "vb_bands"), COL["core"])]
    st(10, core_on, [mv("Arm, head and windscreen", arm_all, COL["saddle"], (160, 0, 0)),
                     mv("Band clamps (2)", C["s_bands"].shape, COL["band"], (0, 0, 0))],
       "arm saddle onto the pole",
       "Saddle V edges on the pole, arm toward the street, head upright; two bands through the web slots",
       context=[pl], elev=20, azim=-50, label_done=False)
    arm_on = core_on + [part("Arm", arm_all, COL["saddle"]), part("Bands", C["s_bands"].shape, COL["band"])]
    st(11, arm_on, [mv("Safety lanyard", C["lanyard"].shape, COL["lanyard"], (0, 0, 120))],
       "safety lanyard",
       "Loop round the pole above the saddle and round the arm beside the flange; thimbles and ferrules, no slack",
       context=[pl], elev=20, azim=-50, label_done=False)
    st(12, arm_on + [part("Lanyard", C["lanyard"].shape, COL["lanyard"])],
       [mv("Sensor cable", C["cable"].shape, COL["cable"], (0, 120, 0))],
       "cable into port A and tied along",
       "Plug into the core's port A; tie to the pole and along the side of the arm; leave a drip loop under the head",
       context=[pl], elev=20, azim=-60, label_done=False)
    return out


# ----------------------------------------------------------------- wiring
def wiring():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    fig = plt.figure(figsize=(12, 6.2), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 120); ax.set_ylim(0, 62); ax.set_axis_off()
    INK, MUT = "#111827", "#4B5563"
    ax.text(2, 60, "NoiseMap prototype: head wiring", fontsize=13, fontweight="bold", color=INK, va="top")
    ax.text(2, 56.6, "Block level. The head has no storage and no radio; only level frames leave it, on the UART pair. "
            "Stranded copper, 0.25 mm² (24 AWG) throughout.", fontsize=8.5, color=MUT, va="top")
    ax.text(2, 53.4, "M12 pins: 1 = 3.3 V, 2 and 4 = UART pair, 3 = ground, 5 not used. Port A on the FieldNode is labelled 3.3 V.", fontsize=8.5, color=MUT, va="top")
    ax.text(2, 1.5, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    ax.text(118, 1.5, "github.com/BoujeeEnjinia1701/noisemap", fontsize=7, color="#0F766E", ha="right", family="monospace")
    ax.add_patch(FancyBboxPatch((3, 10), 58, 40, boxstyle="round,pad=0.4", fc="#F0FDFA", ec="#0F766E", lw=1, ls="--"))
    ax.text(4.5, 48.6, "Inside the microphone head", fontsize=8, color=MUT, va="top")

    def blk(x, y, w, h, title, sub, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc="white", ec=color, lw=1.8))
        ax.text(x + w / 2, y + h - 1.4, title, ha="center", va="top", fontsize=9, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h - 4.3, sub, ha="center", va="top", fontsize=7.2, color=MUT, linespacing=1.3)

    def wire(pts, color, lw=2.0):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", zorder=1)

    def lab(x, y, text, color, ha="left"):
        ax.text(x, y, text, fontsize=7.4, color=color, ha=ha, va="center", zorder=3,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
    RED, BLU, GRY = "#B91C1C", "#1D4ED8", "#6B7280"
    blk(6, 30, 18, 14, "Microphone board", "ICS-43434 (I2S) or\nIM72D128 (PDM),\nunder the port", "#7C3AED")
    blk(34, 16, 22, 28, "Level processor", "Cortex-M4F board\nI2S or PDM in\nUART out, 9,600 baud\nread-out protection\nno storage, no radio", "#2563EB")
    blk(66, 22, 14, 16, "Cable gland", "M16, in the\nbottom cap", "#1F2937")
    blk(90, 18, 26, 24, "FieldNode core", "sensor port A (M12)\nset to the 3.3 V rail,\nlabelled 3.3 V", "#9CA3AF")
    ax.add_patch(FancyBboxPatch((95, 11.2), 16, 4.2, boxstyle="round,pad=0.2", fc="white", ec=INK, lw=1.2))
    ax.text(103, 13.3, "PORT A: 3.3 V", fontsize=8, fontweight="bold", color=INK, ha="center", va="center")
    # microphone to processor
    wire([(24, 41), (34, 41)], RED); lab(29, 43, "3.3 V", RED, "center")
    wire([(24, 38), (34, 38)], GRY); lab(29, 39.5, "ground", GRY, "center")
    wire([(24, 35), (34, 35)], BLU); lab(29, 36.5, "clock", BLU, "center")
    wire([(24, 32), (34, 32)], BLU); lab(29, 33.5, "data", BLU, "center")
    ax.text(15, 27, "four short leads,\nabout 60 mm", fontsize=7.2, color=MUT, ha="center", va="top")
    # processor to cable
    for i, (name, pin, col) in enumerate((("3.3 V", "pin 1", RED), ("TX (levels out)", "pin 2", BLU), ("ground", "pin 3", GRY), ("RX", "pin 4", BLU))):
        y = 37 - i * 4
        wire([(56, y), (66, y)], col)
        wire([(80, y), (90, y)], col)
        lab(61, y + 1.6, name, col, "center")
        lab(85, y + 1.6, pin, col, "center")
    ax.text(73, 14.2, "pin 5 (analog): not connected", fontsize=7, color=MUT, ha="center", va="top")
    ax.text(73, 20, "M12 5-pin cable,\nabout 1.5 m", fontsize=7.2, color=MUT, ha="center", va="top")
    ax.text(4, 7.5, "Record the colour of each conductor on the label at both ends. The fifth conductor is not connected in the head.",
            fontsize=7.6, color=INK)
    ax.text(4, 4.3, "Red: power. Grey: ground. Blue: signal. All circuits are 3.3 V from the FieldNode rail; nothing here is mains powered.",
            fontsize=7.2, color=MUT)
    out = OUT / "wiring.png"
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


if __name__ == "__main__":
    what = sys.argv[1:] or ["overview", "sheets", "layouts", "joints", "steps", "wiring"]
    fns = {"overview": overview, "sheets": sheets, "layouts": layouts, "joints": joints, "steps": steps, "wiring": wiring}
    for w in what:
        r = fns[w]()
        print(w, "->", r)
