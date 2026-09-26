"""NoiseMap parametric model (build123d), TRL 3, massing-plus level of detail.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl:
    noisemap-assembly.step / .stl   the whole node (FieldNode core, street pole adapter, arm, head)
    noisemap-head.step / .stl       microphone arm, head housing, microphone, processor, windscreen
    noisemap-mount.step / .stl      FieldNode back plate, street pole adapter V-blocks and bands, arm saddle

Axes: the street pole is the Z axis (x = y = 0), Z is up with the sidewalk surface at z = 0,
and the street is toward +X. The FieldNode core hangs on the back (-X) of the pole with its
panel facing -X; the microphone arm has its own band clamp and points +X at the street. On
site the core turns about the pole to face the equator and the arm turns to face the street;
the two are independent. Main dimensions and interfaces only: FieldNode core envelope as in
FND-DWG-001 (enclosure 150 x 90 x 200 mm, 6 W panel at 40 deg, 180 x 320 x 3 mm back plate),
the street pole adapter for 60 to 140 mm poles, the arm, the head with its acoustic port, the
microphone position and the windscreen. Not fabrication detail; not for fabrication.
The same PARAMS feed docs/04-calcs/sizing.py (NSM-CAL-001), the drawing NSM-DWG-001
(cad/src/sheets.py) and the concept media (cad/src/concept_media.py).
"""
import math
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # site: street pole on the Z axis (design case 114.3 mm OD, 4.5 in), range the adapter must seat
    "pole_od": 114.3, "pole_range": (60.0, 140.0),
    # microphone: port 4.0 m above the sidewalk (EU strategic noise map height), 0.45 m from the pole face
    "mic_z": 4000.0, "mic_off": 450.0,
    # 14 street pole adapter: 90 deg V-blocks (face width, depth along X, height), V notch width at the face
    "vb": (110.0, 60.0, 40.0), "vnotch_w": 100.0, "band_w": 12.0, "band_t": 0.8,
    # FieldNode core (FND-DWG-001): enclosure W (Y) x D (X) x H (Z), bottom height, back plate W x H x t
    "enc": (150.0, 90.0, 200.0), "enc_wall": 3.0, "enc_z0": 3300.0,
    "plate": (180.0, 320.0, 3.0), "plate_drop": 40.0, "clamp_dz": (-20.0, 230.0),
    # 4 panel (Y x slope x t), tilt, center (distance in front of the enclosure back, height above enc_z0)
    "panel": (290.0, 200.0, 17.0), "tilt": 40.0, "panel_c": (70.0, 385.0),
    "whip": (10.0, 190.0), "port_y": (-52.0, -22.0), "m12_d": (16.0, 22.0),
    # 7 arm: aluminium tube OD x wall; saddle plate (X x Y x Z); arm axis below the microphone port
    "arm": (25.0, 2.0), "saddle": (10.0, 60.0, 90.0), "arm_drop": 120.0,
    # 8 head housing: printed ASA tube OD x wall x height, top plate thickness, drip skirt OD x thickness
    "head": (40.0, 3.0, 150.0), "top_t": 2.0, "skirt": (64.0, 4.0), "skirt_dz": 60.0,
    # acoustic path: port in the top plate (diameter), microphone front cavity (diameter x height)
    "port_d": 3.0, "cavity": (3.0, 0.5),
    # 9 microphone adapter board (diameter x t); 10 level processor board (W x D x H)
    "micboard": (30.0, 1.6), "proc": (26.0, 10.0, 70.0),
    # 11 foam windscreen (diameter), bore for the head, bird spike (length, diameter)
    "ws_d": 90.0, "ws_bore": 41.0, "ws_dz": 5.0, "spike": (110.0, 3.0),
    # 12 sensor cable
    "cable_d": 7.0,
}

BOM = {  # model key: (BOM line, name)
    "enclosure": (1, "FieldNode enclosure, IP65"),
    "board": (2, "FieldNode power and radio board"),
    "cell": (3, "LiFePO4 cell, 6 Ah"),
    "panel": (4, "Solar panel, 6 W"),
    "bracket": (5, "Panel tilt bracket"),
    "plate": (6, "FieldNode back plate"),
    "arm": (7, "Microphone arm and saddle clamp"),
    "head": (8, "Microphone head housing, ASA"),
    "mic": (9, "MEMS microphone on adapter board"),
    "proc": (10, "Level processor board"),
    "windscreen": (11, "Foam windscreen and bird spike"),
    "cable": (12, "Sensor cable, M12"),
    "adapter": (14, "Street pole adapter, V-blocks and bands"),
}


