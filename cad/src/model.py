"""NoiseMap parametric model (build123d), TRL 3, constructable design (NSM-DDR-003).

Run from the repo root:  python cad/src/model.py          (exports and checks)
                         python cad/src/model.py --check  (checks only)
Exports STEP and STL into cad/step and cad/stl:
    noisemap-assembly.step / .stl   the whole node (FieldNode core, street pole adapter, arm, head)
    noisemap-head.step / .stl       arm saddle, arm, microphone head and everything in it, windscreen
    noisemap-mount.step / .stl      FieldNode back plate, street pole adapter V-blocks and bands, arm saddle

Axes: the street pole is the Z axis (x = y = 0), Z is up with the sidewalk surface at z = 0, and
the street is toward +X. The FieldNode core hangs on the back (-X) of the pole with its panel
facing -X; the microphone arm has its own saddle and band clamps and points +X at the street.
On site the core turns about the pole to face the equator and the arm turns to face the street;
the two are independent.

Revised 2026-10-01 under Amish's 2026-09-30 instruction to make the design physically buildable
(NSM-DDR-003, "Design for construction"). What the node does is unchanged: microphone port 4.0 m
up and 0.45 m off the pole face, pointing up, in a 90 mm windscreen; levels only over the M12
cable to a standard FieldNode core; 60 to 140 mm poles; no drilling of the pole. Changes:
    the FieldNode core is the constructable FieldNode (FND-DWG-001 Rev P3, cad/src/fieldnode_core.py),
        built to its own build plan FND-BLD-001, without its small-pole V-blocks and bands;
    street pole V-blocks sawn from 16 mm aluminium bar (112 x 63 x 16, 90 deg V, four drilled
        lightening holes) in place of the machined, pocketed 110 x 60 x 40 blocks; they use
        FieldNode's own V-block screw holes and band slots, with a rebate at each back corner for
        the band;
    arm saddle bent from 2.5 mm aluminium sheet (a channel whose flanges carry the V), held by two
        bands through slots in its web, in place of a milled, pocketed 10 mm plate with one band
        that had no path through it;
    arm tube held in a bought tube flange on the saddle and in a socket printed on the head, each
        with a cross bolt, in place of a tube with no fixing at either end;
    head housing with card guides, two bosses for the microphone board, a sealing gasket, a
        printed bottom cap with an M16 cable gland, and a 45 deg drip skirt that prints without
        support;
    bird spike screwed into a boss on the skirt and rising through the foam, in place of a rod
        floating in the foam;
    safety lanyard and cable route modelled.
Main dimensions and interfaces only; tolerances are TRL 4 work. The same PARAMS feed
docs/04-calcs/sizing.py (NSM-CAL-001), the drawing NSM-DWG-001 (cad/src/sheets.py), the concept
media (cad/src/concept_media.py) and the build plan pictures (cad/src/build_plan_media.py).
"""
import math
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fieldnode_core as fn  # noqa: E402

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # site: street pole on the Z axis (design case 114.3 mm OD, 4.5 in), range the adapter must seat
    "pole_od": 114.3, "pole_range": (60.0, 140.0),
    # microphone: port 4.0 m above the sidewalk (EU strategic noise map height), 0.45 m from the pole face
    "mic_z": 4000.0, "mic_off": 450.0,
    # 14 street pole V-blocks for the FieldNode back plate: width (Y) x depth (X) x height (Z), 90 deg V
    #   whose point is v_land from the back face; rebate (width from the outer edge x depth) at each
    #   back corner where the band passes; FieldNode's band slot and V-block screw positions
    "vb": (112.0, 63.0, 16.0), "v_land": 10.0, "vb_rebate": (9.0, 2.0),
    #   lightening holes drilled through each wing (distance from the back face, from the centre line), diameter
    "vb_holes": ((15.0, 37.0), (35.0, 45.0)), "vb_hole_d": 14.0,
    "band_w": 12.0, "band_t": 0.8, "band_slot_x": 51.0, "vb_screw_y": 18.0,
    # FieldNode core (FND-DWG-001 Rev P3): enclosure W x D x H, wall, bottom height, back plate W x H x t,
    #   plate below the enclosure, clamp heights from the enclosure bottom, panel, tilt, whip
    "enc": (150.0, 90.0, 200.0), "enc_wall": 3.0, "enc_z0": 3300.0,
    "plate": (180.0, 320.0, 3.0), "plate_drop": 40.0, "clamp_dz": (-20.0, 230.0),
    "panel": (290.0, 200.0, 17.0), "tilt": 40.0, "whip": (10.0, 190.0),
    # FieldNode sensor ports seen in NoiseMap axes (port A takes the sensor cable)
    "port_y": (54.0, 22.0),
    # 7 arm saddle: bent channel of aluminium sheet, width (Y) x web height (Z, outside) x flange
    #   depth (X, outside), sheet thickness; V point distance from the web's inner face; band
    #   slot y and band heights from the arm axis
    "saddle": (114.0, 124.0, 65.0, 2.5), "s_land": 8.0, "s_slot_y": 52.0, "s_band_dz": 40.0,
    # 7 tube flange (bought): base disc diameter x thickness, socket OD x length, socket bore depth,
    #   screw pitch circle
    "flange": (60.0, 5.0, 33.0, 30.0, 25.0, 45.0),
    # 7 arm: aluminium tube OD x wall; arm axis below the microphone port
    "arm": (25.0, 2.0), "arm_drop": 120.0,
    # 8 head housing: printed ASA tube OD x wall x height, top plate thickness, drip skirt OD x rim
    #   thickness (45 deg cone under it), skirt rim top below the port, arm socket OD x bore depth
    "head": (40.0, 3.0, 150.0), "top_t": 2.0, "skirt": (64.0, 4.0), "skirt_dz": 58.0,
    "h_socket": (33.0, 25.0),
    # head bottom cap: plate thickness, spigot length and wall; M16 gland
    "cap": (3.0, 8.0, 3.0),
    # acoustic path: port in the top plate (diameter), microphone front cavity (gasket ID x height)
    "port_d": 3.0, "cavity": (3.0, 0.5),
    # 9 microphone adapter board (diameter x t); 10 level processor board (W x D x H)
    "micboard": (28.0, 1.6), "proc": (26.0, 10.0, 70.0),
    # 11 foam windscreen (diameter), bore for the head, centre above the port; bird spike: rod length
    #   above the port, diameter, distance from the head axis
    "ws_d": 90.0, "ws_bore": 40.0, "ws_dz": 5.0, "spike": (160.0, 3.0, 26.0),
    # 12 sensor cable diameter; 13 lanyard wire diameter and its loop height above the arm axis
    "cable_d": 7.0, "lanyard": (2.0, 120.0, 135.0),
}

