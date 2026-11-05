"""NoiseMap STEM check, NSM-STM-001 (STANDARDS section 20).

Run from the repo root:  python docs/04-calcs/stem_check.py
Writes docs/04-calcs/stem_results.csv. First-order screens of every physical, chemical and biological claim of
option A (the current design) and the claims that set options B and C apart. The calculation note
NSM-CAL-001 (docs/04-calcs/sizing.py) holds the detailed numbers; the values below are repeated from it where
a row cites it, and the mass is the model mass.
"""
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
from stem_check import Check, limits  # noqa: E402

c = Check(ROOT / "docs/04-calcs/stem_results.csv")
RHO = 1.225          # kg/m3, air at 15 C
V_GUST = 35.0        # m/s, design gust (NSM-REQ-001 R10)


def lora_airtime(pl_bytes, sf, bw=125e3, cr=1, preamble=8, de=None):
    """LoRa time on air in s (Semtech AN1200.13), explicit header, CRC on."""
    de = (1 if sf >= 11 else 0) if de is None else de
    ts = 2 ** sf / bw
    n = 8 + max(math.ceil((8 * pl_bytes - 4 * sf + 28 + 16) / (4 * (sf - 2 * de))) * (cr + 4), 0)
    return (preamble + 4.25) * ts + n * ts


# ------------------------------------------------------------------ Option A (current design)
c.claim("S1", "Quietest level the microphone resolves: 35 dBA with 1 dB error (IM72D128 fitted by default, 72 dB(A) SNR re 94 dB SPL)",
        "Physics", "Acoustics and vibration", "Self-noise = 94 dB SPL - SNR = 22 dBA; power subtraction error at 35 dBA (CAL A1). The ICS-43434 alternative has 34.9 dBA and no margin",
        value=27.9, limit=35.0, unit="dBA (lower limit for 1 dB error)", rule="below", margin=0.0,
        closed_by="NSM-CAL-001 A1; microphone choice NSM-DEC-001 (2026-11-02)")
c.claim("S2", "Loudest level before clipping: 110 dBA for traffic (IM72D128, overload point 126 dB SPL at 1 % THD)",
        "Physics", "Acoustics and vibration",
        "Peak limit: 126 dB SPL + 3 dB peak/rms - 10 dB crest = 119 dB SPL unweighted; an A-weighted traffic level is 5 to 10 dB lower (mid 7.5 dB); Infineon IM72D128V01 product brief",
        value=119.0 - 7.5, limit=110.0, unit="dBA (ceiling, mid case)", rule="above", margin=0.05,
        closed_by="NSM-CAL-001 A4 (109 to 114 dBA); the ICS-43434 alternative gives 103 to 108 dBA and misses 110 dBA, so the IM72D128 is fitted by default (NSM-DEC-001)")
c.claim("S3", "A- and C-weighted levels computed in the head from 48 kHz samples cover the 20 kHz audio band",
        "Mathematics", "Numerical method", "Nyquist: the sample rate must exceed twice the highest frequency (24 kHz)",
        value=20.0, limit=24.0, unit="kHz", rule="below")
cycles = 132 * 48000
c.claim("S4", "Level processor load: 132 cycles per sample at 48 kHz on a 48 MHz Cortex-M4F is 13 % of the core",
        "Engineering and technology", "Sensing resolution and control", "Cycle budget = cycles per sample x sample rate (CAL F1)",
        value=cycles / 1e6, limit=48.0, unit="Mcycles/s", rule="below")
harvest_limit = 6.0 * 1.5          # Wh: panel rating x peak sun hours, before any losses
c.claim("S5", "Solar harvest of 5.81 Wh/day stored from a 6 W panel at 1.5 peak sun hours",
        "Physics", "Thermodynamics", "Energy = rated power x peak sun hours at 1000 W/m2 (cannot exceed 9.0 Wh)",
        value=5.81, limit=harvest_limit, unit="Wh/day", rule="below", margin=0.0)
cell_wh = 3.2 * 6.0
c.order_of_magnitude("S6", "Autonomy of 53 days without sun on one 3.2 V, 6 Ah LiFePO4 cell at 0.29 Wh/day",
                     "Chemistry", "Electrochemistry and batteries", claimed=53.0, estimate=cell_wh * 0.8 / 0.29, unit="days",
                     law="Stored energy 19.2 Wh x 80 % usable divided by the daily load (CAL E2); 52.9 days rounds to 53")
air9 = lora_airtime(22 + 13, 9)
c.order_of_magnitude("S7", "LoRaWAN airtime 23.7 s/day at SF9 and 15 minute records (22 byte payload, 13 byte MAC overhead)",
                     "Engineering and technology", "Power and link budgets", claimed=23.7, estimate=air9 * 96, unit="s/day",
                     law="Semtech AN1200.13 time on air, 96 uplinks a day")