def derived(p=PARAMS):
    """Dimensions the calc note and the drawing quote, computed from PARAMS."""
    r = p["pole_od"] / 2
    vw, vd, vh = p["vb"]
    notch_depth = p["vnotch_w"] / 2                       # 90 deg V: depth equals half width
    apex = -r * math.sqrt(2)                              # V apex x for the design pole (pole touches both faces)
    plate_front = apex - (vd - notch_depth)               # face of the back plate toward the pole
    plate_back = plate_front - p["plate"][2]
    enc_back = plate_back
    enc_front = enc_back - p["enc"][1]
    head_x = r + p["mic_off"]
    hd, hw, hh = p["head"]
    head_top = p["mic_z"]
    head_bot = head_top - hh
    arm_z = head_top - p["arm_drop"]
    arm_x0 = r + p["saddle"][0]
    t = math.radians(p["tilt"])
    pcx = enc_back - p["panel_c"][0]
    pcz = p["enc_z0"] + p["panel_c"][1]
    half = p["panel"][1] / 2
    # contact half-offset for poles across the range: t = R / sqrt(2) along each V face from the apex
    contact = {d: (d / 2) / math.sqrt(2) for d in p["pole_range"]}
    return {
        "r": r, "apex": apex, "plate_front": plate_front, "plate_back": plate_back,
        "enc_back": enc_back, "enc_front": enc_front, "enc_top": p["enc_z0"] + p["enc"][2],
        "head_x": head_x, "head_top": head_top, "head_bot": head_bot, "arm_z": arm_z,
        "arm_x0": arm_x0, "arm_len": head_x - hd / 2 + 2 - arm_x0,
        "panel_cx": pcx, "panel_cz": pcz,
        "panel_low": (pcx - half * math.cos(t), pcz - half * math.sin(t)),
        "panel_high": (pcx + half * math.cos(t), pcz + half * math.sin(t)),
        "notch_depth": notch_depth, "contact": contact,
        "reach_max_pole": 2 * notch_depth / math.sqrt(2) * 2,   # largest pole whose contacts stay on the faces
        "ws_center_z": head_top + p["ws_dz"],
        "overall_x": (enc_front - 0.0, head_x + p["ws_d"] / 2),
    }


def _box(x0, x1, y0, y1, z0, z1):
    from build123d import Box, Pos
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _tube(a, b, r):
    from build123d import Solid, Plane, Vector
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def _band(z, r_in, w, t):
    from build123d import Cylinder, Pos
    return Pos(0, 0, z) * (Cylinder(r_in + t, w) - Cylinder(r_in, w + 2))


