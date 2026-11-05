---
doc_id: NSM-STM-001
title: NoiseMap STEM check
project: NoiseMap
doc_type: STEM check
version: "0.1"
status: Draft
date: '2026-11-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-11-02'
  author: Amish Chadha
  change: First STEM check (kit 1.8 pipeline) of the current design (option A) and the claims that set options B and C apart
---

# NoiseMap STEM check

Verdict: all 24 claims sit within known science; 21 are within it outright and 3 (S2, the loudest level; S12, the mass margin; S13, reflections) are plausible and closed by NSM-CAL-001; no row fails. The independent review found two problems that were fixed under Amish's standing instruction of 2026-10-23 (the microphone fitted by default, and sealing of stainless-to-aluminium joints, NSM-DEC-001) and two that change requirements and go to Amish (PR-003 is not met on paper; PR-002 and PR-012 at slow data rates). The privacy promise is not a row: the physics is S9 (the cable is too slow for raw audio) and the promise rests on open firmware (NSM-DDR-001 D2). Method and rules: STANDARDS section 20. Calculations: `docs/04-calcs/stem_check.py`, results in `docs/04-calcs/stem_results.csv`. The detailed numbers are in NSM-CAL-001; this check is a first-order screen of each claim and does not replace it.

## Claims checked

Table 1. Claims, governing science and verdicts. S1 to S19 are option A (the current design) and, where noted, also hold for C; S20 to S22 set option B apart and S23 and S24 set option C apart. Requirement numbers (PR-xxx) are in NSM-PRS-001.

