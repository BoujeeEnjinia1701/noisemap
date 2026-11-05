"""NoiseMap concept options B and C, modelled at D3 (kit 1.9, STANDARDS section 24).

Option B, balcony post node: microphone, processor and radio on one board in an IP65 box clamped to a
resident's balcony post, powered over USB, levels over home Wi-Fi. No solar panel, cell, pole or LoRaWAN.
Option C, luminaire socket node: a puck that twist-locks into the street luminaire's photocontrol
receptacle and takes its power from the luminaire; LoRaWAN uplink; microphone on top of the luminaire.
Each function returns cad_parts.part() dicts. B has its post axis on Z and the street toward +X; C has the
receptacle on the Z axis and is lifted to PARAMS["optC"]["z"]. Dimensions are in model.PARAMS["optB"] and
["optC"]. Context parts carry "(site)" in their names and kind "context".
"""
import math

import nsm_parts as N
from nsm_parts import box, zcyl, xcyl, pan_screw, vee_block
from cad_parts import part, at, break_edges, round_tube, hex_bolt, washer
from build123d import Cylinder, Pos, Rot, Sphere, Box


def _m():
    import model
    return model


def _wind_dome(cx, cy, z0, r):
    """Open-cell foam dome: a ball of radius r centred on z0, cut flat at z0 so it sits on the lid."""
    return Pos(cx, cy, z0) * Sphere(r) - box(cx - r - 1, cx + r + 1, cy - r - 1, cy + r + 1, z0 - r - 1, z0)


