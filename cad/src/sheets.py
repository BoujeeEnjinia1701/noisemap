"""NoiseMap general arrangement drawing NSM-DWG-001 (Rev P1).

Run from the repo root:  python cad/src/sheets.py
Builds cad/drawings/NSM-DWG-001.svg, .pdf and .png from the parametric model (cad/src/model.py).
NSM-DWG-001 is free because the concept blueprint in media/ is NSM-DWG-010.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from drawing import Sheet, project_views  # noqa: E402
from model import PARAMS as P, derived, assemblies, build_parts  # noqa: E402

D = derived(P)
parts = build_parts()
asm = assemblies(parts)["noisemap-assembly"]
work = ROOT / "cad/drawings/_views"
views = project_views(asm, work)

s = Sheet(project="NoiseMap", title="General arrangement, street pole node", dwg_no="NSM-DWG-001",
          rev="P1", author="Amish Chadha", date="2026-09-25", concept=True,
          material="Arm, saddle, V-blocks 6063 Al; head ASA; bands stainless. See bom/bom.csv",
          revisions=[("P1", "Preliminary GA from model.py (NSM-CAL-001)", "2026-09-25", "AC")])
s.add_ortho(views, ["front", "top", "right"])
s.add_svg(views["iso"], 276, 30, 140, 84, label="Isometric view", sublabel="Not to scale")
s.add_notes("Key dimensions and interfaces (mm)", [
    f"Microphone port {P['mic_z']:.0f} above sidewalk, {P['mic_off']:.0f} off pole face",
    f"Design pole OD {P['pole_od']}; adapter seats {P['pole_range'][0]:.0f} to {P['pole_range'][1]:.0f}",
    f"V-blocks {P['vb'][0]:.0f} x {P['vb'][1]:.0f} x {P['vb'][2]:.0f}, 90 deg, {P['vnotch_w']:.0f} opening",
    f"Arm {P['arm'][0]:.0f} x {P['arm'][1]:.0f} Al tube, {D['arm_len']:.0f} long, own band clamp",
    f"Head {P['head'][0]:.0f} OD x {P['head'][2]:.0f}; port {P['port_d']:.0f} dia x {P['top_t']:.0f}",
    f"Windscreen {P['ws_d']:.0f} foam ball, bore {P['ws_bore']:.0f}; spike {P['spike'][0]:.0f}",
    "FieldNode core per FND-DWG-001: box 150 x 90 x 200,",
    "  6 W panel at 40 deg, back plate 180 x 320 x 3",
    "Core and arm turn independently about the pole",
    "M12 5-pin cable 1.5 m: 3.3 V, GND, UART 9,600 baud",
    "Mass about 3.3 kg (NSM-CAL-001, R10 not met)",
    "PRELIMINARY, NOT FOR FABRICATION",
], x=276, y=128, width=140)
s.save(ROOT / "cad/drawings/NSM-DWG-001")
shutil.rmtree(work, ignore_errors=True)
print("wrote cad/drawings/NSM-DWG-001.svg, .pdf, .png")
