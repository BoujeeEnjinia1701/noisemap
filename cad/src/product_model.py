"""NoiseMap product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: the FieldNode core (light grey IP65 enclosure with a
lid, parting line, lid screws, side ribs, a lit green status light and a lid label saying the node
records sound levels only), its 6 W solar panel with an aluminium frame and cell grid on the tilt
bracket, the back plate and street pole adapter with band clamp bolts, the M12 ports with the
sensor cable plug and the whip antenna; and on the street side the aluminium arm with its saddle,
band and collar, the printed ASA microphone head with a teal accent ring and grip grooves, the
foam windscreen and the bird spike. Inside: the power and radio board, the LiFePO4 cell in its
cradle, the microphone adapter board and the level processor. Context is a short section of
street pole (114.3 mm design case).
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension, height and interface comes from PARAMS, derived() and build_parts() in
model.py (same axes: pole on the Z axis, sidewalk at Z = 0, street toward +X). The back plate,
adapter, bracket, arm, head, gland, lugs and fixings reuse the model.py solids unchanged (constructable
design, NSM-DDR-003); the plate, V-blocks and arm saddle are no longer the concept shapes.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build123d import (Align, Axis, Box, Cylinder, Plane, Pos, RegularPolygon, Rot, Solid, Sphere, Text,
                       Vector, extrude, fillet)
from model import PARAMS, derived, build_parts, build_components

_FONT = Path(__file__).resolve().parents[2] / ".kit" / "fonts" / "IBMPlexSans-SemiBold.ttf"

TITLE = "NoiseMap: street pole sound level meter that records decibels only, never audio"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 22, "az": -140,
     "note": "Product render from the front left and above (about 22 deg elevation), looking at the "
             "sidewalk side of the pole: solar panel and FieldNode core with its levels-only label at "
             "left, microphone arm reaching toward the street with the foam windscreen at right"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 24, "az": -130,
     "note": "Exploded view from the front left and above (about 24 deg elevation): enclosure body and lid, "
             "power and radio board, LiFePO4 cell, solar panel and bracket, back plate and pole adapter; "
             "arm, microphone head, microphone board, level processor, windscreen and sensor cable"},
    {"name": "detail", "groups": ["shell", "internal"], "explode": False, "el": 18, "az": -150,
     "note": "Detail from the front left, slightly above (about 18 deg elevation), without the pole: "
             "FieldNode core with the levels-only label and the lit status light, microphone head "
             "and windscreen at right"},
]

# Colours (restrained product palette; kit accent)
C_SHELL = "#DADDE1"      # light grey polycarbonate
C_LID = "#E6E8EB"
C_DARK = "#2B2F36"
C_BLACK = "#1C1F24"
C_ACCENT = "#0F766E"
C_ALU = "#C3C8CE"
C_ALU2 = "#AEB4BB"
C_STEEL = "#9CA3AB"
C_CELLS = "#1B2735"
C_GRID = "#C9CDD3"
C_PCB = "#166534"
C_CHIP = "#111827"
C_CELL = "#2F4F6F"
C_HEAD = "#ECECEA"       # printed ASA, off-white
C_FOAM = "#3A3F45"
C_LABEL = "#F4F4F2"
C_LED_G = "#22C55E"
C_POLE = "#B9BEC4"

POLE_Z = (3080.0, 4210.0)   # context pole section, just enough to carry the node


def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _box(cx, cy, cz, sx, sy, sz):
    return Pos(cx, cy, cz) * Box(sx, sy, sz)


def _bx(x0, x1, y0, y1, z0, z1):
    return _box((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2, x1 - x0, y1 - y0, z1 - z0)


def _zcyl(x, y, z, r, h):
    return Pos(x, y, z) * Cylinder(r, h)


def _ycyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, h)


def _xcyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(0, 90, 0) * Cylinder(r, h)


def _pipe(points, r):
    """Round tube through `points` with spherical joints (clean bends)."""
    out = None
    for a, c in zip(points, points[1:]):
        a, c = Vector(*a), Vector(*c)
        d = c - a
        seg = Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))
        out = seg if out is None else out + seg
    for q in points[1:-1]:
        out += Pos(*q) * Sphere(r)
    return out


def _hex_z(x, y, z, af, h):
    return Pos(x, y, z - h / 2) * extrude(RegularPolygon(af / 1.732, 6), amount=h)


def _hex_y(x, y, z, af, h):
    return Pos(x, y - h / 2, z) * extrude(Plane.XZ * RegularPolygon(af / 1.732, 6), amount=-h)


def _hex_x(x, y, z, af, h):
    return Pos(x - h / 2, y, z) * extrude(Plane.YZ * RegularPolygon(af / 1.732, 6), amount=h)


def _faces_min(s, axis):
    return s.faces().sort_by(axis)[0].edges()


def _faces_max(s, axis):
    return s.faces().sort_by(axis)[-1].edges()


def _text_nx(txt, size, x, y, z, h=0.3):
    """Raised text on a face that looks toward -X (reads correctly from -X), centred on (y, z)."""
    t = extrude(Text(txt, font_size=size, font_path=str(_FONT), align=(Align.CENTER, Align.CENTER)), amount=h)
    pl = Plane(origin=(x, y, z), x_dir=(0, -1, 0), z_dir=(-1, 0, 0))
    return pl * t


def _text_nz(txt, size, x, y, z, h=0.3):
    """Raised text on a face that looks down (-Z), centred on (x, y)."""
    t = extrude(Text(txt, font_size=size, font_path=str(_FONT), align=(Align.CENTER, Align.CENTER)), amount=h)
    pl = Plane(origin=(x, y, z), x_dir=(0, 1, 0), z_dir=(0, 0, -1))
    return pl * t


def product_parts(P=PARAMS):
    D = derived(P)
    Cm = build_components(P)
    model = {k: s for k, _, s, _, _, _ in build_parts(P)}
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    r = D["r"]
    ew, ed, eh = P["enc"]
    z0 = P["enc_z0"]
    x0, x1 = D["enc_front"], D["enc_back"]          # -X front (lid) and back against the plate
    wt = P["enc_wall"]
    xm = (x0 + x1) / 2
    zc_enc = z0 + eh / 2

    # ------------------------------------------------------------ FieldNode core
    E_BODY, E_LID = (-140, 0, 0), (-430, 0, 0)
    E_BOARD, E_CELL = (-290, 0, 60), (-290, 0, -150)

    outer = _bx(x0, x1, -ew / 2, ew / 2, z0, z0 + eh)
    outer = _fillet_try(outer, outer.edges().filter_by(Axis.X), [9.0, 7.0, 5.0])
    outer = _fillet_try(outer, _faces_min(outer, Axis.X), [3.0, 2.0, 1.0])
    lid_t = 22.0
    xs = x0 + lid_t                                   # parting line
    body = outer & _bx(xs + 0.3, x1 + 1, -200, 200, z0 - 10, z0 + eh + 10)
    body -= _bx(xs, x1 - wt, -ew / 2 + wt, ew / 2 - wt, z0 + wt, z0 + eh - wt)
    for sy in (-1, 1):                                # vertical side ribs (texture)
        for k in range(5):
            body -= _box(xs + 14 + 10 * k, sy * ew / 2, zc_enc, 3.0, 1.6, eh - 50)
    # M12 port bosses on the bottom face (model.py ports), threaded bodies
    for y in P["port_y"]:
        body += _zcyl(xm, y, z0 - 4.0, 8.0, 8.0)
    add("Enclosure body (IP65 polycarbonate)", body, C_SHELL, "plastic", 1, "shell", E_BODY)

    lid = outer & _bx(x0 - 1, xs - 0.3, -200, 200, z0 - 10, z0 + eh + 10)
    lid -= _bx(x0 + wt, xs, -ew / 2 + wt, ew / 2 - wt, z0 + wt, z0 + eh - wt)
    add("Enclosure lid", lid, C_LID, "plastic", 1, "shell", E_LID)

    gasket = (_bx(xs - 0.3, xs + 0.3, -ew / 2 + 1.0, ew / 2 - 1.0, z0 + 1.0, z0 + eh - 1.0)
              - _bx(xs - 1, xs + 1, -ew / 2 + wt, ew / 2 - wt, z0 + wt, z0 + eh - wt))
    add("Lid gasket (seen at the parting line)", gasket, C_DARK, "rubber", 1, "shell", (-285, 0, 0))

    scr = None
    for sy in (-1, 1):
        for sz in (-1, 1):
            y, z = sy * (ew / 2 - 11), zc_enc + sz * (eh / 2 - 11)
            s = _xcyl(x0 - 0.6, y, z, 3.4, 1.2)
            s = _fillet_try(s, _faces_min(s, Axis.X), [0.5, 0.3])
            s -= _box(x0 - 1.2, y, z, 1.0, 4.0, 0.8)
            scr = s if scr is None else scr + s
    add("Lid screws", scr, C_STEEL, "metal", 1, "shell", (-470, 0, 0))

    # lid label: records levels only (thin raised parts)
    lx = x0 - 0.2
    lz = zc_enc + 22
    add("Lid label", _box(lx, 0, lz, 0.4, 108, 74), C_LABEL, "paper", 1, "shell", (-450, 0, 0))
    add("Lid label accent band", _box(lx - 0.3, 0, lz + 30, 0.3, 108, 14), C_ACCENT, "painted", 1, "shell",
        (-450, 0, 0))
    ink = _text_nx("NoiseMap", 12.0, lx - 0.2, 0, lz + 10)
    ink += _text_nx("RECORDS SOUND LEVELS ONLY", 6.2, lx - 0.2, 0, lz - 8)
    ink += _text_nx("NO AUDIO IS STORED OR SENT", 5.2, lx - 0.2, 0, lz - 20)
    add("Lid label print", ink, C_DARK, "paper", 1, "shell", (-450, 0, 0))
    wtxt = _text_nx("dB ONLY", 7.0, lx - 0.4, 0, lz + 30, h=0.2)
    add("Lid label band text", wtxt, C_LABEL, "paper", 1, "shell", (-450, 0, 0))

    # status light on the lid (lit)
    ly_, lz_ = ew / 2 - 22, z0 + 26
    bez = _xcyl(x0 - 1.0, ly_, lz_, 4.5, 2.0) - _xcyl(x0 - 1.0, ly_, lz_, 2.6, 3.0)
    add("Status light bezel", bez, C_BLACK, "plastic", 2, "shell", E_LID)
    dome = Pos(x0 + 0.2, ly_, lz_) * Sphere(3.0) & _bx(x0 - 3.1, x0, ly_ - 5, ly_ + 5, lz_ - 5, lz_ + 5)
    add("Status light, green (lit)", dome, C_LED_G, "emissive", 2, "shell", E_LID)

    # M12 ports: hex nuts, sensor cable plug on the first, dust cap on the second (BOM 2, 12)
    nuts = None
    for y in P["port_y"]:
        n = _hex_z(xm, y, z0 - 9.5, 20.0, 3.0)
        nuts = n if nuts is None else nuts + n
    add("M12 port nuts", nuts, C_STEEL, "metal", 2, "shell", E_BODY)
    py0, py1 = P["port_y"]
    plug = _zcyl(xm, py0, z0 - 26.0, 9.5, 24.0)
    plug = _fillet_try(plug, _faces_min(plug, Axis.Z), [2.0, 1.0])
    for k in range(12):
        a = 2 * math.pi * k / 12
        plug -= Pos(xm + 9.5 * math.cos(a), py0 + 9.5 * math.sin(a), z0 - 19.0) * Box(1.2, 1.2, 10.0)
    add("Sensor cable plug (M12, knurled)", plug, C_BLACK, "rubber", 12, "shell", E_BODY)
    cap = _zcyl(xm, py1, z0 - 17.0, 9.0, 12.0)
    cap = _fillet_try(cap, _faces_min(cap, Axis.Z), [2.0, 1.0])
    add("Spare M12 port dust cap", cap, C_DARK, "rubber", 2, "shell", E_BODY)
    # port A rail-voltage label on the bottom face beside the port (decision of 2026-10-02: NoiseMap's port is 3.3 V)
    lab_x = xm + 28.0
    add("Port A label plate", _bx(lab_x - 13, lab_x + 13, py0 - 10, py0 + 10, z0 - 0.4, z0), C_LABEL, "paper", 2, "shell", E_BODY)
    add("Port A label print (3.3 V)", _text_nz("A  3.3 V", 6.0, lab_x, py0, z0 - 0.4), C_DARK, "paper", 2, "shell", E_BODY)
    # enclosure lugs, glands and fixings as built (FieldNode BOM lines 1 and 2, model.py)
    add("Enclosure lugs (4) and M5 screws", Cm["fn_lugs"].shape + Cm["fn_lug_screws"].shape, C_ALU2, "metal", 1, "shell", E_BODY)
    add("Enclosure cable glands (2 x M16)", Cm["fn_glands"].shape, C_DARK, "plastic", 1, "shell", E_BODY)
    vent = _hex_z(xm - 22, 20, z0 - 1.5, 12.0, 3.0) + (Pos(xm - 22, 20, z0 - 3.0) * Sphere(5.0)
                                                         & _bx(xm - 30, xm - 14, 12, 28, z0 - 9, z0 - 3))
    add("Enclosure vent (ePTFE)", vent, C_ALU2, "plastic", 1, "shell", E_BODY)

    # whip antenna below the enclosure (model.py position and length)
    wd, wl = P["whip"]
    ay = 58.0
    ant = _hex_z(xm, ay, z0 - 3.0, 12.0, 6.0) + _zcyl(xm, ay, z0 - 14.0, 5.5, 16.0)
    whip = _zcyl(xm, ay, z0 - 22 - (wl - 22) / 2, wd / 2, wl - 22)
    whip = _fillet_try(whip, _faces_min(whip, Axis.Z), [4.0, 2.5])
    add("Antenna base", ant, C_STEEL, "metal", 2, "shell", E_BODY)
    add("Whip antenna (sub-GHz)", whip, C_BLACK, "rubber", 2, "shell", E_BODY)

    # power and radio board (BOM 2), inside against the back wall, as model.py
    bx1 = x1 - wt - 4
    pcb = _bx(bx1 - 1.6, bx1, -60, 60, z0 + 60, z0 + 180)
    add("Power and radio board PCB", pcb, C_PCB, "plastic", 2, "internal", E_BOARD)
    mod = _bx(bx1 - 5.0, bx1 - 1.6, -45, -5, z0 + 120, z0 + 170)
    add("LoRaWAN module", mod, C_CHIP, "plastic", 2, "internal", E_BOARD)
    can = _bx(bx1 - 6.0, bx1 - 5.0, -42, -8, z0 + 124, z0 + 166)
    add("LoRaWAN module shield can", can, C_ALU, "metal", 2, "internal", E_BOARD)
    comps = (_bx(bx1 - 3.0, bx1 - 1.6, 10, 22, z0 + 140, z0 + 152) + _bx(bx1 - 2.5, bx1 - 1.6, 30, 42, z0 + 150, z0 + 158)
             + _bx(bx1 - 8.0, bx1 - 1.6, 12, 40, z0 + 80, z0 + 100) + _bx(bx1 - 12, bx1 - 1.6, -50, -20, z0 + 66, z0 + 80))
    comps += _xcyl(bx1 - 7.6, -2, z0 + 95, 4.0, 12.0)
    add("Board components", comps, C_CHIP, "plastic", 2, "internal", E_BOARD)
    add("Board terminal block", _bx(bx1 - 10, bx1 - 1.6, -20, 20, z0 + 62, z0 + 72), "#2E7D5B", "plastic", 2,
        "internal", E_BOARD)

    # LiFePO4 cell in its cradle (BOM 3), model.py position
    cx_, cz_ = xm - 5, z0 + 40
    cell = _ycyl(cx_, 0, cz_, 16.0, 66.0)
    cell = _fillet_try(cell, cell.edges(), [2.0, 1.0])
    add("LiFePO4 cell (32700, 6 Ah)", cell, C_CELL, "plastic", 3, "internal", E_CELL)
    caps = _ycyl(cx_, 34.0, cz_, 7.0, 2.0) + _ycyl(cx_, -34.0, cz_, 12.0, 2.0)
    add("Cell terminals", caps, C_ALU, "metal", 3, "internal", E_CELL)
    cradle = _bx(cx_ - 19, cx_ + 19, -42, 42, z0 + wt, cz_ - 2) - _ycyl(cx_, 0, cz_, 16.4, 80.0)
    cradle -= _bx(cx_ - 20, cx_ + 20, -30, 30, z0 + wt + 4, cz_)
    add("Cell cradle with fuse", cradle, C_DARK, "plastic", 3, "internal", E_CELL)

    # back plate (BOM 6): the built plate with its window, band slots and fixing holes; the V-blocks
    # fix to it with the M4 countersunk screws of the adapter group
    add("FieldNode back plate", model["plate"], C_ALU, "metal", 6, "shell", (-60, 0, 0))

    # street pole adapter (BOM 14): model.py V-blocks and bands unchanged, band clamp bolts
    add("Street pole adapter (V-blocks and bands)", model["adapter"], C_ALU2, "metal", 14, "shell", (0, 0, 0))
    vw, vd, vh = P["vb"]
    cb = None
    for dz in P["clamp_dz"]:
        zc = z0 + dz + P["band_w"] / 2
        for sy in (-1, 1):
            for xb in (D["plate_front"] + 18, D["plate_front"] + 44):
                b = _hex_y(xb, sy * (vw / 2 + 8.0), zc, 8.0, 4.0) + _ycyl(xb, sy * (vw / 2 + 3.5), zc, 2.5, 7.0)
                cb = b if cb is None else cb + b
    add("Band clamp bolts", cb, C_STEEL, "metal", 14, "shell", (0, 0, 0))

    # solar panel (BOM 4): model.py envelope, aluminium frame, dark cells with a grid, junction box
    pw, pl, pt = P["panel"]
    pan = Pos(D["panel_cx"], 0, D["panel_cz"]) * Rot(0, -P["tilt"], 0)
    E_PAN = (-120, 0, 330)
    frame = Box(pl, pw, pt)
    frame = _fillet_try(frame, frame.edges().filter_by(Axis.Z), [5.0, 3.0])
    frame -= Pos(0, 0, pt / 2 - 2) * Box(pl - 14, pw - 14, 5)
    frame -= Pos(0, 0, -pt / 2 + 6) * Box(pl - 8, pw - 8, 12.02)
    add("Solar panel frame", pan * frame, C_ALU, "metal", 4, "shell", E_PAN)
    lam = Pos(0, 0, pt / 2 - 3.2) * Box(pl - 14, pw - 14, 2.4)
    lam = lam + Pos(0, 0, -pt / 2 + 11.5) * Box(pl - 8, pw - 8, 1.0)
    add("Solar cells (6 W)", pan * lam, C_CELLS, "screen", 4, "shell", E_PAN)
    grid = None
    zt = pt / 2 - 1.85
    for k in range(1, 4):
        g = Pos(-(pl - 14) / 2 + k * (pl - 14) / 4, 0, zt) * Box(0.9, pw - 16, 0.3)
        grid = g if grid is None else grid + g
    for k in range(1, 6):
        grid += Pos(0, -(pw - 14) / 2 + k * (pw - 14) / 6, zt) * Box(pl - 16, 0.9, 0.3)
    add("Solar cell grid lines", pan * grid, C_GRID, "metal", 4, "shell", E_PAN)
    jb = Pos(0, 0, -pt / 2 + 11.0 - 6.0) * Box(50, 40, 10)
    jb = _fillet_try(jb, jb.edges().filter_by(Axis.Z), [3.0, 2.0])
    add("Panel junction box", pan * jb, C_BLACK, "plastic", 4, "shell", E_PAN)

    # tilt bracket (BOM 5): model.py posts and struts
    add("Panel tilt bracket", model["bracket"], C_ALU2, "metal", 5, "shell", (-120, 0, 170))
    add("Bracket and panel clip bolts", Cm["fn_bracket_bolts"].shape + Cm["fn_panel_bolts"].shape, C_STEEL, "metal", 5, "shell", (-120, 0, 170))

    # ------------------------------------------------------------ street side: arm and head
    hx = D["head_x"]
    htop, hbot = D["head_top"], D["head_bot"]
    az = D["arm_z"]
    add("Microphone arm, saddle and band", model["arm"], C_ALU, "metal", 7, "shell", (0, 0, 0))

    E_HEAD = (230, 0, 70)
    head = model["head"]
    hd = P["head"][0]
    for k in range(4):                                # grip grooves near the base (texture)
        zg = hbot + 8 + 6 * k
        head -= _zcyl(hx, 0, zg, hd / 2 + 1, 1.2) - _zcyl(hx, 0, zg, hd / 2 - 0.6, 2.0)
    add("Microphone head housing (ASA)", head, C_HEAD, "plastic", 8, "shell", E_HEAD)
    ring_z = htop - P["skirt_dz"] - P["skirt"][1] / 2 - 3.0
    ring = _zcyl(hx, 0, ring_z, hd / 2 + 0.5, 3.0) - _zcyl(hx, 0, ring_z, hd / 2 - 0.5, 4.0)
    add("Head accent ring", ring, C_ACCENT, "painted", 8, "shell", E_HEAD)
    add("Head cable gland (M16, in the bottom cap)", Cm["gland"].shape, C_DARK, "plastic", 12, "shell", E_HEAD)

    # windscreen and bird spike (BOM 11), model.py sizes
    add("Foam windscreen", Cm["windscreen"].shape, C_FOAM, "fabric", 11, "shell", (230, 0, 230))
    add("Bird spike (in the skirt boss, 26 mm off the axis)", Cm["spike"].shape, C_STEEL, "metal", 11, "shell", (230, 0, 300))

    # microphone on its adapter board (BOM 9) and level processor (BOM 10), model.py positions
    add("MEMS microphone on adapter board", model["mic"], C_PCB, "plastic", 9, "internal", (230, 0, -110))
    pw_, pd_, ph_ = P["proc"]
    pz1 = htop - P["top_t"] - 12
    proc = _bx(hx - 0.8, hx + 0.8, -pw_ / 2, pw_ / 2, pz1 - ph_, pz1)
    add("Level processor board", proc, C_PCB, "plastic", 10, "internal", (230, 0, -260))
    pc = (_bx(hx + 0.8, hx + 2.2, -7, 7, pz1 - 30, pz1 - 16) + _bx(hx + 0.8, hx + 1.8, -9, 1, pz1 - 55, pz1 - 45)
          + _bx(hx - 2.2, hx - 0.8, -6, 6, pz1 - 12, pz1 - 4))
    add("Level processor (Cortex-M4F)", pc, C_CHIP, "plastic", 10, "internal", (230, 0, -260))

    # sensor cable (BOM 12): model.py route with rounded bends
    xmid = xm
    crr = P["cable_d"] / 2
    pts = [(xmid, py0, z0 - 38), (xmid, py0, z0 - 60), (-r - 12, -r - 12, z0 - 60),
           (-r - 12, -r - 12, az - 70), (0, -r - 16, az - 55), (r + 20, -r + 10, az - 40), (hx - 30, -12, az - 25),
           (hx, -12, hbot - 12), (hx, 0, hbot - 6)]
    add("Sensor cable (M12)", _pipe(pts, crr), C_BLACK, "rubber", 12, "shell", (0, -220, -40))

    # ------------------------------------------------------------ context: short pole section
    pz_a, pz_b = POLE_Z
    pole = _zcyl(0, 0, (pz_a + pz_b) / 2, r, pz_b - pz_a)
    add("Street pole section (114 mm)", pole, C_POLE, "painted", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:42s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:9.2f} cm3")