| # | Claim (number and unit) | Field | Branch | Governing law or source | First-order check | Verdict | Closed by |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | Quietest level the microphone resolves: 35 dBA with 1 dB error (IM72D128 fitted by default, 72 dB(A) SNR re 94 dB SPL) | Physics | Acoustics and vibration | Self-noise = 94 dB SPL - SNR = 22 dBA; power subtraction error at 35 dBA (CAL A1). The ICS-43434 alternative has 34.9 dBA and no margin | 27.9 dBA (lower limit for 1 dB error) <= 35 dBA (lower limit for 1 dB error) | Within known science | NSM-CAL-001 A1; microphone choice NSM-DEC-001 (2026-11-02) |
| S2 | Loudest level before clipping: 110 dBA for traffic (IM72D128, overload point 126 dB SPL at 1 % THD) | Physics | Acoustics and vibration | Peak limit: 126 dB SPL + 3 dB peak/rms - 10 dB crest = 119 dB SPL unweighted; an A-weighted traffic level is 5 to 10 dB lower (mid 7.5 dB); Infineon IM72D128V01 product brief | 111.5 dBA (ceiling, mid case) >= 110 dBA (ceiling, mid case) | **Plausible, to confirm at TRL 3** | NSM-CAL-001 A4 (109 to 114 dBA); the ICS-43434 alternative gives 103 to 108 dBA and misses 110 dBA, so the IM72D128 is fitted by default (NSM-DEC-001) |
| S3 | A- and C-weighted levels computed in the head from 48 kHz samples cover the 20 kHz audio band | Mathematics | Numerical method | Nyquist: the sample rate must exceed twice the highest frequency (24 kHz) | 20 kHz <= 24 kHz | Within known science |  |
| S4 | Level processor load: 132 cycles per sample at 48 kHz on a 48 MHz Cortex-M4F is 13 % of the core | Engineering and technology | Sensing resolution and control | Cycle budget = cycles per sample x sample rate (CAL F1) | 6.336 Mcycles/s <= 48 Mcycles/s | Within known science |  |
| S5 | Solar harvest of 5.81 Wh/day stored from a 6 W panel at 1.5 peak sun hours | Physics | Thermodynamics | Energy = rated power x peak sun hours at 1000 W/m2 (cannot exceed 9.0 Wh) | 5.81 Wh/day <= 9 Wh/day | Within known science |  |
| S6 | Autonomy of 53 days without sun on one 3.2 V, 6 Ah LiFePO4 cell at 0.29 Wh/day | Chemistry | Electrochemistry and batteries | Stored energy 19.2 Wh x 80 % usable divided by the daily load (CAL E2); 52.9 days rounds to 53 | claimed 53 days, estimate 53 days (ratio 1.00) | Within known science |  |
| S7 | LoRaWAN airtime 23.7 s/day at SF9 and 15 minute records (22 byte payload, 13 byte MAC overhead) | Engineering and technology | Power and link budgets | Semtech AN1200.13 time on air, 96 uplinks a day | claimed 23.7 s/day, estimate 23.7 s/day (ratio 1.00) | Within known science |  |
| S8 | Duty cycle: one SF9 uplink needs a quiet interval of 99 x airtime; the 15 minute interval is longer | Engineering and technology | Standards practice | ETSI EN 300 220 sub-band limit of 1 % duty cycle for EU868 (cited in NSM-REQ-001 R12) | 24.4316 s between uplinks <= 900 s between uplinks | Within known science |  |
| S9 | The 9,600 baud head-to-core cable is about 150 times too slow for raw 24-bit, 48 kHz audio | Engineering and technology | Power and link budgets | Raw bit rate / UART payload rate (8N1 is 80 % efficient) | claimed 150 x, estimate 150 x (ratio 1.00) | Within known science |  |
| S10 | Wind load of about 96 N on the whole node in a 35 m/s gust | Physics | Fluid mechanics | Drag F = 1/2 rho v^2 Cd A with Cd 1.2 and the projected areas of panel, box, windscreen and arm | claimed 96 N, estimate 100 N (ratio 0.96) | Within known science |  |
| S11 | Arm bending stress under a 35 m/s gust (4.10 N.m at the arm root: wind on arm, head and windscreen 14.8 N, plus weight) | Physics | Strength of materials | Cantilever bending, sigma = M/Z (CAL H3, H4); 6063-T5/T6 aluminium yield about 145 to 215 MPa (taken as 145); stress concentration at the flange screw holes (Kt 2 to 3) still leaves a factor of 9 or more | 5.32291 MPa <= 145 MPa | Within known science |  |
| S12 | Mass on the pole of 3.5 kg or less (R10): model mass of the constructable design | Physics | Mechanics and statics | Sum of part volumes x density from the model (cad/fidelity.json) | 3.45 kg <= 3.5 kg | **Plausible, to confirm at TRL 3** | NSM-CAL-001 H2 and cad/fidelity.json; margin 0.05 kg accepted 2026-10-02 (NSM-DDR-003 A2) |
| S13 | Reflections bias a level by up to 2.4 dB from one facade and up to 2.7 dB in a street canyon (A and C) | Physics | Acoustics and vibration | Incoherent reflection of a line source from one or two facades (CAL C2, C2c); a single coherent reflection cannot exceed +6.02 dB, but several reflections can, so the bound is a screen only | 2.7 dB <= 6.021 dB | **Plausible, to confirm at TRL 3** | NSM-CAL-001 C2 and C2c; the per-deployment site correction (NSM-DDR-001 D7) sets the real figure |
| S14 | Expanded uncertainty (k = 2) of 2.9 dB against a 2 dB target (R3, at risk) | Mathematics | Statistics and uncertainty | Root sum of squares of the CAL C3 terms; k = 2 gives about 95 % coverage (GUM, JCGM 100:2008). The arithmetic holds; the result (3.1 dB with the reference meter) is above the 2 dB target, so PR-003 is not met on paper | claimed 2.9 dB, estimate 2.94 dB (ratio 0.99) | Within known science |  |
| S15 | Stainless bands and screws on aluminium blocks do not corrode the blocks over the service life | Chemistry | Electrochemistry and batteries | Galvanic couple (ASTM G82 galvanic series): stainless is the cathode, aluminium the anode. Screening by area ratio is optimistic in a wet salt film (review finding); crevice corrosion under bands and in tapped holes is the likelier failure | Screw threads and the band contact faces are sealed with the neutral-cure silicone already in BOM line 13 (fix under the standing instruction, NSM-DEC-001); the 5 year life stays a TRL 4 salt-spray test (PR-014) | Within known science | NSM-DEC-001 (sealing of stainless-to-aluminium joints) |
| S16 | Printed ASA head and UV-stabilized foam survive 5 years outdoors with a yearly foam change | Chemistry | Materials and polymer chemistry | ASA is the UV-resistant member of the styrenic family (acrylate rubber, no butadiene double bonds); foam is replaced yearly | Qualitative; the 5 year life is a TRL 4 test (R14), no number is claimed | Within known science |  |
| S17 | Cell is charged only inside the maker's limits (0 to 45 C) and discharged to -20 C with reduced capacity | Chemistry | Electrochemistry and batteries | LiFePO4 cells plate lithium if charged below 0 C; FieldNode's core has a cold-charge lockout; capacity falls in the cold (CAL E2: 37 days at -20 C) | Lockout is a FieldNode design item (FND-CAL-001); NoiseMap adds no charging | Within known science |  |
| S18 | LoRa link to a gateway 1 km away across an urban street (14 dBm, SF9 sensitivity about -129 dBm) | Physics | Electromagnetism and circuits | Okumura-Hata urban path loss for a 30 m gateway and 4 m node (about 120 dB) against the 143 dB available; 23 dB of margin | 119.662 dB loss <= 143 dB loss | Within known science |  |
| S19 | Field check with a 94 dB, 1 kHz calibrator is safe: 2 minutes of exposure | Biology | Human physiology and biomechanics | NIOSH recommended exposure limit 85 dBA for 8 h with a 3 dB exchange rate: 60 min at 94 dBA | 2 min <= 60 min | Within known science |  |
| S20 | B: a Wi-Fi microphone node draws about 0.6 W from a 5 V, 1 A USB supply (about 120 mA average) | Physics | Electromagnetism and circuits | P = V I; a 2.4 GHz module averages 80 to 150 mA with periodic transmit (datasheet class, estimate) | 0.6 W <= 5 W | Within known science |  |
| S21 | B: Wi-Fi link from the balcony to the router 10 m away through one wall (20 dBm, -90 dBm sensitivity) | Physics | Electromagnetism and circuits | Free-space loss at 2437 MHz plus 10 dB wall allowance (estimate) | 70.1771 dB loss available <= 110 dB loss available | Within known science |  |
| S22 | B: two bands (1,000 N preload, friction 0.2) hold a 0.95 kg box on a vertical post in a 35 m/s gust | Physics | Mechanics and statics | Coulomb friction on the V faces: capacity 2 x 1000 N x 0.2 x sqrt(2), the friction value of NSM-CAL-001 | 14.2716 N <= 565.7 N | Within known science |  |
| S23 | C: the node takes about 0.7 W from the luminaire (0.5 W load through a 70 % efficient converter), 6 kWh a year | Physics | Thermodynamics | Input power = load / efficiency; a small isolated converter is 60 to 80 % efficient (datasheet class, estimate) | 0.714286 W (a design ceiling) <= 1 W (a design ceiling) | Within known science |  |
| S24 | C: a microphone 6 m up reads about 0.8 dB less than one at 4 m for a road 5 m away (line source) | Physics | Acoustics and vibration | Geometric spreading from a line source, 10 log(r2/r1), source height 0.5 m | 0.85603 dB (change in level) <= 1.5 dB (change in level) | Within known science |  |