BOM = {  # model key: (BOM line, name)
    "enclosure": (1, "FieldNode enclosure, IP65"),
    "board": (2, "FieldNode power and radio board"),
    "cell": (3, "LiFePO4 cell, 6 Ah"),
    "panel": (4, "Solar panel, 6 W"),
    "bracket": (5, "Panel tilt bracket"),
    "plate": (6, "FieldNode back plate"),
    "arm": (7, "Microphone arm and saddle"),
    "head": (8, "Microphone head housing, ASA"),
    "mic": (9, "MEMS microphone on adapter board"),
    "proc": (10, "Level processor board"),
    "windscreen": (11, "Foam windscreen and bird spike"),
    "cable": (12, "Sensor cable, M12"),
    "adapter": (14, "Street pole adapter, V-blocks and bands"),
}
COLOUR = {"enclosure": "#E5E7EB", "board": "#16A34A", "cell": "#C2410C", "panel": "#1E3A8A", "bracket": "#6B7280",
          "plate": "#94A3B8", "arm": "#A16207", "head": "#0F766E", "mic": "#7C3AED", "proc": "#2563EB",
          "windscreen": "#374151", "cable": "#111827", "adapter": "#78716C"}
EXPLODE = {"enclosure": (-300, 0, 0), "board": (-620, 0, 60), "cell": (-480, 0, -260), "panel": (-200, 0, 420),
           "bracket": (-150, 0, 200), "plate": (-120, 0, 0), "arm": (60, 0, -80), "head": (300, 0, 0),
           "mic": (300, 0, 150), "proc": (560, 0, 40), "windscreen": (300, 0, 480), "cable": (150, -450, -350),
           "adapter": (0, 320, -120)}


@dataclass
class Comp:
    """One component: a single made or bought piece, or a matched set of fixings."""
    name: str
    shape: object
    bom: int
    kind: str          # "made", "bought", "fixing" or "fieldnode"
    group: str         # key in BOM


def derived(p=PARAMS):
    """Dimensions the calc note, the drawing and the build plan quote, computed from PARAMS."""
    r = p["pole_od"] / 2
    vw, vd, vh = p["vb"]
    apex = -r * math.sqrt(2)                              # V point (x) for the design pole: it touches both faces
    plate_front = apex - p["v_land"]                      # back plate face toward the pole
    plate_back = plate_front - p["plate"][2]              # face the enclosure sits on
    enc_back = plate_back
    enc_front = enc_back - p["enc"][1]
    v_half_mouth = vd - p["v_land"]                       # half width of the V at the block's front face
    hd, hw, hh = p["head"]
    head_x = r + p["mic_off"]
    head_top = p["mic_z"]
    head_bot = head_top - hh
    arm_z = head_top - p["arm_drop"]
    sw, sh, sdp, st = p["saddle"]
    s_apex = r * math.sqrt(2)                             # saddle V point (x), design pole touches both edges
    web_in = s_apex + p["s_land"]
    web_out = web_in + st
    fl = p["flange"]
    tube_x0 = web_out + fl[1] + fl[3] - fl[4]             # tube end at the bottom of the flange socket
    sock_x0 = head_x - hd / 2 - p["h_socket"][1] - 3.0    # open end of the head's arm socket
    tube_x1 = sock_x0 + p["h_socket"][1]                   # tube end at the bottom of the head socket
    shift = plate_front - fn.PARAMS["plate_y0"]           # FieldNode frame moved out to the street pole
    t = math.radians(p["tilt"])
    pcy = fn.PARAMS["panel_c"][0] + shift
    pcz = p["enc_z0"] + fn.PARAMS["panel_c"][1]
    half = p["panel"][1] / 2
    contact = {d: (d / 2) / math.sqrt(2) for d in p["pole_range"]}   # lateral offset of each V contact
    return {
        "r": r, "apex": apex, "plate_front": plate_front, "plate_back": plate_back,
        "enc_back": enc_back, "enc_front": enc_front, "enc_top": p["enc_z0"] + p["enc"][2],
        "plate_bot": p["enc_z0"] - p["plate_drop"], "plate_top": p["enc_z0"] - p["plate_drop"] + p["plate"][1],
        "clamps": [p["enc_z0"] + dz for dz in p["clamp_dz"]],
        "v_half_mouth": v_half_mouth, "vb_front": plate_front + vd,
        "head_x": head_x, "head_top": head_top, "head_bot": head_bot, "arm_z": arm_z,
        "s_apex": s_apex, "web_in": web_in, "web_out": web_out, "s_tip": web_out - sdp,
        "s_half_mouth": s_apex - (web_out - sdp),
        "tube_x0": tube_x0, "tube_x1": tube_x1, "arm_len": tube_x1 - tube_x0, "sock_x0": sock_x0,
        "arm_x0": web_out,
        "fn_shift": shift, "panel_cx": pcy, "panel_cz": pcz,
        "panel_low": (pcy - half * math.cos(t), pcz - half * math.sin(t)),
        "panel_high": (pcy + half * math.cos(t), pcz + half * math.sin(t)),
        "contact": contact,
        # largest pole whose V contacts stay 3 mm inside the front face of the V-block and the saddle
        "max_pole_vb": 2 * math.sqrt(2) * (v_half_mouth - 3.0),
        "max_pole_saddle": 2 * math.sqrt(2) * (s_apex - (web_out - sdp) - 3.0),
        "ws_center_z": head_top + p["ws_dz"],
        "overall_x": (enc_back - p["enc"][1], head_x + p["ws_d"] / 2),
    }