def option_b(P):
    M = _m()
    q = P["optB"]
    out = []
    add = lambda *a, **k: out.append(part(*a, **k))
    r = q["post_od"] / 2
    c = P["band_t"] / 2
    bw, bt = P["band_w"], P["band_t"]
    # ---- site context: slab, post, handrail
    add("Balcony slab (site)", box(-1200, 600, -900, 900, -150, 0), "concrete", kind="context", group="context")
    add("Railing post (site)", zcyl(0, 0, 0, q["post_h"], r) - zcyl(0, 0, -1, q["post_h"] + 1, r - q["post_t"]), "galvanised",
        kind="context", group="context")
    add("Handrail (site)", Pos(0, 0, q["post_h"] + r) * Rot(90, 0, 0) * Cylinder(r, 1600) , "galvanised", kind="context", group="context")
    # ---- post clamp block and bands
    blk, g = vee_block(q["blk"][0], q["blk"][1], q["blk"][2], r, q["land"], side=1)
    for sy in (-1, 1):
        for sz in (-1, 1):
            blk -= box(g["front"] - 1, g["back"] + 1, sy * q["slot_y"] - 1.5, sy * q["slot_y"] + 1.5,
                       sz * q["band_dz"] - (bw + 3) / 2, sz * q["band_dz"] + (bw + 3) / 2)
    for sz in (-1, 1):
        blk -= xcyl(g["back"] - 14, g["back"] + 1, 0, sz * q["bolt_dz"], 2.5)      # M5 tapped, blind
    blk = break_edges(blk, 0.6)
    add("Post clamp block", blk, "aluminium", "made", bom=1, group="mount")
    for sz in (-1, 1):
        pts = [(g["back"] + c, 0.0), (g["back"] + c, q["slot_y"]), (g["front"] - c, q["slot_y"])]
        add(f"Band clamp {'upper' if sz > 0 else 'lower'}, 12 mm", M.band_loop(pts, r + c, sz * q["band_dz"], bw, bt),
            "stainless", "bought", bom=2, group="mount")
    # ---- enclosure: base with bosses, lid, gasket
    ex0, ey, ez0, ez1 = g["back"], q["box"][1] / 2, -q["box"][2] / 2, q["box"][2] / 2 - 2.0     # base z range
    ex1 = ex0 + q["box"][0]
    w = q["wall"]
    zt = ez1                                               # top of the base rim
    base = box(ex0, ex1, -ey, ey, ez0, zt) - box(ex0 + w, ex1 - w, -ey + w, ey - w, ez0 + w, zt + 1)
    bx = [ex0 + 8, ex1 - 8]
    by = [-ey + 8, ey - 8]
    for x in bx:
        for y in by:
            base += zcyl(x, y, ez0 + w - 0.01, zt, 4.0)
            base -= zcyl(x, y, zt - 16, zt + 1, 2.0)         # M4 blind hole, bore equals the plain shank
    pcx, pcy = (ex0 + ex1) / 2, 0.0
    pb = ez0 + w + 5.0                                    # board underside
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = pcx + sx * q["pcb_hole"][0], pcy + sy * q["pcb_hole"][1]
            base += zcyl(x, y, ez0 + w - 0.01, pb, 3.0)
            base -= zcyl(x, y, pb - 5.5, pb + 1, 1.5)
    gx, gy = pcx, -20.0                           # cable gland through the floor
    base -= zcyl(gx, gy, ez0 - 1, ez0 + w + 1, 8.0)
    for z in (-1, 1):                                      # band screw bores for the two M5 bolts
        base -= xcyl(ex0 - 1, ex0 + w + 1, 0, z * q["bolt_dz"], 2.5)
    base = break_edges(base, 0.8)
    add("Enclosure base, IP65 ABS", base, "polycarbonate", "bought", bom=3, group="box")
    lid_t = 4.0
    lid = box(ex0, ex1, -ey, ey, zt + 0.5, zt + 0.5 + lid_t)
    for x in bx:
        for y in by:
            lid -= zcyl(x, y, zt, zt + 1 + lid_t, 2.0)
    lid -= zcyl(pcx, pcy, zt, zt + 1 + lid_t, q["port_d"] / 2)
    lid = break_edges(lid, 0.8)
    add("Enclosure lid", lid, "polycarbonate", "bought", bom=3, group="box")
    gk = box(ex0, ex1, -ey, ey, zt, zt + 0.5) - box(ex0 + w, ex1 - w, -ey + w, ey - w, zt - 1, zt + 1)
    for x in bx:
        for y in by:
            gk -= zcyl(x, y, zt - 1, zt + 1, 2.0)
    add("Lid gasket", gk, "epdm", "bought", bom=3, group="box")
    ztop = zt + 0.5 + lid_t
    for x in bx:
        for y in by:
            add("M4x16 pan screw, lid", at(pan_screw(4, 16, 7.6, 2.8), (x, y, ztop)), "stainless", "fastener", bom=4, group="box")
    # ---- enclosure to block: two M5 bolts from inside, washers under the heads
    for z in (-1, 1):
        L = w + 14.0
        bolt = at(hex_bolt(5, L), (ex0 + w + 1.0, 0, z * q["bolt_dz"]), (0, 90, 0))
        add("M5 hex bolt, box to block", bolt, "stainless", "fastener", bom=4, group="mount")
        add("M5 washer, box to block", at(washer(5), (ex0 + w, 0, z * q["bolt_dz"]), (0, 90, 0)), "stainless", "fastener", bom=4, group="mount")
    # ---- board, bosses' screws, parts on the board
    pcb = box(pcx - q["pcb"][0] / 2, pcx + q["pcb"][0] / 2, -q["pcb"][1] / 2, q["pcb"][1] / 2, pb, pb + 1.6)
    for sx in (-1, 1):
        for sy in (-1, 1):
            pcb -= zcyl(pcx + sx * q["pcb_hole"][0], pcy + sy * q["pcb_hole"][1], pb - 1, pb + 2.6, 1.5)
    add("Main board (processor, Wi-Fi, USB power)", break_edges(pcb, 0.3), "pcb", "bought", bom=5, group="elec")
    for sx in (-1, 1):
        for sy in (-1, 1):
            add("M3x6 pan screw, board", at(pan_screw(3, 6, 5.6, 1.8), (pcx + sx * q["pcb_hole"][0], pcy + sy * q["pcb_hole"][1], pb + 1.6)),
                "stainless", "fastener", bom=4, group="elec")
    pt = pb + 1.6
    add("Wi-Fi module on board", break_edges(box(pcx - 38, pcx - 12.5, -9, 9, pt, pt + 3.1), 0.4), "chip", "bought", bom=5, group="elec")
    add("MEMS microphone on board", break_edges(box(pcx - 1.75, pcx + 1.75, -1.3, 1.3, pt, pt + 1.0), 0.2), "chip", "bought", bom=6, group="elec")
    ug = pt + 1.0
    add("Microphone seal, 0.5 mm", zcyl(pcx, pcy, ug, ug + 0.5, 3.0) - zcyl(pcx, pcy, ug - 1, ug + 1, 1.5), "epdm", "bought", bom=6, group="elec")
    add("Acoustic duct", at(round_tube(6.0, 1.5, zt + 0.5 - (ug + 0.5)), (pcx, pcy, ug + 0.5)), "asa", "made", bom=7, group="elec")
    add("Hydrophobic membrane", break_edges(zcyl(pcx, pcy, ztop, ztop + 0.3, 5.0), 0.08), "membrane", "bought", bom=7, group="box")
    add("Foam windscreen dome", _wind_dome(pcx, pcy, ztop + 0.3, q["ws_r"]), "foam", "bought", bom=8, group="box")
    # USB-C receptacle under the board over the gland, cable through the gland
    ux, uy = gx, gy
    add("USB-C receptacle on board", break_edges(box(ux - 4.5, ux + 4.5, uy - 3.6, uy + 3.6, pb - 3.2, pb), 0.4), "chip", "bought", bom=5, group="elec")
    gl = zcyl(gx, gy, ez0 - 6, ez0, 8.0) + zcyl(gx, gy, ez0, ez0 + w, 8.0) + N.zcyl(gx, gy, ez0 - 6, ez0 - 1, 10.0)
    gl -= zcyl(gx, gy, ez0 - 7, ez0 + w + 1, q["cable_d"] / 2)
    add("Cable gland, M16", break_edges(gl, 0.4), "nylon", "bought", bom=9, group="box")
    add("USB cable", break_edges(zcyl(gx, gy, ez0 - 140, pb - 3.2, q["cable_d"] / 2), 0.6), "nylon", "bought", bom=10, group="box")
    return out


