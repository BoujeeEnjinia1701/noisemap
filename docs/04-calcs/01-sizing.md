---
doc_id: NSM-CAL-001
title: NoiseMap sizing calculations
project: NoiseMap
doc_type: Calculation note
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (measuring range, frequency response, reflections and accuracy, processing and power, energy, record format, airtime, privacy capacity, wind and rain flagging, mechanics, mass, cost)
---

# NoiseMap sizing calculations

On paper, NoiseMap meets six of its fifteen requirements (two by calculation, four by design), has four at risk, misses one and leaves four that only tests can settle. The miss is mass: with the FieldNode core at its TRL 3 figure of 2.41 kg, a street pole adapter and the arm, the node weighs **3.32 kg against 3 kg (R10)**. Energy is not a concern: the design load is 12.2 mW, 12 % of FieldNode's 100 mW allowance, which gives 53 days without sun and keeps the node in credit even on the hot clear days that stop FieldNode charging. The measuring range reaches 35 dBA with no margin on the ICS-43434 (34.9 dBA) and with 7 dB of margin on the IM72D128 (27.9 dBA), and tops out at 113 dBA. Accuracy (R3) is at risk: an assumed uncertainty budget gives ±2.9 dB, and a facade behind the pole can add up to 2.4 dB before a site correction. Under D1 the $100 budget covers the NoiseMap parts, now $62.00; the full node with the FieldNode core is $188.00.

Every number in this note is printed by `docs/04-calcs/sizing.py` (run from the repo root: `python docs/04-calcs/sizing.py`), which also writes `docs/04-calcs/results.csv`. The tag in brackets, for example [A1], is the line of the script's output that carries the number. The script imports `PARAMS`, `derived()` and the part volumes from `cad/src/model.py`, reads `bom/bom.csv` and `budget_usd` in `project.yaml`, and takes FieldNode figures from FND-CAL-001 v0.1.

