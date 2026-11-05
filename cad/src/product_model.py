"""NoiseMap product appearance model for photoreal renders (kit 1.9), TRL 3, option A (the current design).

Every part of the node comes from cad/src/model.py components(CHOSEN) as modelled: the FieldNode core with its lid,
cell, boards and fixings, the solar panel on its tilt bracket, the back plate and street pole adapter with bands, the
sensor arm, the printed ASA microphone head, the foam windscreen and the bird spike, the cable and its ties. Only the
site is added, as context parts: a street pole carrying a luminaire arm, the pavement slab, a kerb and the road, and a
1.75 m mannequin standing on the pavement beside the pole for scale. Ground level is z = 0 (the node's own sidewalk
level); every site part reaches below it. The pole stands on the Z axis and the street lies toward +X.
APPEARANCE MODEL ONLY. CONCEPT, NOT FOR FABRICATION.

Groups: "shell" (what is seen from outside), "internal" (boards, cell, level processor), "context" (site, mannequin).
Part names ending "(site)" are left out of the picture framing; "(scale)" stays in it.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material_name"])
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Cylinder, Pos, Rot  # noqa: E402
from cad_parts import part  # noqa: E402
import model  # noqa: E402
from nsm_parts import box, zcyl  # noqa: E402

TITLE = "NoiseMap: street pole sound level meter that records decibels only, never audio"

_SITE_HERO = ["--scene=outdoor", "--ground=concrete", "--ground-z=0", "--sun=38,-125", "--lens=50"]

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 14, "az": -140,
     "args": _SITE_HERO,
     "note": "Site render from the sidewalk side, front left and about 14 deg above the horizon: the NoiseMap node clamped "
             "to a street pole with its solar panel and FieldNode core, the microphone arm reaching 0.45 m toward the "
             "road with the foam windscreen and bird spike at 4.0 m, kerb and road beyond; 1.75 m mannequin standing "
             "on the pavement beside the pole for scale"},
    {"name": "node", "groups": ["shell", "internal"], "explode": False, "el": 20, "az": -140,
     "note": "Studio view from the sidewalk side, front left and about 20 deg above the horizon, without the pole "
             "context: FieldNode core with lid and status light, panel on its bracket, arm, microphone head and "
             "windscreen"},
    {"name": "exploded", "groups": ["shell", "internal"], "explode": True, "el": 24, "az": -130,
     "note": "Exploded view from the front left and about 24 deg above the horizon: enclosure and lid, boards and cell, "
             "solar panel and bracket, back plate and pole adapter, arm, microphone head, level processor, windscreen "
             "and cable"},
]

_INTERNAL = {"board", "cell", "proc"}


def _group(p):
    if p["kind"] == "context":
        return "context"
    return "internal" if p["group"] in _INTERNAL else "shell"


def site():
    """Street furniture and the mannequin; every part reaches below z = 0 except the pole, kerb and figure."""
    from context_parts import mannequin
    r = model.PARAMS["pole_od"] / 2
    out = [
        part("Street pole, 114.3 mm (site)", zcyl(0, 0, -400.0, 6400.0, r), "galvanised", "context"),
        part("Pole base collar (site)", zcyl(0, 0, -400.0, 650.0, r + 14.0), "galvanised", "context"),
        part("Luminaire arm (site)", Pos(700, 0, 6000.0) * Rot(0, 90, 0) * Cylinder(38.0, 1400.0), "galvanised", "context"),
        part("Luminaire head (site)", box(1000, 1900, -170, 170, 5920.0, 6080.0), "mild_steel", "context"),
        part("Pavement slab (site)", box(-3500, 2200, -3500, 3500, -400.0, 0.0), "concrete", "context"),
        part("Kerb stone (site)", box(2200, 2350, -3500, 3500, -400.0, 140.0), "concrete", "context"),
        part("Road surface (site)", box(2350, 8000, -3500, 3500, -400.0, -10.0), "mild_steel", "context"),
    ]
    # 1.75 m person standing on the pavement beside the pole, facing -Y (toward the viewer's side)
    out.append(part("Person, 1.75 m, standing (scale)", Pos(-650, 520, 0) * mannequin(1750, "stand"), "skin", "context"))
    return out


def product_parts():
    out = []
    for p in model.components(model.CHOSEN):
        q = dict(p)
        if q["kind"] == "context":
            continue                      # the options-picture site is replaced by the richer site below
        q["group"] = _group(p)
        out.append(q)
    for p in site():
        q = dict(p)
        q["group"] = "context"
        out.append(q)
    return out


if __name__ == "__main__":
    ps = product_parts()
    for p in ps:
        if p["group"] == "context":
            s = p["shape"]
            print(f"{p['name']:50s} {p['material_name']:12s} valid={s.is_valid} zmin={s.bounding_box().min.Z:8.1f}")
    print(len(ps), "parts")