Verdicts: **Within known science**, **Plausible, to confirm at TRL 3**, **Fails, fix proposed**, **Fails**. Rows that bear on a product requirement: S1 and S2 on PR-004, S5 and S6 on PR-007, S7 and S8 on PR-012, S9 on PR-001, S10 to S12 on PR-010, S13 and S14 on PR-003, S19 on PR-009 (the calibrator check). The public notice (PR-016) and falling-part lanyard (PR-017) carry no physical claim beyond S10 and S11.

## Fields not relevant

- Nuclear and ionising radiation (Physics): the node has no source and is not shielded for one.
- Optics and radiation (Physics): the only light is the panel's sunlight (S5) and the status light; no laser or UV source.
- Organic, inorganic and analytical chemistry beyond the cell and the galvanic couple (Chemistry): there are no reagents, no emissions and no dosing. The foam, ASA and silicone are inert in use (S16).
- Biology beyond hearing safety (S19): no living material, no sampling. A bird spike deters perching and does not harm birds, as a blunt-tipped 3 mm rod; the effect on birds is soft wording and not claimed as a result. Health claims are non-clinical: the node measures a nuisance, it does not assess anyone's health.
- Control (Engineering): there is no feedback loop; the only firmware logic is filtering and counting (S4).

## Concept options