c.claim("S8", "Duty cycle: one SF9 uplink needs a quiet interval of 99 x airtime; the 15 minute interval is longer",
        "Engineering and technology", "Standards practice", "ETSI EN 300 220 sub-band limit of 1 % duty cycle for EU868 (cited in NSM-REQ-001 R12)",
        value=air9 * 99, limit=900.0, unit="s between uplinks", rule="below")
c.order_of_magnitude("S9", "The 9,600 baud head-to-core cable is about 150 times too slow for raw 24-bit, 48 kHz audio",
                     "Engineering and technology", "Power and link budgets", claimed=150.0, estimate=48000 * 24 / (9600 * 0.8), unit="x",
                     law="Raw bit rate / UART payload rate (8N1 is 80 % efficient)")
a_wind = 0.29 * 0.2 + 0.15 * 0.2 + 0.09 * 0.15 + 0.025 * 0.4     # panel, enclosure, windscreen, arm (m2)
f_wind = 0.5 * RHO * V_GUST ** 2 * 1.2 * a_wind
c.order_of_magnitude("S10", "Wind load of about 96 N on the whole node in a 35 m/s gust",
                     "Physics", "Fluid mechanics", claimed=96.0, estimate=f_wind, unit="N",
                     law="Drag F = 1/2 rho v^2 Cd A with Cd 1.2 and the projected areas of panel, box, windscreen and arm")
z = math.pi / 32 * (25 ** 4 - 21 ** 4) / 25            # section modulus of the 25 x 2 mm tube, mm3
sigma = 4.10e3 / z                                      # N.mm / mm3 = MPa; 4.10 N.m at the arm root (CAL H4: wind 4.01 + weight 0.83, combined)
c.claim("S11", "Arm bending stress under a 35 m/s gust (4.10 N.m at the arm root: wind on arm, head and windscreen 14.8 N, plus weight)",
        "Physics", "Strength of materials", "Cantilever bending, sigma = M/Z (CAL H3, H4); 6063-T5/T6 aluminium yield about 145 to 215 MPa (taken as 145); stress concentration at the flange screw holes (Kt 2 to 3) still leaves a factor of 9 or more",
        value=sigma, limit=145.0, unit="MPa", rule="below", margin=0.1)
mass_a = 3.45     # kg, model mass (cad/fidelity.json reports 3.5 after rounding to 0.1 kg; NSM-CAL-001 H2 3.45)
c.claim("S12", "Mass on the pole of 3.5 kg or less (R10): model mass of the constructable design",
        "Physics", "Mechanics and statics", "Sum of part volumes x density from the model (cad/fidelity.json)",
        value=mass_a, limit=3.5, unit="kg", rule="below", margin=0.05,
        closed_by="NSM-CAL-001 H2 and cad/fidelity.json; margin 0.05 kg accepted 2026-10-02 (NSM-DDR-003 A2)")
c.claim("S13", "Reflections bias a level by up to 2.4 dB from one facade and up to 2.7 dB in a street canyon (A and C)",
        "Physics", "Acoustics and vibration", "Incoherent reflection of a line source from one or two facades (CAL C2, C2c); a single coherent reflection cannot exceed +6.02 dB, but several reflections can, so the bound is a screen only",
        value=2.7, limit=20 * math.log10(2), unit="dB", rule="below", margin=0.6,
        closed_by="NSM-CAL-001 C2 and C2c; the per-deployment site correction (NSM-DDR-001 D7) sets the real figure")
u = math.sqrt(sum(x * x for x in (0.4, 0.5, 0.5, 0.7, 0.8)))
c.order_of_magnitude("S14", "Expanded uncertainty (k = 2) of 2.9 dB against a 2 dB target (R3, at risk)",
                     "Mathematics", "Statistics and uncertainty", claimed=2.9, estimate=2 * 1.47, unit="dB",
                     law="Root sum of squares of the CAL C3 terms; k = 2 gives about 95 % coverage (GUM, JCGM 100:2008). The arithmetic holds; the result (3.1 dB with the reference meter) is above the 2 dB target, so PR-003 is not met on paper")
c.cited("S15", "Stainless bands and screws on aluminium blocks do not corrode the blocks over the service life",
        "Chemistry", "Electrochemistry and batteries",
        "Galvanic couple (ASTM G82 galvanic series): stainless is the cathode, aluminium the anode. Screening by area ratio is optimistic in a wet salt film (review finding); crevice corrosion under bands and in tapped holes is the likelier failure",
        "Screw threads and the band contact faces are sealed with the neutral-cure silicone already in BOM line 13 (fix under the standing instruction, NSM-DEC-001); the 5 year life stays a TRL 4 salt-spray test (PR-014)",
        "Within known science", "NSM-DEC-001 (sealing of stainless-to-aluminium joints)")