# ------------------------------------------------------------------ geometry helpers
def _b3d():
    import build123d as b
    return b


def box(x0, x1, y0, y1, z0, z1):
    b = _b3d()
    return b.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * b.Box(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0))


def zcyl(x, y, z0, z1, r):
    b = _b3d()
    return b.Pos(x, y, (z0 + z1) / 2) * b.Cylinder(r, abs(z1 - z0))


def xcyl(x0, x1, y, z, r):
    b = _b3d()
    return b.Pos((x0 + x1) / 2, y, z) * b.Rot(0, 90, 0) * b.Cylinder(r, abs(x1 - x0))


def rod(a, c, r):
    b = _b3d()
    a = b.Vector(*a); c = b.Vector(*c); d = c - a
    return b.Solid.make_cylinder(r, d.length, b.Plane(origin=a, z_dir=d.normalized()))


def path(points, r):
    """A round cable or wire along a polyline, with a ball at each bend."""
    b = _b3d()
    out = None
    for a, c in zip(points[:-1], points[1:]):
        s = rod(a, c, r)
        out = s if out is None else out + s
    for q in points[1:-1]:
        out = out + b.Pos(*q) * b.Sphere(r)
    return out


def fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def hexz(x, y, z0, z1, af):
    """Hexagon nut or bolt head (across flats af) from z0 up to z1."""
    b = _b3d()
    return b.Pos(x, y, z0) * b.extrude(b.RegularPolygon(af / math.sqrt(3), 6), abs(z1 - z0))


def _tangent_pts(px, py, rr, side):
    """Tangent point on the circle (centre origin, radius rr) seen from (px, py); side +1 or -1."""
    d = math.hypot(px, py)
    a = math.atan2(py, px)
    b_ = math.acos(rr / d)
    return rr * math.cos(a + side * b_), rr * math.sin(a + side * b_)


def band_loop(pts_pos_y, rr, z, w, t, n=90):
    """A band clamp: centreline goes through pts_pos_y (x, y with y > 0, from the end on the
    symmetry line outward to the last point before the pole), mirrored to -y, and round the pole
    (radius rr to the centreline) on the side away from the last point. Returns the solid band."""
    b = _b3d()
    last = pts_pos_y[-1]
    a_far = math.pi if last[0] > 0 else 0.0
    cands = [math.atan2(*reversed(_tangent_pts(last[0], last[1], rr, s))) for s in (1, -1)]
    wrap = lambda a: abs((a - a_far + math.pi) % (2 * math.pi) - math.pi)  # noqa: E731
    a0 = min(cands, key=wrap)
    if a_far == math.pi and a0 < 0:
        a0 += 2 * math.pi
    # arc from tp (y > 0) through the far side to the mirror point (y < 0)
    sweep = [a0 + (a_far - a0) * k / n for k in range(n + 1)]
    arc = [((rr + 0.03) * math.cos(a), (rr + 0.03) * math.sin(a)) for a in sweep]
    half = list(pts_pos_y) + arc
    full = half + [(x, -y) for x, y in reversed(half[:-1])]
    # drop exact duplicates
    clean = [full[0]]
    for q in full[1:]:
        if math.hypot(q[0] - clean[-1][0], q[1] - clean[-1][1]) > 1e-6:
            clean.append(q)
    if math.hypot(clean[0][0] - clean[-1][0], clean[0][1] - clean[-1][1]) < 1e-6:
        clean = clean[:-1]
    face = b.Face(b.Wire.make_polygon([b.Vector(x, y, 0) for x, y in clean], close=True))
    outer = b.offset(face, t / 2, kind=b.Kind.INTERSECTION)
    inner = b.offset(face, -t / 2, kind=b.Kind.INTERSECTION)
    ring = b.Pos(0, 0, z - w / 2) * (b.extrude(outer, w, dir=(0, 0, 1)) - b.extrude(inner, w, dir=(0, 0, 1)))
    # worm-drive housing on the far side of the pole
    hx = (rr + t / 2 + 5) * (1 if a_far == 0.0 else -1)
    return ring + box(hx - 5, hx + 5, -8, 8, z - w / 2 - 2, z + w / 2 + 2)


# ------------------------------------------------------------------ FieldNode core
def fieldnode_params(p=PARAMS):
    """FieldNode PARAMS for the street pole: plate stand-off and height moved, nothing else."""
    D = derived(p)
    q = dict(fn.PARAMS)
    s = D["fn_shift"]
    q["plate_y0"] = D["plate_front"]
    q["z0"] = p["enc_z0"]
    q["panel_c"] = (fn.PARAMS["panel_c"][0] + s, fn.PARAMS["panel_c"][1])
    q["post_foot"] = (fn.PARAMS["post_foot"][0] + s, fn.PARAMS["post_foot"][1])
    q["strut_foot"] = (fn.PARAMS["strut_foot"][0] + s, fn.PARAMS["strut_foot"][1])
    return q


