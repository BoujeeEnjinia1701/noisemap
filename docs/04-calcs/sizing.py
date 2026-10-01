"""NoiseMap sizing calculations, NSM-CAL-001 v0.3 (TRL 3, constructable design NSM-DDR-003).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md; each line carries a tag such as [A3]
that the note cites. It also writes docs/04-calcs/results.csv (one row per requirement).
Geometry comes from cad/src/model.py (PARAMS, derived and the part volumes), costs from
bom/bom.csv and the budget from project.yaml. FieldNode energy figures are taken from FND-CAL-001 v0.1,
its mass from FND-CAL-001 v0.3 (constructable design).
First-principles estimates for a paper proof of concept; nothing here is measured.
"""
import csv
import math
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))
from model import PARAMS as P, derived, build_components  # noqa: E402

D = derived(P)
rows = []


def tag(t, text):
    print(f"[{t}] {text}")


def res(rid, value, target, status):
    rows.append((rid, value, target, status))


def db(x):
    return 10 * math.log10(x)


def dbsum(*levels):
    return db(sum(10 ** (l / 10) for l in levels))


# ---------------------------------------------------------------- assumptions
# Microphones. ICS-43434 figures from the TDK product page; IM72D128 SNR and interface from the DNMS README.
MICS = {
    "ICS-43434": {"snr": 65.0, "sens_dbfs": -26.0, "aop": 120.0, "f_lo": 60.0, "i_ma": 0.49, "if": "I2S"},
    "IM72D128": {"snr": 72.0, "sens_dbfs": None, "aop": 120.0, "f_lo": 60.0, "i_ma": 1.0, "if": "PDM"},
}
# Supply currents are typical class values, not checked. IM72D128 AOP and roll-off not checked: taken equal to ICS-43434.
REF_SPL = 94.0             # dB SPL reference for SNR and sensitivity
CREST = 10.0               # dB, crest factor allowed for traffic, sirens and horns above the rms level
ERR_LOW = 1.0              # dB, largest self-noise error accepted at the bottom of the range (uncorrected)
FC_TOL = 0.20              # unit-to-unit spread of the microphone low-frequency corner, +/-
TOL_63, TOL_8K = 2.5, 5.0  # dB, taken as the class 2 acceptance limits at 63 Hz and 8 kHz (IEC 61672-1 table not re-checked)
C_AIR = 343.0              # m/s
# Processing (level processor, Cortex-M4F class)
FS = 48000                 # Hz sample rate
BIQUADS = {"A weighting": 3, "C weighting": 2, "low-frequency equalizer": 1, "wind band (Z weighted, below 40 Hz)": 1}
CYC_BIQUAD = 14            # cycles per biquad per sample (single precision, direct form)
CYC_CHANNEL = 6            # square, accumulate and Fast exponential average, per channel per sample
CHANNELS = 4               # A, C, A Fast, wind band
CYC_OVERHEAD = 10          # DMA buffer handling per sample
F_CPU = 48e6               # Hz core clock
I_RUN_PER_MHZ = 120e-6     # A per MHz in run mode (STM32L4 class, typical)
I_SLEEP_PERIPH = 1.6e-3    # A in sleep with PLL, SAI or DFSDM and DMA running (assumed)
I_PROC_TRL2 = 5.0e-3       # A, TRL 2 assumption, kept as the upper bound
V_RAIL = 3.3
ETA_RAIL = 0.90            # FieldNode switched rail converter
# FieldNode core (FND-CAL-001 v0.1)
FND_CORE_WH = 0.0040       # Wh/day core consumption at 96 reports
FND_STORED_2PSH = 7.75     # Wh/day stored, worst month (2 peak sun hours)
FND_USABLE = 15.36         # Wh usable in the cell
FND_COLD, FND_EOL = 0.70, 0.80
FND_HOT_CLEAN, FND_HOT_DUSTY = 0.8, 0.3    # Wh stored on a hot clear day without the shield
FND_MASS = 2.45            # kg, base node, FND-CAL-001 v0.3 [F1] (constructable design, FND-DDR-003)
FND_BANDS = 0.08           # kg, FieldNode band clamps (FND-CAL-001 v0.3, bought masses), not fitted on a street pole
FND_WIND_N = 81.0          # N added to the pole by the core at 35 m/s (FND-CAL-001 section D)
FND_ALLOW_MW = 100.0       # FieldNode design sensor allowance (115 mW ceiling)
# The core wakes for each 1 s level frame on the UART
T_FRAME_WAKE = 5e-3        # s overhead per wake
I_CORE_AWAKE = 8e-3        # A (FND-CAL-001)
BAUD, FRAME_BYTES = 9600, 12
# Energy chain for R7 (NoiseMap design case 1.5 peak sun hours)
PANEL_W, PSH, DERATE, ETA_CHG, ETA_CELL = 6.0, 1.5, 0.80, 0.85, 0.95
# Radio: LoRaWAN, 125 kHz, CR 4/5, 8-symbol preamble, explicit header, CRC; 13 bytes of overhead
RECORD_BYTES, LORAWAN_OVH, TS_BYTES = 22, 13, 4
REPORTS = 96
TTN_S = 30.0
# Privacy leak capacity: Codec 2 speech codec, 700 to 3200 bit/s (rowetel.com)
CODEC2_MIN, CODEC2_MAX = 700.0, 3200.0
RAW_BITS = 24
# Reflections
POLE_SOURCES = [5.0, 10.0]           # m, horizontal distance from the microphone to a traffic lane
FACADES = [1.0, 2.0, 5.0, 10.0]     # m, facade behind the microphone
FACADE_REFL = 0.9                    # energy reflection coefficient of a masonry facade (assumed)
# Wind
Q_GUST = 35.0
RHO = 1.225
CD_TUBE, CD_SPHERE = 1.2, 0.5
E_AL, FY_AL = 69e9, 145e6            # Pa, 6063-T5 class (typical)
PRELOAD, MU = 1000.0, 0.2            # N band preload and friction (FND-CAL-001 assumption)
STROUHAL = 0.2
TURB_I = 0.2                          # turbulence intensity at 4 m in a street (assumed)
WIND_FLAG = 5.0                       # m/s, R11 threshold
ANEMO_COST, ANEMO_MASS = 25.0, 0.15   # cup anemometer with pulse output (indicative, unchecked)
# Mass densities (g/cm3) and bought-part masses (kg)
RHO_AL, RHO_ASA, RHO_FOAM, RHO_SS = 2.70, 1.07, 0.030, 7.90
M_MIC, M_PROC, M_CABLE, M_HW = 0.005, 0.010, 0.090, 0.030
MASS_LIMIT = 3.5          # kg, R10 relaxed from 3.0 kg under NSM-DDR-002 (O2 option c)