c.cited("S16", "Printed ASA head and UV-stabilized foam survive 5 years outdoors with a yearly foam change",
        "Chemistry", "Materials and polymer chemistry",
        "ASA is the UV-resistant member of the styrenic family (acrylate rubber, no butadiene double bonds); foam is replaced yearly",
        "Qualitative; the 5 year life is a TRL 4 test (R14), no number is claimed", "Within known science")
c.cited("S17", "Cell is charged only inside the maker's limits (0 to 45 C) and discharged to -20 C with reduced capacity",
        "Chemistry", "Electrochemistry and batteries",
        "LiFePO4 cells plate lithium if charged below 0 C; FieldNode's core has a cold-charge lockout; capacity falls in the cold (CAL E2: 37 days at -20 C)",
        "Lockout is a FieldNode design item (FND-CAL-001); NoiseMap adds no charging", "Within known science")
f_mhz, hb, hm, d_km = 868.0, 30.0, 4.0, 1.0           # Okumura-Hata small city, used slightly outside its 150 to 1500 MHz band
a_hm = (1.1 * math.log10(f_mhz) - 0.7) * hm - (1.56 * math.log10(f_mhz) - 0.8)
hata = 69.55 + 26.16 * math.log10(f_mhz) - 13.82 * math.log10(hb) - a_hm + (44.9 - 6.55 * math.log10(hb)) * math.log10(d_km)
c.claim("S18", "LoRa link to a gateway 1 km away across an urban street (14 dBm, SF9 sensitivity about -129 dBm)",
        "Physics", "Electromagnetism and circuits", "Okumura-Hata urban path loss for a 30 m gateway and 4 m node (about 120 dB) against the 143 dB available; 23 dB of margin",
        value=hata, limit=14 + 129, unit="dB loss", rule="below")
t_allowed_min = 480 / 2 ** ((94 - 85) / 3)
c.claim("S19", "Field check with a 94 dB, 1 kHz calibrator is safe: 2 minutes of exposure",
        "Biology", "Human physiology and biomechanics", "NIOSH recommended exposure limit 85 dBA for 8 h with a 3 dB exchange rate: 60 min at 94 dBA",
        value=2.0, limit=t_allowed_min, unit="min", rule="below")
# ------------------------------------------------------------------ Option B (balcony post node)
p_b = 5.0 * 0.12
c.claim("S20", "B: a Wi-Fi microphone node draws about 0.6 W from a 5 V, 1 A USB supply (about 120 mA average)",
        "Physics", "Electromagnetism and circuits", "P = V I; a 2.4 GHz module averages 80 to 150 mA with periodic transmit (datasheet class, estimate)",
        value=p_b, limit=5.0, unit="W", rule="below")
loss_b = 32.44 + 20 * math.log10(0.01) + 20 * math.log10(2437.0) + 10.0
c.claim("S21", "B: Wi-Fi link from the balcony to the router 10 m away through one wall (20 dBm, -90 dBm sensitivity)",
        "Physics", "Electromagnetism and circuits", "Free-space loss at 2437 MHz plus 10 dB wall allowance (estimate)",
        value=loss_b, limit=20 + 90, unit="dB loss available", rule="below")
f_slip = 0.5 * RHO * V_GUST ** 2 * 1.2 * (0.1 * 0.055) + 0.95 * 9.81
c.claim("S22", "B: two bands (1,000 N preload, friction 0.2) hold a 0.95 kg box on a vertical post in a 35 m/s gust",
        "Physics", "Mechanics and statics", "Coulomb friction on the V faces: capacity 2 x 1000 N x 0.2 x sqrt(2), the friction value of NSM-CAL-001",
        value=f_slip, limit=2 * 1000 * 0.2 * math.sqrt(2), unit="N", rule="below", margin=0.1)
# ------------------------------------------------------------------ Option C (luminaire socket node)
p_c = 0.5 / 0.7
c.claim("S23", "C: the node takes about 0.7 W from the luminaire (0.5 W load through a 70 % efficient converter), 6 kWh a year",
        "Physics", "Thermodynamics", "Input power = load / efficiency; a small isolated converter is 60 to 80 % efficient (datasheet class, estimate)",
        value=p_c, limit=1.0, unit="W (a design ceiling)", rule="below")
dl = 10 * math.log10(math.hypot(5.0, 5.5) / math.hypot(5.0, 3.5))
c.claim("S24", "C: a microphone 6 m up reads about 0.8 dB less than one at 4 m for a road 5 m away (line source)",
        "Physics", "Acoustics and vibration", "Geometric spreading from a line source, 10 log(r2/r1), source height 0.5 m",
        value=dl, limit=1.5, unit="dB (change in level)", rule="below")
if __name__ == "__main__":
    state = c.write()
    sys.exit(0 if state != "fail" else 1)