FN_GROUP = {  # FieldNode component key -> NoiseMap BOM key
    "body": "enclosure", "lid": "enclosure", "lugs": "enclosure", "lug_screws": "enclosure", "glands": "enclosure",
    "vent": "enclosure", "ports": "board", "antenna": "board", "mplate": "board", "mplate_screws": "board",
    "power": "board", "ctrl": "board", "connectors": "board", "cell": "cell", "panel": "panel",
    "panel_bolts": "panel", "plate": "plate", "bracket_bolts": "bracket",
}
FN_LEFT_OUT = ("vblock_low", "vblock_up", "bands")   # replaced by the NoiseMap street pole adapter


def fieldnode_components(p=PARAMS):
    b = _b3d()
    turn = b.Rot(0, 0, -90)          # FieldNode faces -Y; NoiseMap's core faces -X
    out = {}
    for k, c in fn.build_components(fieldnode_params(p)).items():
        if k in FN_LEFT_OUT:
            continue
        g = FN_GROUP.get(k, "bracket")
        out["fn_" + k] = Comp("FieldNode " + c.name[0].lower() + c.name[1:], turn * c.shape, BOM[g][0], "fieldnode", g)
    return out


# ------------------------------------------------------------------ NoiseMap parts
def build_components(p=PARAMS):
    """Every component as a Comp, keyed by a short name."""
    b = _b3d()
    D = derived(p)
    r = D["r"]
    C = fieldnode_components(p)

    def add(key, name, shape, group, kind):
        C[key] = Comp(name, shape, BOM[group][0], kind, group)

    # ---------------------------------------------------------- 14 street pole adapter
    vw, vd, vh = p["vb"]
    xb, xf = D["plate_front"], D["vb_front"]
    rw, rd = p["vb_rebate"]
    bw, bt = p["band_w"], p["band_t"]
    ys = p["band_slot_x"]
    for key, zz in (("vblock_low", D["clamps"][0]), ("vblock_up", D["clamps"][1])):
        blk = box(xb, xf, -vw / 2, vw / 2, zz - vh / 2, zz + vh / 2)
        ap = D["apex"]
        m = xf - ap + 2
        tri = b.Pos(0, 0, zz - vh / 2 - 1) * b.extrude(b.Polygon((ap, 0), (ap + m, -m), (ap + m, m), align=None), vh + 2, dir=(0, 0, 1))
        blk -= tri
        for sy in (-1, 1):
            blk -= box(xb - 1, xb + rd, sy * (vw / 2 - rw), sy * (vw / 2 + 1), zz - vh, zz + vh)    # band rebate
            blk -= xcyl(xb - 1, xb + 12, sy * p["vb_screw_y"], zz, 1.9)                          # M4 tapped, 12 deep
            for hx_, hy_ in p["vb_holes"]:
                blk -= zcyl(xb + hx_, sy * hy_, zz - vh, zz + vh, p["vb_hole_d"] / 2)             # lightening hole
        add(key, "Street pole V-block, " + ("lower" if key == "vblock_low" else "upper"), blk, "adapter", "made")
    screws = []
    for zz in D["clamps"]:
        for sy in (-1, 1):
            y = sy * p["vb_screw_y"]
            screws.append(xcyl(D["plate_back"], xb + 9, y, zz, 1.9))
            screws.append(b.Pos(D["plate_back"], y, zz) * b.Rot(0, 90, 0) *
                          b.Cone(3.8, 2.0, 1.8, align=(b.Align.CENTER, b.Align.CENTER, b.Align.MIN)))
    add("vb_screws", "M4 countersunk screws, V-blocks (4)", fuse(screws), "adapter", "fixing")
    bands = []
    c = bt / 2
    for zz in D["clamps"]:
        pts = [(D["plate_back"] - c, 0.0), (D["plate_back"] - c, ys), (xb + c, ys), (xb + c, vw / 2 + c),
               (xf + 0.0, vw / 2 + c)]
        bands.append(band_loop(pts, r + c, zz, bw, bt))
    add("vb_bands", "Band clamps, street pole adapter (2)", fuse(bands), "adapter", "bought")

    # ---------------------------------------------------------- 7 arm saddle, flange, arm, bands
    sw, sh, sdp, st = p["saddle"]
    az = D["arm_z"]
    wi, wo, tip = D["web_in"], D["web_out"], D["s_tip"]
    sap = D["s_apex"]
    web = box(wi, wo, -sw / 2, sw / 2, az - sh / 2, az + sh / 2)
    fls = []
    for sz in (-1, 1):
        z_out = az + sz * sh / 2
        f = box(tip, wo, -sw / 2, sw / 2, min(z_out, z_out - sz * st), max(z_out, z_out - sz * st))
        mm = sap - tip + 2
        v = b.Pos(0, 0, z_out - (st if sz > 0 else 0) - 1) * b.extrude(
            b.Polygon((sap, 0), (sap - mm, mm), (sap - mm, -mm), align=None), st + 2, dir=(0, 0, 1))
        fls.append(f - v)
    saddle = web + fls[0] + fls[1]
    fd, ft, so, sl, sbd, pcd = p["flange"]
    for k in range(3):
        a = math.radians(90 + 120 * k)
        saddle -= xcyl(wi - 1, wo + 1, pcd / 2 * math.cos(a), az + pcd / 2 * math.sin(a), 2.75)
    for sz in (-1, 1):
        for sy in (-1, 1):
            saddle -= box(wi - 1, wo + 1, sy * p["s_slot_y"] - 1.5, sy * p["s_slot_y"] + 1.5,
                          az + sz * p["s_band_dz"] - (bw + 3) / 2, az + sz * p["s_band_dz"] + (bw + 3) / 2)
    add("saddle", "Arm saddle", saddle, "arm", "made")
    flange = xcyl(wo, wo + ft, 0, az, fd / 2) + xcyl(wo + ft, wo + ft + sl, 0, az, so / 2)
    flange -= xcyl(wo + ft + sl - sbd, wo + ft + sl + 1, 0, az, p["arm"][0] / 2 + 0.2)
    flange -= zcyl(wo + ft + sl - sbd / 2, 0, az - so, az + so, 2.3)
    for k in range(3):
        a = math.radians(90 + 120 * k)
        flange -= xcyl(wo - 1, wo + ft + 1, pcd / 2 * math.cos(a), az + pcd / 2 * math.sin(a), 2.75)
    add("flange", "Tube flange (bought)", flange, "arm", "bought")
    fix = []
    for k in range(3):
        a = math.radians(90 + 120 * k)
        yy, zz = pcd / 2 * math.cos(a), az + pcd / 2 * math.sin(a)
        fix.append(xcyl(wi - 4.5, wo + ft + 2.75, yy, zz, 2.2) + xcyl(wo + ft, wo + ft + 2.75, yy, zz, 4.75)
                   + b.Pos(wi - 4.5, yy, zz) * b.Rot(0, 90, 0) * b.extrude(b.RegularPolygon(8 / math.sqrt(3), 6), 4.5))
    xb1 = wo + ft + sl - sbd / 2                       # cross bolt through the flange socket and tube
    fix.append(zcyl(xb1, 0, az - so / 2 - 4, az + so / 2 + 3, 2.2) + zcyl(xb1, 0, az + so / 2, az + so / 2 + 3, 4.0)
               + hexz(xb1, 0, az - so / 2 - 4, az - so / 2, 8.0))
    add("flange_fix", "M5 screws and cross bolt, flange", fuse(fix), "arm", "fixing")
    ao, aw = p["arm"]
    tube = xcyl(D["tube_x0"], D["tube_x1"], 0, az, ao / 2) - xcyl(D["tube_x0"] - 1, D["tube_x1"] + 1, 0, az, ao / 2 - aw)
    for xx in (wo + ft + sl - p["flange"][4] / 2, (D["sock_x0"] + D["tube_x1"]) / 2):
        tube -= zcyl(xx, 0, az - ao, az + ao, 2.3)
    add("tube", "Arm tube", tube, "arm", "made")
    sbands = []
    for sz in (-1, 1):
        pts = [(wo + c, 0.0), (wo + c, p["s_slot_y"]), (wi - c, p["s_slot_y"])]
        sbands.append(band_loop(pts, r + c, az + sz * p["s_band_dz"], bw, bt))
    add("s_bands", "Band clamps, arm saddle (2)", fuse(sbands), "arm", "bought")

    # ---------------------------------------------------------- 8 head housing, cap, gland
    hx = D["head_x"]
    hd, hwall, hh = p["head"]
    htop, hbot = D["head_top"], D["head_bot"]
    ri = hd / 2 - hwall
    head = zcyl(hx, 0, hbot, htop, hd / 2) - zcyl(hx, 0, hbot - 1, htop - p["top_t"], ri)
    head -= zcyl(hx, 0, htop - p["top_t"] - 1, htop + 1, p["port_d"] / 2)
    so_, rim = p["skirt"]
    zr = htop - p["skirt_dz"]                                         # top of the skirt rim
    cone_h = so_ / 2 - hd / 2
    skirt = zcyl(hx, 0, zr - rim, zr, so_ / 2) + b.Pos(hx, 0, zr - rim - cone_h) * b.Cone(
        hd / 2, so_ / 2, cone_h, align=(b.Align.CENTER, b.Align.CENTER, b.Align.MIN))
    skirt -= zcyl(hx, 0, zr - rim - cone_h - 1, zr + 1, ri)
    head += skirt
    # spike boss on the skirt (heat-set insert for the M3 thread of the spike)
    sl_, sd_, sr_ = p["spike"]
    head += zcyl(hx, -sr_, zr - rim - 6, zr, 4.0)
    head -= zcyl(hx, -sr_, zr - rim - 7, zr + 1, sd_ / 2)
    # card guides for the level processor
    pw_, pd_, ph_ = p["proc"]
    zp0, zp1 = htop - p["top_t"] - 12 - ph_, htop - p["top_t"] - 12
    for sy in (-1, 1):
        rib = box(hx - 3, hx + 3, sy * (pw_ / 2 - 1.0), sy * (ri + 0.5), zp0 - 2, zp1 + 2)
        rib -= box(hx - 0.9, hx + 0.9, sy * (pw_ / 2 - 1.5), sy * (pw_ / 2), zp0 - 3, zp1 + 0.01)
        head += rib
    # microphone board bosses under the top plate
    zt = htop - p["top_t"]
    for sy in (-1, 1):
        head += zcyl(hx, sy * 10.0, zt - p["cavity"][1], zt + 0.01, 2.5)
        head -= zcyl(hx, sy * 10.0, zt - p["cavity"][1] - 1, zt + 0.8, 0.9)
    # arm socket, printed on the head
    sod, sdp_ = p["h_socket"]
    sock = xcyl(D["sock_x0"], hx, 0, az, sod / 2) - zcyl(hx, 0, az - sod, az + sod, ri)
    sock -= xcyl(D["sock_x0"] - 1, D["tube_x1"], 0, az, ao / 2 + 0.2)
    head += sock
    xh = (D["sock_x0"] + D["tube_x1"]) / 2
    head -= zcyl(xh, 0, az - sod, az + sod, 2.2)
    add("head", "Head housing", head, "head", "made")
    add("head_bolt", "M4 cross bolt, head socket",
        zcyl(xh, 0, az - sod / 2 - 4, az + sod / 2 + 2.5, 1.9) + zcyl(xh, 0, az + sod / 2, az + sod / 2 + 2.5, 3.5)
        + hexz(xh, 0, az - sod / 2 - 3.2, az - sod / 2, 7.0), "head", "fixing")
    ct, csl, cw = p["cap"]
    cap = zcyl(hx, 0, hbot - ct, hbot, hd / 2) + zcyl(hx, 0, hbot, hbot + csl, ri)
    cap -= zcyl(hx, 0, hbot, hbot + csl + 1, ri - cw)
    cap -= zcyl(hx, 0, hbot - ct - 1, hbot + 1, 8.0)
    for sy in (-1, 1):
        cap -= rod((hx, sy * (ri - 3.5), hbot + csl / 2), (hx, sy * (hd / 2 + 1), hbot + csl / 2), 1.4)
        C["head"].shape = C["head"].shape - rod((hx, sy * (ri - 1), hbot + csl / 2), (hx, sy * (hd / 2 + 1), hbot + csl / 2), 1.6)
    add("cap", "Head bottom cap", cap, "head", "made")
    gland = zcyl(hx, 0, hbot - ct - 18, hbot - ct, 10.0) + zcyl(hx, 0, hbot - ct, hbot, 8.0) \
        + hexz(hx, 0, hbot, hbot + 5, 20.0)
    add("gland", "Cable gland, M16", gland, "cable", "bought")
    cscr = []
    for sy in (-1, 1):
        cscr.append(rod((hx, sy * (ri - 3.0), hbot + csl / 2), (hx, sy * (hd / 2 + 1.6), hbot + csl / 2), 1.4)
                    + rod((hx, sy * (hd / 2), hbot + csl / 2), (hx, sy * (hd / 2 + 1.6), hbot + csl / 2), 2.75))
    add("cap_screws", "M3 screws, bottom cap (2)", fuse(cscr), "head", "fixing")

    # ---------------------------------------------------------- 9 microphone, 10 processor
    mbd, mbt = p["micboard"]
    zc0 = zt - p["cavity"][1]
    mic = zcyl(hx, 0, zc0 - mbt, zc0, mbd / 2) + box(hx - 2, hx + 2, -1.5, 1.5, zc0 - mbt - 1.0, zc0 - mbt)
    for sy in (-1, 1):
        mic -= zcyl(hx, sy * 10.0, zc0 - mbt - 1, zc0 + 1, 1.1)
    add("mic", "MEMS microphone on adapter board", mic, "mic", "bought")
    gid = p["cavity"][0]
    add("gasket", "Acoustic gasket", zcyl(hx, 0, zc0, zt, 5.0) - zcyl(hx, 0, zc0 - 1, zt + 1, gid / 2), "mic", "bought")
    add("mic_screws", "M2 screws, microphone board (2)",
        fuse(zcyl(hx, sy * 10.0, zc0 - mbt - 1.0, zt + 0.8, 0.9) + zcyl(hx, sy * 10.0, zc0 - mbt - 1.0, zc0 - mbt, 1.9)
             for sy in (-1, 1)), "mic", "fixing")
    add("membrane", "Hydrophobic acoustic membrane", zcyl(hx, 0, htop, htop + 0.3, 6.0), "head", "bought")
    proc = box(hx - 0.8, hx + 0.8, -pw_ / 2, pw_ / 2, zp0, zp1) + box(hx + 0.8, hx + 4.5, -pw_ / 2 + 3, pw_ / 2 - 3, zp0 + 4, zp1 - 4) \
        + box(hx - 4.5, hx - 0.8, -pw_ / 2 + 4, pw_ / 2 - 4, zp0 + 10, zp1 - 20)
    add("proc", "Level processor board", proc, "proc", "bought")

    # ---------------------------------------------------------- 11 windscreen, spike
    wsz = D["ws_center_z"]
    bore_z0 = wsz - p["ws_d"] / 2 - 2
    ws = b.Pos(hx, 0, wsz) * b.Sphere(p["ws_d"] / 2) - zcyl(hx, 0, bore_z0, htop + 0.3, p["ws_bore"] / 2)
    ws -= zcyl(hx, -sr_, bore_z0 - 5, wsz + p["ws_d"], sd_ / 2 + 0.1)
    add("windscreen", "Foam windscreen", ws, "windscreen", "bought")
    add("spike", "Bird spike", zcyl(hx, -sr_, zr - rim - 6, htop + sl_, sd_ / 2), "windscreen", "bought")

    # ---------------------------------------------------------- 12 sensor cable
    cr = p["cable_d"] / 2
    fq = fieldnode_params(p)
    yb_f = fq["plate_y0"] - fq["plate"][2]                        # enclosure back, FieldNode frame
    pa_x = yb_f - fq["pen_rows"][1]                               # port A, world x
    pa_y = -fq["pens"]["port_a"][0]                               # port A, world y
    z0 = p["enc_z0"]
    yc = r + cr + 2.0                                             # run up the pole on its +Y side
    ys_out = sw / 2 + cr + 5.0
    yarm = ao / 2 + cr + 0.8
    pts = [(pa_x, pa_y, z0 - 22), (pa_x, pa_y, z0 - 60), (-40, pa_y + 8, z0 - 60), (-6, yc, z0 - 60),
           (0, yc, az - 80), (30, ys_out, az - 75), (D["web_out"] + 55, ys_out, az), (D["web_out"] + 72, yarm, az),
           (D["sock_x0"] - 20, yarm, az), (D["sock_x0"] + 10, 32, az - 30), (hx - 8, 10, hbot - 50),
           (hx, 0, hbot - 52), (hx, 0, hbot - p["cap"][0] - 18)]
    pts[0] = (pts[0][0], pts[0][1], z0 - 22)
    cable = path(pts, cr)
    add("cable", "Sensor cable", cable, "cable", "bought")

    # ---------------------------------------------------------- 13 safety lanyard
    ld, lz, lx = p["lanyard"]
    rl = r + ld / 2
    ring = zcyl(0, 0, az + lz - ld / 2, az + lz + ld / 2, rl + ld / 2) - zcyl(0, 0, az + lz - ld, az + lz + ld, rl - ld / 2)
    loop = xcyl(lx - ld / 2, lx + ld / 2, 0, az, ao / 2 + ld) - xcyl(lx - ld, lx + ld, 0, az, ao / 2)
    wire = rod((rl, 0, az + lz), (lx, 0, az + ao / 2 + ld / 2), ld / 2)
    add("lanyard", "Safety lanyard", ring + loop + wire, "arm", "bought")
    return C