def build_parts(p=PARAMS):
    """Return a list of (key, name, shape, colour, bom_line, explode_offset)."""
    from build123d import Box, Cylinder, Sphere, Pos, Rot
    d = derived(p)
    r = d["r"]
    b = _box
    ew, ed, eh = p["enc"]
    z0 = p["enc_z0"]

    # 1 FieldNode enclosure (hollow box, lid seam implied), back against the back plate
    x0, x1 = d["enc_front"], d["enc_back"]
    wt = p["enc_wall"]
    enclosure = b(x0, x1, -ew / 2, ew / 2, z0, z0 + eh) - b(x0 + wt, x1 - wt, -ew / 2 + wt, ew / 2 - wt, z0 + wt, z0 + eh - wt)
    # M12 ports on the bottom face (FieldNode D5); the sensor cable uses the first
    ports = None
    for y in p["port_y"]:
        s = Pos((x0 + x1) / 2, y, z0 - 9) * Cylinder(p["m12_d"][1] / 2, 18)
        ports = s if ports is None else ports + s
    enclosure = enclosure + ports

    # 2 FieldNode power and radio board with the whip antenna below the enclosure
    board = b(x1 - wt - 14, x1 - wt - 4, -60, 60, z0 + 60, z0 + 180)
    whip_d, whip_l = p["whip"]
    antenna = Pos((x0 + x1) / 2, 58, z0 - whip_l / 2) * Cylinder(whip_d / 2, whip_l)
    board = board + antenna

    # 3 LiFePO4 32700 cell lying in the base of the enclosure
    cell = Pos((x0 + x1) / 2 - 5, 0, z0 + 40) * Rot(90, 0, 0) * Cylinder(16, 70)

    # 4 6 W panel, facing -X, tilted 40 deg, low edge toward -X
    pw, pl, pt = p["panel"]
    panel = Pos(d["panel_cx"], 0, d["panel_cz"]) * Rot(0, -p["tilt"], 0) * Box(pl, pw, pt)

    # 5 bracket: two rear posts from the back plate and two front struts from the lid to the panel underside
    t = math.radians(p["tilt"])
    def under(u, y):
        return (d["panel_cx"] + u * math.cos(t) + pt / 2 * math.sin(t) + 0, y,
                d["panel_cz"] + u * math.sin(t) - pt / 2 * math.cos(t) - 1)
    top = z0 + eh
    bracket = None
    for y in (-110, 110):
        for foot, u in (((x1 - 6, y, top + 60), 80.0), ((x0 + 12, y, top), -60.0)):
            s_ = _tube(foot, under(u, y), 5)
            bracket = s_ if bracket is None else bracket + s_

    # 6 FieldNode back plate
    plw, plh, plt = p["plate"]
    plate = b(d["plate_back"], d["plate_front"], -plw / 2, plw / 2, z0 - p["plate_drop"], z0 - p["plate_drop"] + plh)

    # 14 street pole adapter: two 90 deg V-blocks on the plate and two stainless bands round the pole
    vw, vd, vh = p["vb"]
    adapter = None
    for dz in p["clamp_dz"]:
        zc = z0 + dz + p["band_w"] / 2
        blk = b(d["plate_front"], d["plate_front"] + vd, -vw / 2, vw / 2, zc - vh / 2, zc + vh / 2)
        notch = Pos(d["apex"], 0, zc) * Rot(0, 0, 45) * Box(200, 200, vh + 2)
        blk = blk - (notch & b(d["apex"], d["apex"] + 300, -300, 300, zc - vh, zc + vh))
        band = _band(zc - p["band_w"] / 2, r, p["band_w"], p["band_t"])
        band = band - b(-300, d["plate_front"], -vw / 2, vw / 2, zc - 20, zc + 20)
        tails = b(d["plate_front"] + 2, d["plate_front"] + vd, -vw / 2 - 6, -vw / 2 - 1, zc - 6, zc + 6) \
            + b(d["plate_front"] + 2, d["plate_front"] + vd, vw / 2 + 1, vw / 2 + 6, zc - 6, zc + 6)
        part = blk + band + tails
        adapter = part if adapter is None else adapter + part

    # 7 microphone arm: saddle plate on the street side of the pole, own band, tube to the head collar
    sx, sy, sz = p["saddle"]
    az = d["arm_z"]
    ao, awall = p["arm"]
    saddle = b(r, r + sx, -sy / 2, sy / 2, az - sz / 2, az + sz / 2)
    arm_band = _band(az - p["band_w"] / 2, r, p["band_w"], p["band_t"]) - b(r - 1, 400, -sy / 2, sy / 2, az - 20, az + 20)
    hx = d["head_x"]
    hd, hwall, hh = p["head"]
    tube = _tube((r + sx, 0, az), (hx - hd / 2 - 0.3, 0, az), ao / 2) - _tube((r + sx - 1, 0, az), (hx - hd / 2 + 2, 0, az), ao / 2 - awall)
    collar = Pos(hx, 0, az) * (Cylinder(hd / 2 + 4, 40) - Cylinder(hd / 2 + 0.2, 42))
    arm = saddle + arm_band + tube + collar

    # 8 head housing: tube with a top plate carrying the acoustic port, and a drip skirt
    htop, hbot = d["head_top"], d["head_bot"]
    head = Pos(hx, 0, (htop + hbot) / 2) * (Cylinder(hd / 2, hh) - Pos(0, 0, -p["top_t"] / 2 - 1) * Cylinder(hd / 2 - hwall, hh - p["top_t"] + 2))
    head = head - Pos(hx, 0, htop - p["top_t"] / 2) * Cylinder(p["port_d"] / 2, p["top_t"] + 2)
    so, st = p["skirt"]
    head = head + Pos(hx, 0, htop - p["skirt_dz"]) * (Cylinder(so / 2, st) - Cylinder(hd / 2 - 0.5, st + 2))

    # 9 microphone on its adapter board, bottom port under the head's acoustic port
    mbd, mbt = p["micboard"]
    cav_h = p["cavity"][1]
    mic = (Pos(hx, 0, htop - p["top_t"] - cav_h - mbt / 2) * Cylinder(mbd / 2 - 1, mbt)
           + Pos(hx, 0, htop - p["top_t"] - cav_h - mbt - 0.5) * Box(4.0, 3.0, 1.0))

    # 10 level processor board standing in the tube
    pw_, pd_, ph_ = p["proc"]
    proc = b(hx - pd_ / 2, hx + pd_ / 2, -pw_ / 2, pw_ / 2, htop - p["top_t"] - 12 - ph_, htop - p["top_t"] - 12)

    # 11 foam windscreen bored over the head, and the bird spike
    wsz = d["ws_center_z"]
    bore_z0 = wsz - p["ws_d"] / 2 - 2
    windscreen = Pos(hx, 0, wsz) * Sphere(p["ws_d"] / 2) - Pos(hx, 0, (bore_z0 + htop + 0.5) / 2) * Cylinder(p["ws_bore"] / 2, htop + 0.5 - bore_z0)
    sl, sd = p["spike"]
    windscreen = windscreen + _tube((hx, 0, wsz + p["ws_d"] / 2 - 5), (hx, 0, wsz + p["ws_d"] / 2 + sl), sd / 2)

    # 12 sensor cable: FieldNode bottom port, round the pole, along under the arm, into the head base
    pxm = (x0 + x1) / 2
    cr = p["cable_d"] / 2
    pts = [(pxm, p["port_y"][0], z0 - 20), (pxm, p["port_y"][0], z0 - 60), (-r - 12, -r - 12, z0 - 60),
           (-r - 12, -r - 12, az - 70), (0, -r - 16, az - 55), (r + 20, -r + 10, az - 40), (hx - 30, -12, az - 25),
           (hx, -12, hbot - 12), (hx, 0, hbot - 6)]
    cable = None
    for a_, b_ in zip(pts[:-1], pts[1:]):
        s = _tube(a_, b_, cr)
        cable = s if cable is None else cable + s

    return [
        ("enclosure", BOM["enclosure"][1], enclosure, "#E5E7EB", 1, (-300, 0, 0)),
        ("board", BOM["board"][1], board, "#16A34A", 2, (-620, 0, 60)),
        ("cell", BOM["cell"][1], cell, "#C2410C", 3, (-480, 0, -260)),
        ("panel", BOM["panel"][1], panel, "#1E3A8A", 4, (-200, 0, 420)),
        ("bracket", BOM["bracket"][1], bracket, "#6B7280", 5, (-150, 0, 200)),
        ("plate", BOM["plate"][1], plate, "#94A3B8", 6, (-120, 0, 0)),
        ("arm", BOM["arm"][1], arm, "#A16207", 7, (60, 0, -80)),
        ("head", BOM["head"][1], head, "#0F766E", 8, (300, 0, 0)),
        ("mic", BOM["mic"][1], mic, "#7C3AED", 9, (300, 0, 150)),
        ("proc", BOM["proc"][1], proc, "#2563EB", 10, (560, 0, 40)),
        ("windscreen", BOM["windscreen"][1], windscreen, "#374151", 11, (300, 0, 480)),
        ("cable", BOM["cable"][1], cable, "#111827", 12, (150, -450, -350)),
        ("adapter", BOM["adapter"][1], adapter, "#78716C", 14, (0, 320, -120)),
    ]