print("NoiseMap sizing, NSM-CAL-001 v0.3")
print(f"Geometry from cad/src/model.py: pole {P['pole_od']} mm, microphone {P['mic_z']:.0f} mm up and "
      f"{P['mic_off']:.0f} mm off the pole face, arm {D['arm_len']:.0f} mm, head {P['head']} mm")

# ---------------------------------------------------------------- A. Measuring range (R4)
print("\nA. Measuring range")
rng = {}
for name, m in MICS.items():
    n = REF_SPL - m["snr"]
    low = n + db(1 / (10 ** (ERR_LOW / 10) - 1))
    err35 = dbsum(35.0, n) - 35.0
    fs_rms = REF_SPL - m["sens_dbfs"] if m["sens_dbfs"] is not None else m["aop"]
    top = min(m["aop"], fs_rms) + 3.0 - CREST
    rng[name] = (n, low, err35, top)
    tag("A1", f"{name}: self-noise {n:.1f} dBA; lower limit for {ERR_LOW:.0f} dB error {low:.1f} dBA; "
              f"error at 35 dBA {err35:.2f} dB; upper limit {top:.1f} dB (AOP {m['aop']:.0f} dB SPL, crest {CREST:.0f} dB)")
# with noise-floor subtraction, a 1 dB error in the known self-noise
n = rng["ICS-43434"][0]
meas = dbsum(35.0, n)
for dn in (-1.0, 1.0):
    corr = db(10 ** (meas / 10) - 10 ** ((n + dn) / 10))
    tag("A2", f"ICS-43434 at 35 dBA, subtraction with self-noise off by {dn:+.0f} dB: reads {corr:.2f} dBA")