def build_parts(p=PARAMS, C=None):
    """Return a list of (key, name, shape, colour, bom_line, explode_offset), one per BOM line with geometry."""
    from build123d import Compound
    C = C or build_components(p)
    kids = {}
    for c in C.values():
        kids.setdefault(c.group, []).append(c.shape)
    groups = {k: (v[0] if len(v) == 1 else Compound(v)) for k, v in kids.items()}
    order = ["enclosure", "board", "cell", "panel", "bracket", "plate", "arm", "head", "mic", "proc", "windscreen", "cable", "adapter"]
    return [(k, BOM[k][1], groups[k], COLOUR[k], BOM[k][0], EXPLODE[k]) for k in order]


def pole(p=PARAMS, z0=0.0, z1=5000.0):
    """Reference street pole (context only, not in the BOM)."""
    return zcyl(0, 0, z0, z1, p["pole_od"] / 2)


def assemblies(parts=None):
    from build123d import Compound
    parts = parts or build_parts()
    by = {k: s for k, _, s, _, _, _ in parts}
    return {
        "noisemap-assembly": Compound([s for _, _, s, _, _, _ in parts]),
        "noisemap-head": Compound([by[k] for k in ("arm", "head", "mic", "proc", "windscreen")]),
        "noisemap-mount": Compound([by[k] for k in ("plate", "adapter", "arm")]),
    }


