"""NoiseMap repo helpers for the kit 1.9 model (materials the kit library lacks, small shapes, vee blocks).

Repo specific; the kit library is in .kit/cad_parts.py and is not edited. Importing this module adds
the extra materials to cad_parts.MATERIALS in the running process, so cad_parts.part() accepts them and
cad_parts.mass_kg() uses their density. The render class (second field) is one the Cycles renderer knows.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
import cad_parts as cp  # noqa: E402
from build123d import Box, Cylinder, Pos, Rot, Sphere, Align  # noqa: E402

cp.MATERIALS.update({
    "asa": ("#ECECEA", "hdpe", 1070),             # printed ASA
    "pcb": ("#166534", "painted", 1900),           # FR4 board with parts
    "chip": ("#111827", "matte_black", 1800),      # module, connector or chip bodies
    "cell": ("#2F4F6F", "metal", 1800),            # LiFePO4 cylindrical cell (matches the 140 g of a 32700 cell)
    "panel": ("#1B2735", "painted", 1800),         # framed 6 W panel, averaged over its volume
    "foam": ("#3A3F45", "rubber", 30),             # open-cell polyurethane windscreen
    "nylon": ("#111827", "matte_black", 1150),     # cable glands, cable jackets
    "membrane": ("#F4F4F2", "paper", 900),         # hydrophobic acoustic membrane
})


def box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0))


def zcyl(x, y, z0, z1, r):
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, abs(z1 - z0))


def xcyl(x0, x1, y, z, r):
    return Pos((x0 + x1) / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, abs(x1 - x0))


def pan_screw(d, length, head_d=None, head_h=None):
    """Pan head screw, head from z 0 to head_h, shank from z 0 down to -length (plain shank, as in assembly CAD)."""
    head_d = head_d or 1.9 * d
    head_h = head_h or 0.7 * d
    return Pos(0, 0, head_h / 2) * Cylinder(head_d / 2, head_h) + Pos(0, 0, -length / 2) * Cylinder(d / 2, length)


def vee_block(width, depth, height, pole_r, land, side=1):
    """Aluminium block with a 90 degree V notch that seats a round post of radius pole_r on both faces.
    The post axis is the Z axis. side=+1: block on the +X side. The notch vertex is pole_r*sqrt(2) from the
    axis; `land` of material lies behind it. Returns (shape, dict of x positions)."""
    apex = side * pole_r * math.sqrt(2)
    back = apex + side * land
    front = back - side * depth
    blk = box(min(back, front), max(back, front), -width / 2, width / 2, -height / 2, height / 2)
    m = abs(apex - front) + 2
    tri = Pos(0, 0, -height / 2 - 1) * __import__("build123d").extrude(
        __import__("build123d").Polygon((apex, 0), (apex - side * m, -m), (apex - side * m, m), align=None), height + 2)
    return blk - tri, dict(apex=apex, back=back, front=front)


def split_solids(shape):
    """The separate solids of a fused set of fixings, largest first."""
    try:
        s = list(shape.solids())
    except Exception:
        s = []
    return s or [shape]