tag("A3", f"Full scale of the ICS-43434: {REF_SPL - MICS['ICS-43434']['sens_dbfs']:.0f} dB SPL rms sine, "
          f"{REF_SPL - MICS['ICS-43434']['sens_dbfs'] + 3:.0f} dB peak")
ics, im = rng["ICS-43434"], rng["IM72D128"]
res("R4", f"ICS-43434 {ics[1]:.1f} to {ics[3]:.0f} dBA; IM72D128 {im[1]:.1f} to {im[3]:.0f} dBA (AOP assumed)",
    "35 to 110 dBA", "At risk (no margin at 35 dBA with ICS-43434; met with IM72D128)")

# ---------------------------------------------------------------- B. Frequency response (R5)
print("\nB. Frequency response")


def hp1(f, fc):
    return db(1 / (1 + (fc / f) ** 2))


fc = MICS["ICS-43434"]["f_lo"]
for f in (31.5, 63.0, 125.0):
    tag("B1", f"First-order roll-off with a {fc:.0f} Hz corner: {hp1(f, fc):.1f} dB at {f:g} Hz")
res63 = [hp1(63, fc * (1 + s)) - hp1(63, fc) for s in (-FC_TOL, FC_TOL)]
res31 = [hp1(31.5, fc * (1 + s)) - hp1(31.5, fc) for s in (-FC_TOL, FC_TOL)]
tag("B2", f"After a fixed equalizer for {fc:.0f} Hz, corner spread +/-{FC_TOL * 100:.0f} %: residual "
          f"{res63[0]:+.1f} / {res63[1]:+.1f} dB at 63 Hz, {res31[0]:+.1f} / {res31[1]:+.1f} dB at 31.5 Hz "
          f"(limit taken as +/-{TOL_63} dB at 63 Hz)")
eq_boost = -hp1(31.5, fc)
tag("B2b", f"Equalizer gain at 31.5 Hz {eq_boost:.1f} dB; the A-weighted self-noise barely changes because "
           f"A weighting is -39.4 dB there")
# Helmholtz resonance of the acoustic port and front cavity
a = math.pi * (P["port_d"] / 2e3) ** 2
l_eff = P["top_t"] / 1e3 + 1.7 * P["port_d"] / 2e3
vol = math.pi * (P["cavity"][0] / 2e3) ** 2 * P["cavity"][1] / 1e3
f0 = C_AIR / (2 * math.pi) * math.sqrt(a / (vol * l_eff))
rise8 = 20 * math.log10(1 / (1 - (8000 / f0) ** 2))
tag("B3", f"Port {P['port_d']} mm x {P['top_t']} mm, front cavity {P['cavity'][0]} x {P['cavity'][1]} mm: "
          f"Helmholtz resonance {f0 / 1e3:.1f} kHz; undamped rise at 8 kHz {rise8:.2f} dB (limit {TOL_8K} dB)")
f0_long = C_AIR / (2 * math.pi) * math.sqrt(a / (vol * 10 * (3e-3 + 1.7 * P["port_d"] / 2e3)))
tag("B3b", f"For comparison, a 3 mm port with a ten times larger cavity resonates at {f0_long / 1e3:.1f} kHz "
           f"(rise at 8 kHz {20 * math.log10(1 / (1 - (8000 / f0_long) ** 2)):.1f} dB): keep the cavity small")
res("R5", f"Roll-off {hp1(63, fc):.1f} dB at 63 Hz before equalizing; residual {max(map(abs, res63)):.1f} dB after; "
          f"port resonance {f0 / 1e3:.0f} kHz (+{rise8:.1f} dB at 8 kHz); membrane and head diffraction unknown",
    "A and C weighting within class 2 limits, 63 Hz to 8 kHz", "At risk (membrane, windscreen and head diffraction not verifiable at TRL 3)")

# ---------------------------------------------------------------- C. Accuracy and reflections (R3)
print("\nC. Reflections")
r_pole = P["pole_od"] / 2e3
s = P["mic_off"] / 1e3
amp = math.sqrt((r_pole / 2) / (s + r_pole / 2))
tag("C1", f"Pole {P['pole_od']} mm at {s:.2f} m: reflected energy {amp ** 2 * 100:.1f} % of direct, "
          f"+{db(1 + amp ** 2):.2f} dB (geometric, incoherent)")