def option_c(P):
    q = P["optC"]
    out = []
    add = lambda *a, **k: out.append(part(*a, **k))
    Z = q["z"]
    R, wl = q["od"] / 2, q["wall"]
    # ---- site context: pole, outreach arm, luminaire head with its receptacle
    add("Lighting column (site)", zcyl(0, -1300, -300, Z - 120, 57.15), "galvanised", kind="context", group="context")
    add("Outreach arm (site)", Pos(0, -650, Z - 150) * Rot(90, 0, 0) * Cylinder(30, 1300), "galvanised", kind="context", group="context")
    add("Luminaire head (site)", box(-300, 300, -250, 250, Z - 220, Z - 100), "mild_steel", kind="context", group="context")
    add("Photocontrol receptacle (site)", zcyl(0, 0, Z - 100, Z, 46.0) - zcyl(0, 0, Z - 101, Z - 8, 30.0), "matte_black", kind="context", group="context")

    def up(shape):
        return Pos(0, 0, Z) * shape
    # ---- one-piece printed housing: floor with blade slots, wall, four screw bosses, board bosses
    h = q["h"]
    body = zcyl(0, 0, 0, h, R) - zcyl(0, 0, wl, h + 1, R - wl)
    bs = [(q["boss_r"] * math.cos(math.radians(a)), q["boss_r"] * math.sin(math.radians(a))) for a in (45, 135, 225, 315)]
    for x, y in bs:
        body += zcyl(x, y, wl - 0.01, h, 4.0)
        body -= zcyl(x, y, h - 14, h + 1, 2.0)
    pz = wl + 6.0
    ps = [(q["pcb_r"] * math.cos(math.radians(a)), q["pcb_r"] * math.sin(math.radians(a))) for a in (60, 120, 240, 300)]
    for x, y in ps:
        body += zcyl(x, y, wl - 0.01, pz, 3.0)
        body -= zcyl(x, y, pz - 5.5, pz + 1, 1.5)
    blades = []
    for a in (0, 120, 240):
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        bx_, by_ = 24.0 * ca, 24.0 * sa
        blade = Pos(bx_, by_, (-q["blade_h"] + wl) / 2) * Rot(0, 0, a + 90) * Box(q["blade_w"], 1.6, q["blade_h"] + wl)
        body -= Pos(bx_, by_, wl / 2) * Rot(0, 0, a + 90) * Box(q["blade_w"], 1.6, wl + 2)
        blades.append(break_edges(blade, 0.3))
    body = break_edges(body, 0.8)
    add("Housing and twist-lock base (one piece)", up(body), "asa", "made", bom=1, group="housing")
    for i, b in enumerate(blades, 1):
        add(f"Contact blade {i}", up(b), "brass", "bought", bom=2, group="housing")
    add("Receptacle seal ring", up(zcyl(0, 0, -2, 0, R + 4) - zcyl(0, 0, -3, 1, R - 8)), "epdm", "bought", bom=3, group="housing")
    # ---- cover with port, gasket, four screws
    ct = 4.0
    cover = zcyl(0, 0, h + 0.5, h + 0.5 + ct, R)
    for x, y in bs:
        cover -= zcyl(x, y, h, h + 1 + ct, 2.0)
    cover -= zcyl(0, 0, h, h + 1 + ct, q["port_d"] / 2)
    cover -= zcyl(q["ant_off"], 0, h, h + 1 + ct, 3.2)
    add("Cover", up(break_edges(cover, 0.8)), "asa", "made", bom=4, group="housing")
    add("Cover gasket", up(zcyl(0, 0, h, h + 0.5, R) - zcyl(0, 0, h - 1, h + 1, R - wl)
                          - fuse_cyl(bs, h - 1, h + 1, 2.0)), "epdm", "bought", bom=3, group="housing")
    top = h + 0.5 + ct
    for x, y in bs:
        add("M4x16 pan screw, cover", up(at(pan_screw(4, 16, 7.6, 2.8), (x, y, top))), "stainless", "fastener", bom=5, group="housing")
    # ---- boards
    pcb = zcyl(0, 0, pz, pz + 1.6, q["pcb_d"] / 2)
    for x, y in ps:
        pcb -= zcyl(x, y, pz - 1, pz + 2.6, 1.5)
    add("Carrier board (power, LoRaWAN, level processor)", up(break_edges(pcb, 0.3)), "pcb", "bought", bom=6, group="elec")
    for x, y in ps:
        add("M3x6 pan screw, board", up(at(pan_screw(3, 6, 5.6, 1.8), (x, y, pz + 1.6))), "stainless", "fastener", bom=5, group="elec")
    pt = pz + 1.6
    add("AC-DC isolated converter module", up(break_edges(box(-21, 3, -12, 12, pt, pt + 20), 0.5)), "chip", "bought", bom=7, group="elec")
    add("LoRaWAN module", up(break_edges(box(5, 21, -9, 9, pt, pt + 3.0), 0.4)), "chip", "bought", bom=6, group="elec")
    # microphone board hung under the cover, 50 mm above the carrier
    mz = h - 1.0
    add("MEMS microphone board", up(break_edges(zcyl(0, 0, mz - 1.6, mz, 7.0), 0.3)),
        "pcb", "bought", bom=8, group="elec")
    add("Microphone seal", up(zcyl(0, 0, mz, h + 0.5, 3.0) - zcyl(0, 0, mz - 1, h + 1, q["port_d"] / 2)), "epdm", "bought", bom=8, group="elec")
    add("Hydrophobic membrane", up(break_edges(zcyl(0, 0, top, top + 0.3, 5.0), 0.08)), "membrane", "bought", bom=9, group="housing")
    add("Foam windscreen dome", up(_wind_dome(0, 0, top + 0.3, q["ws_r"])), "foam", "bought", bom=10, group="housing")
    # ---- antenna through the cover with a nut
    ax = q["ant_off"]
    add("Antenna whip, 868 MHz", up(break_edges(zcyl(ax, 0, top + 6.0, top + 6.0 + q["ant_h"], 3.5), 1.2)), "nylon", "bought", bom=11, group="housing")
    add("Antenna bulkhead connector", up(zcyl(ax, 0, h - 4.0, top + 6.0, 3.2) + zcyl(ax, 0, top, top + 6.0, 4.5)), "brass", "bought", bom=11, group="housing")
    return out


def fuse_cyl(pts, z0, z1, r):
    out = None
    for x, y in pts:
        s = zcyl(x, y, z0, z1, r)
        out = s if out is None else out + s
    return out