> **Safety:** These are first-principles estimates for a paper proof of concept. They do not show that the pole mounting, the lithium iron phosphate cell or the installation is safe. Clamp preload, arm fixing and the cell's charge lockout must be checked on hardware before any node is installed. See NSM-PRC-001, Safety.

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| ICS-43434 | 65 dB SNR, sensitivity -26 dBFS at 94 dB SPL, 120 dB SPL overload, response 60 Hz to 20 kHz, listed end of life; supply 0.49 mA | TDK product page ([TDK InvenSense](https://invensense.tdk.com/products/ics-43434/)); current is a typical class value, not checked |
| IM72D128 | 72 dB(A) SNR, PDM output, IP57 at part level; overload and roll-off taken equal to the ICS-43434; supply 1.0 mA | DNMS README ([DNMS](https://github.com/hbitter/DNMS)); overload, roll-off and current not checked |
| Range criteria | Lower limit where self-noise adds 1 dB; 10 dB crest factor above the rms level for traffic, horns and sirens | Screening values |
| Response limits | ±2.5 dB at 63 Hz and ±5 dB at 8 kHz, taken as the class 2 limits; low-frequency corner spread ±20 % | Approximate; the IEC 61672-1 table was not re-checked in this session |
| Processing | 48 kHz; seven biquads (A 3, C 2, low-frequency equalizer 1, wind band 1) at 14 cycles each; four channels at 6 cycles; 10 cycles overhead; 48 MHz clock; 120 µA/MHz running, 1.6 mA asleep with DMA running | STM32L4 class typical figures; to confirm on the chosen board |
| FieldNode core | 4.0 mWh/day core; 15.36 Wh usable; 70 % at -20 °C, 80 % at end of life; rail 90 %; controller 8 mA awake, woken for each 12-byte frame at 9,600 baud plus 5 ms | FND-CAL-001 v0.1; the wake overhead is assumed |
| Energy chain | 6 W panel, 1.5 peak sun hours (NoiseMap design case), 0.80 derating, charger 0.85, cell 0.95 | NSM-REQ-001 Table 2; FND-CAL-001 |
| Radio | 22-byte record plus 13 bytes of LoRaWAN overhead; 125 kHz, CR 4/5, 8-symbol preamble, explicit header, CRC; 96 uplinks a day | LoRaWAN defaults |
| Speech codec | Codec 2 runs at 700 to 3,200 bit/s | [Rowetel, Codec 2](https://www.rowetel.com/?page_id=452) |
| Reflections | Incoherent addition; facade energy reflection 0.9; lanes 5 and 10 m from the microphone | Screening values |
| Wind | 35 m/s gust, 1.225 kg/m³; Cd 1.2 on tubes, 0.5 on the foam sphere; 6063-T5 class E = 69 GPa, yield 145 MPa; band preload 1,000 N and friction 0.2; turbulence intensity 0.2 at 4 m | Handbook ranges; preload as FND-CAL-001 |
| Mass | Aluminium 2.70, ASA 1.07, foam 0.030 g/cm³ from model volumes (bands counted as aluminium); boards 15 g, spike 6 g, cable 90 g, hardware and lanyard 50 g; FieldNode core 2.41 kg with its small-pole V-blocks and bands left in | Estimates |

## A. Measuring range (R4)

- **Self-noise and lower limit.** The ICS-43434 has 29.0 dBA of self-noise, so a 35 dBA street reads 0.97 dB high; the 1 dB lower limit is **34.9 dBA**, with no margin on the 35 dBA target. The IM72D128 has 22.0 dBA of self-noise and a lower limit of **27.9 dBA** [A1].
- **Noise-floor subtraction** helps only as far as the self-noise is known: with the ICS-43434 at 35 dBA, an error of ±1 dB in the stored self-noise leaves the result between 34.71 and 35.22 dBA [A2]. The adapter board of D3 lets a quiet-street node use the IM72D128.
- **Upper limit.** The ICS-43434 reaches full scale at 120 dB SPL rms for a sine, 123 dB peak [A3]. With a 10 dB crest factor the highest rms level measured cleanly is **113 dB**, against the 110 dBA target. The TRL 2 figure of 115 dBA ignored crest factor. The IM72D128 overload point was not checked and is taken as the same.
- **R4 is at risk** with the ICS-43434 and met on paper with the IM72D128.

## B. Frequency response (R5)

- **Low frequencies.** Treating the 60 Hz lower limit as a first-order corner, the microphone is down 0.9 dB at 125 Hz, 2.8 dB at 63 Hz and 6.7 dB at 31.5 Hz [B1]. A fixed digital equalizer in the head restores this; if the corner varies by ±20 % between parts, the residual is ±0.8 dB at 63 Hz and about ±1.4 dB at 31.5 Hz [B2], inside the ±2.5 dB taken as the class 2 limit at 63 Hz. The equalizer adds 6.7 dB of gain at 31.5 Hz, where A weighting is -39.4 dB, so LAeq self-noise barely changes; LCeq self-noise rises at low frequencies [B2b].
- **Acoustic port.** The 3 mm port through the 2 mm top plate and a 3 x 0.5 mm front cavity (the gasket gap between plate and microphone board) resonate at **36.2 kHz**, adding 0.44 dB at 8 kHz undamped [B3]. A tenfold larger cavity would resonate at 10.4 kHz and add 7.9 dB at 8 kHz [B3b], so the cavity must stay small. These dimensions are parameters in `cad/src/model.py`.
- **R5 is at risk.** The hydrophobic membrane, the windscreen and diffraction round the 40 mm head all shape the response above about 2 kHz, and none can be calculated with confidence on paper.

## C. Reflections and accuracy (R3)

- **Pole.** A 114.3 mm pole 0.45 m behind the microphone reflects 6.0 % of the direct energy back to it, adding 0.25 dB [C1]. The FieldNode core sits in the pole's shadow on the far side.
- **Facades.** A facade behind the pole adds more (Table 2) [C2]. At 1 to 2 m the bias is 1.1 to 2.4 dB, which approaches the whole ±2 dB of R3.

*Table 2. Level added by a facade behind the microphone (energy reflection 0.9).*

| Facade distance | Lane 5 m, point source | Lane 5 m, traffic line | Lane 10 m, point source | Lane 10 m, traffic line |
| --- | --- | --- | --- | --- |
| 1 m | +1.6 dB | +2.2 dB | +2.1 dB | +2.4 dB |
| 2 m | +1.1 dB | +1.8 dB | +1.6 dB | +2.2 dB |
| 5 m | +0.4 dB | +1.1 dB | +0.9 dB | +1.6 dB |
| 10 m | +0.2 dB | +0.7 dB | +0.4 dB | +1.1 dB |

- **Uncertainty budget.** With assumed standard uncertainties of 0.4 dB for the calibrator, 0.5 dB for drift between checks, 0.5 dB for the windscreen, 0.7 dB for the response residual and 1.0 dB for reflections after a site correction, the combined value is 1.47 dB and the expanded value (k = 2) **2.9 dB** against ±2 dB [C3], [C3b]. **R3 is at risk.** The side-by-side comparison of D7 is what sets the site correction; only it can show whether R3 is met.

## D. Processing and power (R7)

- **Processor load.** Seven biquads and four channels take 132 cycles per sample: 6.34 million cycles a second, 13.2 % of a 48 MHz core. At 32 kHz this falls to 4.22 million [D1]. The TRL 2 question on sample rate therefore does not affect power much; 48 kHz stays.
- **Current.** Running 13.2 % of the time at 5.76 mA and sleeping with DMA at 1.6 mA, the processor averages **2.15 mA** [D2]. The TRL 2 assumption was 5 mA.
- **Node load.** With the ICS-43434 the head takes 9.7 mW from the cell and the node 10.3 mW; with the IM72D128 the head takes 11.5 mW and the node **12.2 mW** (0.292 Wh a day), the design value. Waking the FieldNode controller for each one-second frame costs 0.46 mW, more than the 0.17 mW of the rest of the core [D3]. With the TRL 2 processor current and a 1 mA microphone the upper bound is 22.6 mW (0.543 Wh a day) [D4]. The design load is 12 % of FieldNode's 100 mW design allowance [D5].

## E. Energy (R7)

- **Harvest.** At 1.5 peak sun hours the cell stores 5.81 Wh a day, 20 times the design load and 11 times the upper bound; FieldNode's worst month (2 h) gives 7.75 Wh [E1].
- **Autonomy.** At the design load one cell lasts **53 days** without sun, 37 days at -20 °C and 42 days at end of life; the upper bound, cold and aged, still gives 16 days [E2], against 14.
- **Hot weather.** FieldNode's hot clear day without a shield stores 0.8 Wh (clean) or 0.3 Wh (dusty) because the cell is above its 45 °C charge limit most of the day. NoiseMap draws 0.29 Wh at the design load, so it stays in credit, marginally when dusty; at the upper bound (0.54 Wh) a dusty node would lose charge [E3]. The FieldNode sun shield decision (FieldNode review item 4) matters little to NoiseMap.
- **R7 is met on paper.**

## F. Record, radio and privacy (R1, R2, R6, R12)

- **Record.** Fifteen 1-minute LAeq bytes, LAeq,15min, LAFmax, LAFmin, L10, L90, LCeq and a status byte make **22 bytes**; one byte at 0.5 dB steps spans 20.0 to 147.5 dB [F1]. The status byte carries the wind flag and the count of flagged minutes. R2 is met by design.
- **Airtime (Table 3).** At SF9 each uplink takes 246.8 ms, 23.7 s a day. At SF10 the 35-byte frame takes 493.6 ms and 47.4 s a day, over The Things Network's 30 s [F2]. A stored record sent later carries a 4-byte time stamp (267.3 ms at SF9) [F2b]. **R12 is at risk**: met at SF7 to SF9, not at SF10 or slower unless the interval grows (item O4 in NSM-DDR-001). The EU868 1 % duty cycle is met at every spreading factor.

*Table 3. Time on air for a 22-byte record (35 bytes on air) at 125 kHz [F2].*

| Spreading factor | Per uplink | Per day at 15 min | Shortest interval within 30 s/day | EU868 1 % off-time |
| --- | --- | --- | --- | --- |
| SF7 | 77.1 ms | 7.4 s | 4 min | 8 s |
| SF8 | 143.9 ms | 13.8 s | 7 min | 14 s |
| SF9 | 246.8 ms | 23.7 s | 12 min | 24 s |
| SF10 | 493.6 ms | 47.4 s | 24 min | 49 s |
| SF11 | 987.1 ms | 94.8 s | 48 min | 98 s |
| SF12 | 1,810.4 ms | 173.8 s | 87 min | 179 s |

- **Time stamps.** The core stamps each record from LoRaWAN network time (DeviceTimeReq), which is well within 2 s; R6 is met by design.
- **What the links could carry (R1).** Raw audio is 1.152 Mbit/s. The UART carries 7,680 bit/s of payload, 150 times too slow for raw audio, and the level frames use 1.25 % of it. A speech codec such as Codec 2 needs 700 to 3,200 bit/s, which the cable could carry [F3]. The radio could carry 21.4 kbit a day at SF9 under fair use, about 31 s of 700 bit/s speech, or 1.97 Mbit a day at SF7 under the 1 % duty cycle alone, about 47 min [F4]. The physical links do not rule out leaking speech, so, as D2 states, privacy rests on the open head firmware, read-out protection and a published build hash. R1 is met by design on that basis.

## G. Wind and rain flagging (R11)

- **Wind.** Turbulence at 4 m makes pressure fluctuations of about 1 Pa rms at 2 m/s, 6 Pa at 5 m/s and 25 Pa at 10 m/s at an unscreened microphone (94, 110 and 122 dB), mostly below 20 Hz [G1]. The foam windscreen removes much of this, but what reaches the microphone scales roughly with the fourth power of wind speed: from 2 to 5 m/s it rises by 15.9 dB, and 1 m/s near 5 m/s is 3.2 dB [G2]. A Z-weighted band below 40 Hz, computed in the head, and its one-second spread therefore separate windy minutes sharply from traffic once a threshold is set. The threshold cannot be computed; it needs a field comparison with an anemometer.
- **Wind sensor option.** A cup anemometer with a pulse output on FieldNode's second port would cost about $25 and weigh about 0.15 kg (indicative, unchecked), bringing the NoiseMap parts to $87.00 and the node to 3.47 kg [I3].
- **Rain.** Rain on the foam gives broadband impulses that level statistics do not reliably separate from street noise. The proposed method is a server-side flag from the nearest public weather station or radar rainfall, which needs no hardware.
- **R11 is not verifiable at TRL 3.** The method is defined; the threshold needs field data. The choice between the level-based flag and a sensor is item O3 in NSM-DDR-001.

## H. Mechanics (R10)

- **Mass.** To FieldNode's 2.41 kg the arm, saddle and band add 0.374 kg, the head housing 0.066 kg, the boards 0.015 kg, the windscreen and spike 0.016 kg, the cable 0.090 kg, the street pole adapter 0.294 kg and hardware 0.050 kg [H1]: **3.32 kg against 3.0 kg, so R10 is not met** [H2]. The TRL 2 figure of 2.3 kg used FieldNode's TRL 2 mass of 1.7 kg. Pocketing the V-blocks and saddle to half their solid mass gives 3.10 kg [H2b], still over; the FieldNode small-pole V-blocks and bands, left in the core mass, would save a little more. The options are item O2 in NSM-DDR-001.
- **Wind on the arm.** At 35 m/s (750 Pa) the arm takes 9.5 N, the head tube 3.8 N and the windscreen 2.4 N [H3]. The arm root sees 4.61 N·m from wind and 0.74 N·m from weight, 4.67 N·m combined; the 25 x 2 mm tube (770 mm³ section modulus) is stressed to 6.1 MPa, a factor of 24 on yield [H4]. The tip moves 0.37 mm in the gust.
- **Vibration.** The arm and head have a first mode near 70 Hz. Vortex shedding matches it at about 8.8 m/s across the arm and 14.0 m/s across the head [H5]. Stresses are low, but vibration at those speeds would add structure-borne noise at the microphone, and those intervals are windy enough to be flagged anyway.
- **Clamp.** Wind twists the arm clamp about the pole with 5.50 N·m against 22.9 N·m of friction (factor 4.2), and the arm and head pull it down with 4.6 N against 400 N [H6]. Both depend on the assumed 1,000 N preload.
- **Pole load.** The node adds about 97 N at 3.5 to 4 m in a 35 m/s gust (81 N from FieldNode) [H7], which the pole owner should check.
- **Fit.** On a 60 mm pole the V contacts sit 21.2 mm along each 70.7 mm V face and on a 140 mm pole 49.5 mm; the 100 mm V seats poles up to 141 mm. Bands need about 261 to 450 mm [H8], [H8b]. The fit to 60 to 140 mm poles is met by design; the 45 min installation time can only be timed.

## I. Cost (R13)

The BOM has 14 lines, all priced. Lines 1 to 6, the FieldNode core, total $126.00, the figure in the FieldNode BOM; lines 7 to 14, the NoiseMap parts, total **$62.00**, 62 % of the $100 `budget_usd`, a margin of $38.00. The full node is $188.00, $88.00 more than $100 [I1], [I2]. Under D1 the budget covers the NoiseMap parts, so **R13 is met on paper**. The TRL 2 figure of $171 used $119 for the core and had no street pole adapter.

## L. Results against every requirement

*Table 4. Requirement status (not met first) [L].*

| ID | Requirement | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R10 | Installation and mass | 3.32 kg (3.10 kg pocketed); arm factor 24 on yield; clamp twist factor 4.2; fits 60 to 140 mm poles | 3 kg or less; 35 m/s gusts; two people, 45 min | **Not met** on mass; wind met on paper; time not verifiable at TRL 3 |
| R3 | Accuracy | Expanded uncertainty 2.9 dB (assumed terms); facade bias up to +2.4 dB before site correction | ±2 dB, 40 to 100 dBA | **At risk** |
| R4 | Measuring range | ICS-43434 34.9 to 113 dBA; IM72D128 27.9 to 113 dBA | 35 to 110 dBA | **At risk** (no margin with ICS-43434) |
| R5 | Frequency weighting | -2.8 dB at 63 Hz before equalizing, ±0.8 dB after; port resonance 36 kHz | Class 2 limits, 63 Hz to 8 kHz | **At risk** (membrane, windscreen, head) |
| R12 | Radio use | 23.7 s/day at SF9; 47.4 s/day at SF10 | 1 % duty cycle; 30 s/day | **At risk** (not met at SF10 to SF12 at 15 min) |
| R8 | Ingress and weather | FieldNode IP65; head skirt, membrane, bored windscreen | IP65; driving rain; -20 to +50 °C | Not verifiable at TRL 3 |
| R9 | Calibration check | Calibrator fits the head with the windscreen off; offset stored in the head | 10 min or less | Not verifiable at TRL 3 |
| R11 | Contaminated data | Level-based wind flag; server rain flag | Flag wind above 5 m/s and heavy rain | Not verifiable at TRL 3 (method defined) |
| R14 | Service life | ASA, yearly windscreen, FieldNode cell swap | 5 years | Not verifiable at TRL 3 |
| R7 | Energy | 5.81 Wh/day stored against 0.29 Wh/day; 53 days without sun (16 cold, aged, upper bound) | Neutral at 1.5 h; 14 days | Met on paper |
| R13 | Parts cost | NoiseMap parts $62.00; full node $188.00 | NoiseMap parts $100 or less | Met on paper |
| R1 | Privacy | No storage or radio in the head; firmware sends levels only | Levels only; published build hash | Met by design (rests on firmware) |
| R2 | Reported metrics | 22 bytes per 15 min | Metric set per D5 | Met by design |
| R6 | Time stamps | LoRaWAN network time | Within 2 s of UTC | Met by design |
| R15 | Openness | Repo licenses; method and format here | All published | Met by design |

Counts [L2]: 1 not met, 4 at risk, 4 not verifiable at TRL 3, 2 met on paper, 4 met by design.

## Checks against the TRL 2 figures

| TRL 2 claim (NSM-PRC-001 v0.2) | This note | Action |
| --- | --- | --- |
| Range about 35 to 115 dBA | 34.9 (27.9 with IM72D128) to 113 dBA | Precis and README updated |
| Processor about 5 mA; head 18 mW; node 21 mW, 0.51 Wh/day | 2.15 mA; head 9.7 to 11.5 mW; node 12.2 mW, 0.29 Wh/day (22.6 mW upper bound) | Precis, README and flow updated |
| Autonomy about 30 days | 53 days (37 at -20 °C) | Updated |
| Winter harvest about 5.8 Wh/day | 5.81 Wh/day | Stands |
| Airtime about 24 s/day at SF9; 47 s at SF10 | 23.7 s and 47.4 s | Stands |
| Mass about 2.3 kg; R10 met | 3.32 kg; R10 not met | Updated; option O2 |
| Wind load on the panel about 50 N | 52.2 N (FND-CAL-001); 16 N more on the arm and head | Updated |
| Cost about $171 (core $119, NoiseMap $52) | $188.00 (core $126.00, NoiseMap $62.00 with the adapter) | BOM, precis and README updated |
| Microphone 0.45 m from the pole; arm about 400 mm | 0.45 m; arm 422 mm from saddle to head | Stands |
| Cable "far too slow" for audio | Too slow for raw audio, fast enough for a speech codec | Precis wording follows D2 |