worst_facade = 0.0
for fac in FACADES:
    out = []
    for src in POLE_SOURCES:
        refl = src + 2 * fac
        pt = db(1 + FACADE_REFL * (src / refl) ** 2)
        ln = db(1 + FACADE_REFL * (src / refl))
        worst_facade = max(worst_facade, pt, ln)
        out.append(f"lane {src:g} m: point +{pt:.1f}, line +{ln:.1f} dB")
    tag("C2", f"Facade {fac:g} m behind the microphone: " + "; ".join(out))
budget = {"calibrator (94 dB, class 1)": 0.4, "microphone drift between checks": 0.5,
          "windscreen insertion loss after correction": 0.5, "frequency response residual (traffic spectrum)": 0.7,
          "facade and pole reflections after a site correction": 1.0}
rss = math.sqrt(sum(v ** 2 for v in budget.values()))
tag("C3", "Uncertainty budget (assumed standard values, dB): " + "; ".join(f"{k} {v}" for k, v in budget.items()))
tag("C3b", f"Combined {rss:.2f} dB; expanded (k = 2) {2 * rss:.1f} dB against +/-2 dB; worst uncorrected facade bias +{worst_facade:.1f} dB")
res("R3", f"Expanded uncertainty {2 * rss:.1f} dB (assumed terms); facade bias up to +{worst_facade:.1f} dB before a site correction",
    "+/-2 dB from 40 to 100 dBA after field calibration", "At risk")

# ---------------------------------------------------------------- D. Processing and power (R7)
print("\nD. Processing and power")
cyc = sum(BIQUADS.values()) * CYC_BIQUAD + CHANNELS * CYC_CHANNEL + CYC_OVERHEAD
load = cyc * FS / F_CPU
i_run = I_RUN_PER_MHZ * F_CPU / 1e6
i_proc = load * i_run + (1 - load) * I_SLEEP_PERIPH
tag("D1", f"{sum(BIQUADS.values())} biquads and {CHANNELS} channels: {cyc} cycles per sample, "
          f"{cyc * FS / 1e6:.2f} M cycles/s, {load * 100:.1f} % of {F_CPU / 1e6:.0f} MHz; at 32 kHz {cyc * 32000 / 1e6:.2f} M cycles/s")
tag("D2", f"Processor {i_run * 1e3:.2f} mA running, {I_SLEEP_PERIPH * 1e3:.1f} mA in sleep with DMA: average {i_proc * 1e3:.2f} mA")
core_uart = (FRAME_BYTES * 10 / BAUD + T_FRAME_WAKE) * I_CORE_AWAKE * V_RAIL
core_mw = FND_CORE_WH / 24 * 1e3
loads = {}
for name, m in MICS.items():
    head = (i_proc + m["i_ma"] / 1e3) * V_RAIL
    loads[name] = head / ETA_RAIL * 1e3 + core_uart * 1e3 + core_mw
    tag("D3", f"{name}: head {head * 1e3:.1f} mW at the rail, {head / ETA_RAIL * 1e3:.1f} mW from the cell; "
              f"core UART wake {core_uart * 1e3:.2f} mW; core {core_mw:.2f} mW; total {loads[name]:.1f} mW, "
              f"{loads[name] * 24 / 1e3:.3f} Wh/day")
upper = (I_PROC_TRL2 + 1.0e-3) * V_RAIL / ETA_RAIL * 1e3 + core_uart * 1e3 + core_mw
design = max(loads.values())
tag("D4", f"Upper bound with the TRL 2 processor current (5 mA) and a 1 mA microphone: {upper:.1f} mW, {upper * 24 / 1e3:.3f} Wh/day")
tag("D5", f"Design load {design:.1f} mW is {design / FND_ALLOW_MW * 100:.0f} % of the FieldNode 100 mW design allowance")

print("\nE. Energy")
harvest = PANEL_W * PSH * DERATE * ETA_CHG * ETA_CELL
wh_d, wh_u = design * 24 / 1e3, upper * 24 / 1e3
tag("E1", f"Harvest at {PSH} peak sun hours: {harvest:.2f} Wh/day stored; {harvest / wh_d:.0f} times the design load, "
          f"{harvest / wh_u:.0f} times the upper bound; FieldNode worst month (2 h) {FND_STORED_2PSH} Wh/day")