- **Option A, pole clamp node (the current design):** S1 to S19 pass. Three plausible rows are closed by NSM-CAL-001. Carried forward.
- **Option B, balcony post node:** S20 (power), S21 (Wi-Fi link) and S22 (clamp hold) pass with wide margins. Its working principle (microphone, processor and radio on one board, powered over USB, home Wi-Fi) is sound. It inherits S1 to S3, S13 and S14 from A, since the microphone and level processing are the same.
- **Option C, luminaire socket node:** S23 (power draw) and S24 (height effect) pass. It inherits S1 to S3, S7 to S9, S13 and S14 from A. Whether mains voltage can be kept isolated inside a sealed puck is a design and certification matter, not a STEM row (NSM-REG-001 G12).
- No option fails. Option C's isolation question needs a qualified reviewer before any product claim (NSM-REG-001 G12).

## Independent review

One reviewer (Claude Opus 5.5, run headless with `claude -p`, no tools but Read) saw only this STEM check, NSM-CAL-001, NSM-PRS-001 and `sizing.py`, not the author's reasoning, and tried to refute every "Within known science" verdict and the headline results. Method: STANDARDS section 20. Its findings and what changed:

Table 2. Independent review findings and dispositions.

| # | Finding (reviewer) | Severity | Disposition |
| --- | --- | --- | --- |
| 1 | The 113 dB ceiling (S2, range) is an unweighted level; for a traffic spectrum the A-weighted ceiling is about 103 to 108 dBA, below the 110 dBA target, and "113 <= 120" tested nothing | Fails (for the ICS-43434) | Accepted. Fix under Amish's standing instruction of 2026-10-23: the IM72D128 (overload point 126 dB SPL at 1 % THD, Infineon product brief read 2026-11-02) is the microphone fitted by default on the existing dual-footprint adapter board, giving 109 to 114 dBA; NSM-CAL-001 A4 added; S2 restated and closed by A4 and the decision (NSM-DEC-001). PR-004 stays at risk. The price of line 9 is to confirm |
| 2 | S13: 2.4 dB is one facade; a street canyon has more reflections, and the 6 dB bound holds only for one coherent reflection | Weak verdict | Accepted. S13 is now Plausible, closed by NSM-CAL-001 C2c (canyon +2.7 dB) and the per-deployment site correction |
| 3 | S14: the arithmetic holds but 2.9 dB is above the 2 dB target, and the budget omits the reference meter (about 3.1 dB with it) | Weak verdict | Accepted. PR-003 is restated as not met on paper (NSM-CAL-001 C3c). Relaxing the target or cutting the terms changes the requirement, so it goes to Amish |
| 4 | S12: the 0.05 kg margin is 1.4 % of an estimate; the 0.144 kg appears twice in the mass list | Weak verdict | Kept Plausible. The CAD model, which sums part volumes times density independently of the hand list, also gives 3.45 kg (cad/fidelity.json, rounded to 3.5 kg). The repeated 0.144 kg is not resolved by this review and is left for TRL 4 weighing. The margin was accepted on 2026-10-02 (NSM-DDR-003 A2) |
| 5 | S10, S11 and CAL disagree (97 N and 96 N; 16 N and 14.8 N; 7.96 and 5.3 MPa) | Minor | Accepted. S10 is 96 N, S11 uses the CAL root moment of 4.10 N.m (5.3 MPa), and NSM-PRC-001 says 96 N |
| 6 | S23 uses friction 0.3, CAL H6 uses 0.2 and omits the V factor | Minor | S22 (was S23) now uses 0.2 as CAL does. CAL H6 leaves out the factor of the V and is therefore conservative; no change |
| 7 | The interval rule at SF10 to SF12 breaks PR-002's 1-minute values, and SF12 leaves 0.03 s of the 30 s a day | Weak verdict | Accepted. PR-002 and PR-012 statuses are amended; project risk R-9 added |
| 8 | S20 and S26 are not science claims | Weak verdict | Accepted. S20 is removed (the physics is S9; the promise is a firmware matter, NSM-DDR-001 D2). S26 is removed and the isolation question sits in NSM-REG-001 G12 as to assess |
| 9 | S15: the area ratio is optimistic in a wet salt film; crevice corrosion is likelier | Weak verdict | Accepted. Fix under the standing instruction: seal screw threads and band contact faces with the neutral-cure silicone already in BOM line 13 (build plan, NSM-DEC-001). S15 stays Within known science, closed by that decision |
| 10 | S18: 111 dB is the loss needed, Hata gives about 120 dB | Minor | Accepted. S18 now uses Okumura-Hata (119.7 dB) against 143 dB available |
| 11 | S6: compare against the usable energy, not 19.2 Wh | Minor | Accepted. S6 now uses 80 % usable (52.9 days) |