def patch_svg_export():
    """Let build123d's SVG exporter skip an ellipse edge whose ends coincide after projection (a
    sloping cable or wire seen end on); otherwise svgpathtools refuses it and the drawing stops."""
    import build123d.exporters as ex
    if getattr(ex.ExportSVG, "_nsm_patched", False):
        return
    orig = ex.ExportSVG._ellipse_segments

    def safe(self, edge, reverse):
        try:
            return orig(self, edge, reverse)
        except AssertionError:
            return []
    ex.ExportSVG._ellipse_segments = safe
    ex.ExportSVG._nsm_patched = True


# ------------------------------------------------------------------ constructability checks
def _vol(a, b_):
    try:
        s = a & b_
        return 0.0 if s is None else s.volume
    except Exception:
        return 0.0


def _gap(a, b_):
    try:
        return a.distance_to(b_)
    except Exception:
        return float("nan")


def checks(p=PARAMS, C=None):
    """(description, ok, value) for every touch and clearance the build relies on."""
    C = C or build_components(p)
    D = derived(p)
    S = lambda k: C[k].shape  # noqa: E731
    pl = pole(p, 3000, 4300)
    res = []

    def chk(desc, a, b_, expect, lim=0.0):
        v = _vol(a, b_)
        g = 0.0 if v > 0.5 else _gap(a, b_)
        if expect == "touch":
            ok = v < 2.0 and g < 0.1
            res.append((desc + " (touch)", ok, f"gap {g:.2f} mm, overlap {v:.1f} mm3"))
        else:
            ok = v < 0.5 and g >= lim
            res.append((desc + f" (clear by {lim:g} mm or more)", ok, f"gap {g:.2f} mm, overlap {v:.1f} mm3"))
    # street pole adapter
    for k in ("vblock_low", "vblock_up"):
        chk(f"{k}: pole on both V faces", S(k), pl, "touch")
        chk(f"{k}: back face on the FieldNode back plate", S(k), S("fn_plate"), "touch")
        chk(f"{k}: clear of the lug screws", S(k), S("fn_lug_screws"), "clear", 0.5)
        chk(f"{k}: clear of the bracket bolts", S(k), S("fn_bracket_bolts"), "clear", 0.5)
    chk("V-block screws in the plate and blocks, clear of the pole", S("vb_screws"), pl, "clear", 5.0)
    chk("Adapter bands round the pole", S("vb_bands"), pl, "touch")
    chk("Adapter bands clear of the V-blocks' faces", S("vb_bands"), S("vblock_low") + S("vblock_up"), "touch")
    chk("Adapter bands through the plate slots, clear of the plate", S("vb_bands"), S("fn_plate"), "touch")
    chk("Adapter bands clear of the enclosure", S("vb_bands"), S("fn_body") + S("fn_lid"), "clear", 1.0)
    chk("Adapter bands clear of the lug screws", S("vb_bands"), S("fn_lug_screws"), "clear", 0.0)
    chk("Adapter bands clear of the lugs", S("vb_bands"), S("fn_lugs"), "clear", 0.5)
    chk("Adapter bands clear of the bracket", S("vb_bands"), S("fn_bracket_bolts") + S("fn_plate_clip_r") + S("fn_plate_clip_l"), "clear", 1.0)
    chk("FieldNode back plate clear of the pole", S("fn_plate"), pl, "clear", 5.0)
    chk("FieldNode panel clear of the pole", S("fn_panel"), pl, "clear", 5.0)
    chk("FieldNode panel clear of the arm saddle bands", S("fn_panel"), S("s_bands"), "clear", 20.0)
    # arm saddle
    chk("Arm saddle: pole on both V edges of each flange", S("saddle"), pl, "touch")
    chk("Arm bands round the pole", S("s_bands"), pl, "touch")
    chk("Arm bands through the web slots", S("s_bands"), S("saddle"), "touch")
    chk("Arm bands clear of the tube flange", S("s_bands"), S("flange") + S("flange_fix"), "clear", 1.0)
    chk("Tube flange flat on the web", S("flange"), S("saddle"), "touch")
    chk("Flange screws through web and flange", S("flange_fix"), S("saddle"), "touch")
    chk("Arm tube seated in the flange socket", S("tube"), S("flange"), "touch")
    chk("Arm tube seated in the head socket", S("tube"), S("head"), "touch")
    chk("Arm tube clear of the saddle web", S("tube"), S("saddle"), "clear", 1.0)
    chk("Head cross bolt through the socket", S("head_bolt"), S("head"), "touch")
    # head
    chk("Bottom cap in the head", S("cap"), S("head"), "touch")
    chk("Cable gland in the cap", S("gland"), S("cap"), "touch")
    chk("Processor board in its card guides", S("proc"), S("head"), "touch")
    chk("Processor board clear of the cap and gland", S("proc"), S("cap") + S("gland"), "clear", 5.0)
    chk("Microphone board on its bosses", S("mic"), S("head"), "touch")
    chk("Gasket between microphone board and top plate", S("gasket"), S("head"), "touch")
    chk("Gasket on the microphone board", S("gasket"), S("mic"), "touch")
    chk("Microphone board clear of the processor board", S("mic"), S("proc"), "clear", 3.0)
    chk("Windscreen on the head", S("windscreen"), S("head") + S("membrane"), "touch")
    chk("Spike in its boss", S("spike"), S("head"), "touch")
    chk("Spike clear of the head tube", S("spike"), zcyl(D["head_x"], 0, D["head_bot"], D["head_top"], p["head"][0] / 2), "clear", 1.0)
    # cable and lanyard
    cab = S("cable")
    chk("Cable into the gland", cab, S("gland"), "touch")
    for k, lim in (("fn_body", 1.0), ("fn_plate", 1.0), ("vblock_low", 1.0), ("vblock_up", 1.0), ("vb_bands", 0.0),
                   ("saddle", 2.0), ("s_bands", 0.0), ("flange", 2.0), ("flange_fix", 1.0), ("tube", 0.3), ("head", 2.0),
                   ("head_bolt", 2.0), ("lanyard", 0.5), ("fn_antenna", 3.0)):
        chk(f"Cable clear of {C[k].name.lower()}", cab, S(k), "clear", lim)
    chk("Cable clear of the pole", cab, pl, "clear", 0.0)
    chk("Lanyard round the pole", S("lanyard"), pl, "touch")
    chk("Lanyard round the arm", S("lanyard"), S("tube"), "touch")
    chk("Lanyard clear of the saddle and flange", S("lanyard"), S("saddle") + S("flange") + S("flange_fix"), "clear", 3.0)
    # nothing in the NoiseMap parts overlaps anything else (contacts aside)
    keys = [k for k in C if not k.startswith("fn_")]
    worst = []
    for i, a in enumerate(keys):
        for b_ in keys[i + 1:]:
            v = _vol(S(a), S(b_))
            if v > 2.0:
                worst.append(f"{a}/{b_} {v:.0f}")
    res.append(("No NoiseMap part overlaps another", not worst, "; ".join(worst) or "none"))
    # pole range
    for d in p["pole_range"]:
        t = D["contact"][d]
        res.append((f"{d:.0f} mm pole: V contacts {t:.1f} mm each side, inside the V-block mouth ({D['v_half_mouth']:.1f}) "
                    f"and the saddle mouth ({D['s_half_mouth']:.1f}) by 3 mm or more",
                    t <= D["v_half_mouth"] - 3 and t <= D["s_half_mouth"] - 3, f"largest pole {min(D['max_pole_vb'], D['max_pole_saddle']):.0f} mm"))
    return res


def print_checks(p=PARAMS, C=None):
    res = checks(p, C)
    n_ok = sum(1 for _, ok, _ in res if ok)
    for desc, ok, val in res:
        print(f"  [{'ok' if ok else 'FAIL'}] {desc}: {val}")
    print(f"constructability checks: {n_ok} of {len(res)} pass")
    return n_ok == len(res)


if __name__ == "__main__":
    C = build_components()
    if "--check" not in sys.argv:
        from build123d import export_step, export_stl
        root = Path(__file__).resolve().parents[1]
        (root / "step").mkdir(exist_ok=True); (root / "stl").mkdir(exist_ok=True)
        parts = build_parts(C=C)
        for name, shape in assemblies(parts).items():
            export_step(shape, str(root / "step" / f"{name}.step"))
            export_stl(shape, str(root / "stl" / f"{name}.stl"), tolerance=0.2, angular_tolerance=0.3)
            bb = shape.bounding_box()
            print(f"{name:20s} {bb.size.X:7.1f} x {bb.size.Y:7.1f} x {bb.size.Z:7.1f} mm")
        for k, n, s, _, bom, _ in parts:
            print(f"  {bom:2d} {n:40s} volume {s.volume / 1e3:8.1f} cm3")
    print_checks(C=C)