aut = {k: FND_USABLE * f / wh_d for k, f in (("nominal", 1.0), ("-20 C", FND_COLD), ("end of life", FND_EOL))}
aut_u = FND_USABLE * FND_COLD * FND_EOL / wh_u
tag("E2", "Autonomy at the design load: " + ", ".join(f"{k} {v:.0f} days" for k, v in aut.items())
    + f"; upper bound, cold and aged {aut_u:.0f} days; nominal upper bound {FND_USABLE / wh_u:.0f} days")
tag("E3", f"Hot clear day without the FieldNode shield: stored {FND_HOT_CLEAN} Wh clean, {FND_HOT_DUSTY} Wh dusty, "
          f"against {wh_d:.2f} Wh (design) and {wh_u:.2f} Wh (upper bound)")
res("R7", f"{harvest:.2f} Wh/day stored at 1.5 h against {wh_d:.2f} Wh/day ({wh_u:.2f} upper bound); "
          f"{aut['nominal']:.0f} days without sun ({aut_u:.0f} cold, aged, upper bound)",
    "Energy neutral at 1.5 peak sun hours; 14 days without sun", "Met on paper")

# ---------------------------------------------------------------- F. Data, radio and privacy (R1, R2, R6, R12)
print("\nF. Data, radio and privacy")
tag("F1", f"Record: 15 one-minute LAeq + LAeq,15min, LAFmax, LAFmin, L10, L90, LCeq + status = {15 + 6 + 1} bytes; "
          f"1 byte at 0.5 dB steps spans 20.0 to {20 + 0.5 * 255:.1f} dB")
res("R2", f"{15 + 6 + 1} bytes per 15 min; wind flag and flagged-minute count in the status byte",
    "1-minute LAeq, LAeq, LAFmax, LAFmin, L10, L90, LCeq, status per 15 min", "Met by design")


def toa(payload, sf, bw=125e3, cr=1, pre=8):
    ts = 2 ** sf / bw
    de = 1 if sf >= 11 else 0
    n = 8 + max(math.ceil((8 * payload - 4 * sf + 28 + 16) / (4 * (sf - 2 * de))) * (cr + 4), 0)
    return (pre + 4.25) * ts + n * ts


phy = RECORD_BYTES + LORAWAN_OVH
air = {}
for sf in range(7, 13):
    t = toa(phy, sf)
    air[sf] = t
    tag("F2", f"SF{sf}: {t * 1e3:.1f} ms per uplink, {t * REPORTS:.1f} s/day at 15 min, shortest interval within "
              f"{TTN_S:.0f} s/day {math.ceil(t * 1440 * 60 / TTN_S / 60)} min, EU868 1 % off-time {t * 99:.0f} s")
tag("F2b", f"Stored record with a {TS_BYTES}-byte time stamp: {toa(phy + TS_BYTES, 9) * 1e3:.1f} ms at SF9")
# Interval rule (NSM-DDR-002, O4): the core lengthens the interval automatically at slow data rates so that
# airtime stays within fair use; 15 min is kept where it fits. The 15 sub-interval LAeq values then span interval/15.
interval = {sf: max(15, math.ceil(t * 1440 * 60 / TTN_S / 60)) for sf, t in air.items()}
rule_air = {sf: air[sf] * 1440 / interval[sf] for sf in air}
for sf in range(7, 13):
    tag("F2c", f"Interval rule, SF{sf}: {interval[sf]} min, {rule_air[sf]:.1f} s/day, {1440 // interval[sf]} records a day, "
               f"sub-interval LAeq over {interval[sf] / 15:.1f} min")
worst_rule = max(rule_air.values())
res("R12", f"15 min at SF7 to SF9 ({air[9] * REPORTS:.1f} s/day at SF9); interval rule {interval[10]}, {interval[11]} and {interval[12]} min "
           f"at SF10 to SF12 (at most {worst_rule:.1f} s/day); 1 % duty cycle met at all SF",
    "EU868 1 % duty cycle and 30 s/day fair use", "Met on paper (with the interval rule of NSM-DDR-002)")
raw = FS * RAW_BITS
uart = BAUD * 8 / 10
lev = FRAME_BYTES * 10
tag("F3", f"Raw audio {raw / 1e6:.3f} Mbit/s; UART payload capacity {uart:.0f} bit/s ({raw / uart:.0f} times too slow for raw audio); "
          f"level frames use {lev / BAUD * 100:.2f} % of the line; Codec 2 needs {CODEC2_MIN:.0f} to {CODEC2_MAX:.0f} bit/s, "
          f"which the line could carry")