The reviewer could not refute S3, S4, S5, S7, S8, S9, S16, S17, S19, S20, S21 and S23 to S24 as they stood (numbers as in this version), nor the headline lower limit (34.9 dBA for the ICS-43434), the 12.2 mW load, the 23.7 s/day airtime at SF9 or the cost arithmetic. After the changes above the check was rerun: 21 rows within known science, 3 plausible and closed by calculation (S2, S12, S13), none failing. The reviewer's findings 1 and 9 were fixes to the design (a part choice and a sealing step) made under the fix rule; findings 3 and 7 concern requirements and go to Amish.

## Sources

- IM72D128 overload point (126 dB SPL at 1 % THD) and SNR: Infineon IM72D128V01 product brief, https://www.infineon.com/content/dam/infineon/row/public/documents/24/45/infineon-mems-im72d128v01-productbrief-en.pdf (read 2026-11-02).
- ICS-43434 product page and datasheet figures (SNR 65 dB, acoustic overload point 120 dB SPL): TDK InvenSense, https://invensense.tdk.com/products/ics-43434/ (cited in NSM-PRB-001, checked there 2026-10-02).
- DNMS README, https://github.com/hbitter/DNMS (cited in NSM-PRB-001, checked there 2026-10-02).
- LoRa time on air: Semtech application note AN1200.13, "LoRa Modem Designer's Guide" (formula applied in `stem_check.py`; publication cited from memory, link not checked in this session).
- EU868 duty cycle of 1 %: ETSI EN 300 220 as cited in NSM-REQ-001 R12 (now NSM-PRS-001 PR-012); the standard number is as in that earlier text and was not re-checked in this session.
- Uncertainty: JCGM 100:2008, Guide to the expression of uncertainty in measurement (GUM), root sum of squares and coverage factor k = 2.
- Drag on a bluff body, F = 1/2 rho v^2 Cd A, and cantilever bending, sigma = M/Z: any mechanics textbook (for example Roark's Formulas for Stress and Strain).
- Galvanic series: ASTM G82, Standard Guide for Development and Use of a Galvanic Series for Predicting Galvanic Corrosion Performance (title as known; not re-checked in this session).
- Noise exposure: NIOSH recommended exposure limit of 85 dBA over 8 hours with a 3 dB exchange rate, summarized at https://www.cdc.gov/niosh/bulletin/2022/noise-50.html (listed by a web search 2026-11-02; figure also in the NIOSH 1998 criteria document).
- Okumura-Hata urban path loss model, as in any radio propagation textbook (applied slightly outside its 150 to 1500 MHz band).
- Reflection of sound at a rigid surface: pressure doubling, +6.02 dB, any acoustics textbook; facade estimates from NSM-CAL-001 C2.
- LiFePO4 charge limits: cell maker datasheets (0 to 45 degrees C as in bom/bom.csv line 3); FieldNode FND-CAL-001 for the cold-charge lockout.
- Luminaire receptacle and Zhaga: Zhaga Book 18, https://zhagastandard.org/books/overview/smart-interface-between-outdoor-luminaires-and-sensing-communication-modules-18.html (checked 2026-11-02; it names ANSI C136.41 as the dimming receptacle standard).
