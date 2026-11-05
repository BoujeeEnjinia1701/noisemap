"""Export STL meshes for every option of the kit 1.9 model (cad/src/model.py).

Run from the repo root:  python cad/src/export_stl.py
Writes cad/stl/<option>-assembly.stl (the option's parts, site context left out) at 0.15 mm chordal tolerance and
cad/stl/A/<n>-<name>.stl for each 3D printed (ASA) part of the chosen option. STEP files come from
`python .kit/cad_check.py --export`. CONCEPT, NOT FOR FABRICATION.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(Path(__file__).resolve().parent)]
from build123d import Compound, export_stl  # noqa: E402
import model  # noqa: E402

TOL, ANG = 0.15, 0.3                     # mm chordal, radians angular
out = ROOT / "cad" / "stl"
out.mkdir(exist_ok=True)


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:48]


for opt in model.OPTIONS:
    parts = [p for p in model.components(opt) if p["kind"] != "context"]
    asm = Compound([p["shape"] for p in parts])
    export_stl(asm, str(out / f"{opt}-assembly.stl"), tolerance=TOL, angular_tolerance=ANG)
    print(opt, "assembly", len(parts), "parts")
    if opt == model.CHOSEN:
        (out / opt).mkdir(exist_ok=True)
        n = 0
        for p in parts:
            if p["kind"] == "made" and p["material_name"] == "asa":
                n += 1
                export_stl(p["shape"], str(out / opt / f"{n:02d}-{slug(p['name'])}.stl"), tolerance=TOL, angular_tolerance=ANG)
                print("  ", p["name"])