bits9 = TTN_S / air[9] * RECORD_BYTES * 8
bits7 = 0.01 * 86400 / air[7] * RECORD_BYTES * 8
tag("F4", f"Radio capacity: {bits9 / 1e3:.1f} kbit/day at SF9 under fair use = {bits9 / CODEC2_MIN:.0f} s of 700 bit/s speech a day; "
          f"{bits7 / 1e6:.2f} Mbit/day at SF7 under the 1 % duty cycle = {bits7 / CODEC2_MIN / 60:.0f} min a day")
res("R1", "Head has no data storage or radio; firmware sends levels only; cable could carry a speech codec, radio a few minutes a day",
    "No audio stored or sent; head firmware published with a build hash", "Met by design (rests on firmware, not physics)")
res("R6", "Network time via LoRaWAN DeviceTimeReq; records stamped at the core; stored records carry a 4-byte time",
    "Within 2 s of UTC", "Met by design")

# ---------------------------------------------------------------- G. Wind and rain flagging (R11)
print("\nG. Wind and rain flagging")
for u in (2.0, 5.0, 10.0):
    p_turb = RHO * u * TURB_I * u
    tag("G1", f"{u:g} m/s: unscreened turbulent pressure about {p_turb:.2f} Pa rms, {20 * math.log10(p_turb / 20e-6):.0f} dB, mostly below 20 Hz")
tag("G2", f"Wind noise scales about as U^4 in power: 2 to 5 m/s adds {40 * math.log10(5 / 2):.1f} dB; "
          f"a 1 m/s error at 5 m/s is {40 * math.log10(6 / 5):.1f} dB of band level")
res("R11", "Wind: level-based flag (Z weighted band below 40 Hz and its 1 s spread) against a threshold set in the field; rain: server flag from weather data",
    "Flag intervals with wind above 5 m/s or heavy rain", "Not verifiable at TRL 3 (method chosen; threshold needs field data, on hold with TRL 4)")

# ---------------------------------------------------------------- H. Mechanics (R10)
print("\nH. Mechanics")
C = build_components()
KG = {"al": RHO_AL / 1e6, "ss": RHO_SS / 1e6, "asa": RHO_ASA / 1e6, "foam": RHO_FOAM / 1e6, "nylon": 1.15e-6}  # kg/mm3
V = lambda *ks: sum(C[k].shape.volume for k in ks)  # noqa: E731
m_add = {
    "arm saddle, tube, flange and fixings": V("saddle", "tube", "flange") * KG["al"] + V("flange_fix") * KG["ss"],
    "arm bands and lanyard": V("s_bands", "lanyard") * KG["ss"],
    "head housing, cap and bolts": V("head", "cap") * KG["asa"] + V("head_bolt", "cap_screws") * KG["ss"],
    "microphone and processor boards": M_MIC + M_PROC,
    "windscreen and spike": V("windscreen") * KG["foam"] + V("spike") * KG["ss"],
    "sensor cable and gland": M_CABLE + V("gland") * KG["nylon"],
    "street pole V-blocks and screws": V("vblock_low", "vblock_up") * KG["al"] + V("vb_screws") * KG["ss"],
    "street pole bands": V("vb_bands") * KG["ss"],
    "ties, tape and small parts": M_HW,
}
# FieldNode core on a street pole: the base node of FND-CAL-001 v0.3 [F1] less its small-pole
# V-blocks and bands, which NoiseMap leaves off (NSM-DDR-003)
import fieldnode_core as fnc  # noqa: E402
_fc = fnc.build_components()
fn_vb = (_fc["vblock_low"].shape.volume + _fc["vblock_up"].shape.volume) * KG["al"]
FND_STREET = FND_MASS - fn_vb - FND_BANDS
m_total = FND_STREET + sum(m_add.values())
tag("H1", "Added to FieldNode: " + "; ".join(f"{k} {v:.3f} kg" for k, v in m_add.items()))
tag("H2", f"FieldNode core {FND_MASS} kg less its V-blocks {fn_vb:.3f} kg and bands {FND_BANDS} kg = {FND_STREET:.2f} kg; "
          f"+ NoiseMap {sum(m_add.values()):.2f} kg = {m_total:.2f} kg against {MASS_LIMIT} kg")