def _ivol(a, b):
    """Volume of the intersection of two shapes (0 when they do not meet)."""
    try:
        s = a & b
        return 0.0 if s is None else s.volume
    except Exception:
        return 0.0


def pole(p=PARAMS, z0=0.0, z1=5000.0):
    """Reference street pole (context only, not in the BOM)."""
    from build123d import Cylinder, Pos
    return Pos(0, 0, (z0 + z1) / 2) * Cylinder(p["pole_od"] / 2, z1 - z0)


def assemblies(parts=None):
    from build123d import Compound
    parts = parts or build_parts()
    by = {k: s for k, _, s, _, _, _ in parts}
    return {
        "noisemap-assembly": Compound([s for _, _, s, _, _, _ in parts]),
        "noisemap-head": Compound([by[k] for k in ("arm", "head", "mic", "proc", "windscreen")]),
        "noisemap-mount": Compound([by[k] for k in ("plate", "adapter", "arm")]),
    }


if __name__ == "__main__":
    from build123d import export_step, export_stl
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True); (root / "stl").mkdir(exist_ok=True)
    parts = build_parts()
    for name, shape in assemblies(parts).items():
        export_step(shape, str(root / "step" / f"{name}.step"))
        export_stl(shape, str(root / "stl" / f"{name}.stl"))
        bb = shape.bounding_box()
        print(f"{name:20s} {bb.size.X:7.1f} x {bb.size.Y:7.1f} x {bb.size.Z:7.1f} mm")
    for k, n, s, _, bom, _ in parts:
        print(f"  {bom:2d} {n:40s} volume {s.volume / 1e3:8.1f} cm3")
    # Clash check between parts that must not touch (arm, head and cable pass close to the pole)
    pl = pole()
    worst = 0.0
    for k, n, s, _, _, _ in parts:
        v = _ivol(s, pl)
        if v > 1.0:
            print(f"clash with pole: {n}: {v:.0f} mm3"); worst = max(worst, v)
    for i in range(len(parts)):
        for j in range(i + 1, len(parts)):
            v = _ivol(parts[i][2], parts[j][2])
            if v > 200.0:   # contacts under 200 mm3 are attachment points (bracket ends, cable entry)
                print(f"clash {parts[i][1]} / {parts[j][1]}: {v:.0f} mm3"); worst = max(worst, v)
    print("clash check: none" if worst == 0 else "clash check: see above")
