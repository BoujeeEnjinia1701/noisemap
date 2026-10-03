"""NoiseMap general arrangement drawing NSM-DWG-001 (Rev P4).

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
from model import PARAMS as P, derived, assemblies, build_parts, patch_svg_export  # noqa: E402

patch_svg_export()

D = derived(P)
parts = build_parts()
asm = assemblies(parts)["noisemap-assembly"]
work = ROOT / "cad/drawings/_views"
views = project_views(asm, work)

s = Sheet(project="NoiseMap", title="General arrangement, street pole node", dwg_no="NSM-DWG-001",
          rev="P4", author="Amish Chadha", date="2026-10-02", concept=True,
          material="Saddle, tube, V-blocks Al; head ASA; bands stainless. See bom/bom.csv",
          revisions=[("P1", "Preliminary GA from model.py (NSM-CAL-001)", "2026-09-25", "AC"),
                     ("P2", "Pocketed V-blocks and saddle; V notch corrected (NSM-DDR-002)", "2026-09-25", "AC"),
                     ("P3", "Design for construction (NSM-DDR-003)", "2026-10-01", "AC"),
                     ("P4", "M12 pin assignment and 3.3 V port label (2026-10-02)", "2026-10-02", "AC")])
s.add_ortho(views, ["front", "top", "right"])
s.add_svg(views["iso"], 276, 38, 140, 78, label="Isometric view", sublabel="Not to scale")
s.add_notes("Key dimensions and interfaces (mm)", [
    f"Microphone port {P['mic_z']:.0f} above sidewalk, {P['mic_off']:.0f} off pole face",
    f"Design pole OD {P['pole_od']}; adapter seats {P['pole_range'][0]:.0f} to {P['pole_range'][1]:.0f}",
    f"V-blocks {P['vb'][0]:.0f} x {P['vb'][1]:.0f} x {P['vb'][2]:.0f}, 90 deg V, {2 * D['v_half_mouth']:.0f} mouth,",
    "  on FieldNode's V-block screws; bands through its slots",
    f"Arm saddle: {P['saddle'][3]} sheet channel, 2 bands; tube flange",
    f"Arm {P['arm'][0]:.0f} x {P['arm'][1]:.0f} Al tube, {D['arm_len']:.0f} long, cross bolted",
    f"Head {P['head'][0]:.0f} OD x {P['head'][2]:.0f}; port {P['port_d']:.0f} dia x {P['top_t']:.0f}; cap, M16 gland",
    f"Windscreen {P['ws_d']:.0f} foam ball, bore {P['ws_bore']:.0f}; spike in skirt boss",
    "FieldNode core per FND-DWG-001 Rev P3, without its",
    "  small-pole V-blocks and bands",
    "Core and arm turn independently about the pole",
    "M12 cable 1.5 m: pin 1 3.3 V, 3 GND, 2 and 4 UART",
    "Mass about 3.45 kg (NSM-CAL-001 v0.3; R10 3.5 kg)",
    "PRELIMINARY, NOT FOR FABRICATION",
], x=276, y=128, width=140)
s.save(ROOT / "cad/drawings/NSM-DWG-001")
shutil.rmtree(work, ignore_errors=True)
print("wrote cad/drawings/NSM-DWG-001.svg, .pdf, .png")