v_full = V("vblock_low", "vblock_up") / P["vb"][2] * 20.0
holes = 8 * math.pi / 4 * P["vb_hole_d"] ** 2 * P["vb"][2]
tag("H2b", f"V-blocks: 16 mm bar instead of 20 mm and four 14 mm holes each save "
           f"{((v_full + holes * 20 / P['vb'][2]) - V('vblock_low', 'vblock_up')) * KG['al']:.3f} kg; saddle in 2.5 mm sheet")
q = 0.5 * RHO * Q_GUST ** 2
ao, aw = P["arm"][0] / 1e3, P["arm"][1] / 1e3
L = D["arm_len"] / 1e3
hd = P["head"][0] / 1e3
head_exposed = (P["head"][2] - P["ws_d"] / 2) / 1e3
f_arm = q * CD_TUBE * ao * L
f_head = q * CD_TUBE * hd * head_exposed
f_ws = q * CD_SPHERE * math.pi * (P["ws_d"] / 2e3) ** 2
tag("H3", f"q = {q:.0f} Pa at {Q_GUST:.0f} m/s: arm {f_arm:.1f} N, head tube {f_head:.1f} N, windscreen {f_ws:.1f} N")
x_tip = L
m_wind = f_arm * L / 2 + (f_head + f_ws) * x_tip
m_head = (m_add["head housing, cap and bolts"] + M_MIC + M_PROC + m_add["windscreen and spike"])
m_tube = math.pi / 4 * (ao ** 2 - (ao - 2 * aw) ** 2) * L * RHO_AL * 1e3
m_grav = 9.81 * (m_head * x_tip + m_tube * L / 2)
m_comb = math.hypot(m_wind, m_grav)
Z = math.pi * (ao ** 4 - (ao - 2 * aw) ** 4) / (32 * ao)
I = Z * ao / 2
sigma = m_comb / Z
tag("H4", f"Arm root: wind {m_wind:.2f} N m, weight {m_grav:.2f} N m, combined {m_comb:.2f} N m; "
          f"Z = {Z * 1e9:.0f} mm3; stress {sigma / 1e6:.1f} MPa; factor on yield {FY_AL / sigma:.0f}")
k = 3 * E_AL * I / L ** 3
m_eff = m_head + 0.24 * m_tube
fn = math.sqrt(k / m_eff) / (2 * math.pi)
defl = (f_head + f_ws) * L ** 3 / (3 * E_AL * I) + f_arm * L ** 3 / (8 * E_AL * I)
tag("H5", f"Arm stiffness {k / 1e3:.1f} kN/m, tip deflection in the gust {defl * 1e3:.2f} mm; first mode {fn:.0f} Hz; "
          f"vortex shedding matches it at {fn * ao / STROUHAL:.1f} m/s on the arm and {fn * hd / STROUHAL:.1f} m/s on the head")
twist = f_arm * (D["r"] / 1e3 + L / 2) + (f_head + f_ws) * (D["r"] / 1e3 + L)
N_ARM_BANDS = 2                       # two bands on the arm saddle (NSM-DDR-003)
cap = N_ARM_BANDS * MU * 2 * PRELOAD * D["r"] / 1e3
m_arm = m_add["arm saddle, tube, flange and fixings"] + m_add["arm bands and lanyard"]
tag("H6", f"Twist on the arm clamp {twist:.2f} N m against {cap:.1f} N m of friction from two bands (factor {cap / twist:.1f}); "
          f"slip {9.81 * (m_head + m_arm):.1f} N against {N_ARM_BANDS * MU * 2 * PRELOAD:.0f} N")
tag("H7", f"Load added to the pole: FieldNode {FND_WIND_N:.0f} N + NoiseMap {f_arm + f_head + f_ws:.0f} N = {FND_WIND_N + f_arm + f_head + f_ws:.0f} N at about 3.5 to 4 m")
for dpole in P["pole_range"]:
    rr = dpole / 2
    t = rr / math.sqrt(2)
    band = 1.5 * math.pi * rr + 2 * P["vb"][1] + 2 * P["band_slot_x"]
    tag("H8", f"Pole {dpole:.0f} mm: V contacts {t:.1f} mm either side of the centre line (V-block mouth half width "
              f"{D['v_half_mouth']:.1f} mm, saddle {D['s_half_mouth']:.1f} mm); adapter band about {band:.0f} mm")
tag("H8b", f"Largest pole whose contacts stay 3 mm inside both mouths: {min(D['max_pole_vb'], D['max_pole_saddle']):.0f} mm")
mass_ok = m_total <= MASS_LIMIT
res("R10", f"{m_total:.2f} kg with the constructable adapter and saddle; arm factor {FY_AL / sigma:.0f} on yield; clamp twist factor {cap / twist:.1f}; fits 60 to 140 mm poles",
    f"{MASS_LIMIT} kg or less; 35 m/s gusts; two people in 45 min",
    (f"Met on paper on mass ({m_total:.2f} kg, margin {MASS_LIMIT - m_total:.2f} kg)" if mass_ok else f"Not met on mass ({m_total:.2f} kg)")
    + "; wind met on paper; install time not verifiable at TRL 3")

# ---------------------------------------------------------------- I. Cost (R13)
print("\nI. Cost")
bom = list(csv.DictReader((ROOT / "bom/bom.csv").open()))
cost = {int(r["item"].split()[0]): float(r["qty"]) * float(r["unit_cost_usd"]) for r in bom}
core = sum(v for k, v in cost.items() if k <= 6)
own = sum(v for k, v in cost.items() if k > 6)
budget_usd = yaml.safe_load((ROOT / "project.yaml").read_text())["budget_usd"]
tag("I1", f"{len(bom)} BOM lines, all priced: FieldNode core (lines 1 to 6) ${core:.2f}; NoiseMap parts (lines 7 to 14) ${own:.2f}; full node ${core + own:.2f}")
tag("I2", f"Value-engineering target (budget_usd, a hypothetical control target, not a limit): USD {budget_usd}. "
          f"Estimated cost of the constructable NoiseMap parts: USD {own:.2f} (USD {budget_usd - own:.2f} under the target); "
          f"the full node with the FieldNode core is USD {core + own:.2f}")
tag("I3", f"Rejected option (NSM-DDR-002, O3) with a cup anemometer for R11: NoiseMap parts ${own + ANEMO_COST:.2f}, mass {m_total + ANEMO_MASS:.2f} kg")
res("R13", f"NoiseMap parts ${own:.2f}; full node ${core + own:.2f} with the FieldNode core (${core:.2f})",
    f"NoiseMap parts at or under the ${budget_usd} value-engineering target; FieldNode core costed in FieldNode",
    f"Met on paper (USD {budget_usd - own:.2f} under the value-engineering target)")

# ---------------------------------------------------------------- J. Items settled by design or only by test
res("R8", "FieldNode IP65 core; head with drip skirt, hydrophobic membrane and bored windscreen; IM72D128 is IP57 at part level",
    "IP65; head survives driving rain; -20 to +50 C", "Not verifiable at TRL 3 (by design)")
res("R9", "Calibrator slides over the head after the windscreen is removed; offset stored in the head",
    "Field check in 10 min or less; offset stored", "Not verifiable at TRL 3 (timed trial)")
res("R14", "ASA housing, UV-stabilized foam changed yearly, FieldNode cell swap",
    "5 years with yearly windscreen and one battery change", "Not verifiable at TRL 3")
res("R15", "CERN-OHL-S-2.0 and MIT; calibration method and record format in NSM-CAL-001", "All published", "Met by design")

order = {"Not met": 0, "At risk": 1, "Not verifiable": 2, "Met on paper": 3, "Met by design": 4}
rows.sort(key=lambda r: (min(v for k, v in order.items() if r[3].startswith(k)), int(r[0][1:])))
print("\nL. Results")
with (ROOT / "docs/04-calcs/results.csv").open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "value", "target", "status"])
    for r in rows:
        w.writerow(r)
        tag("L", f"{r[0]:4s} {r[3]}: {r[1]}")
counts = {}
for r in rows:
    key = next(k for k in order if r[3].startswith(k))
    counts[key] = counts.get(key, 0) + 1
tag("L2", ", ".join(f"{v} {k.lower()}" for k, v in counts.items()) + f"; {len(rows)} requirements")
