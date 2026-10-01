---
doc_id: NSM-CAL-001
title: NoiseMap sizing calculations
project: NoiseMap
doc_type: Calculation note
version: "0.3"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (measuring range, frequency response, reflections and accuracy, processing and power, energy, record format, airtime, privacy capacity, wind and rain flagging, mechanics, mass, cost)
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002); pocketed V-blocks and saddle, corrected V-block geometry, R10 at 3.5 kg, interval rule for R12, level-based wind flag
- version: "0.3"
  date: '2026-10-01'
  author: Amish Chadha
  change: Mechanics, mass and cost re-run for the constructable design (NSM-DDR-003); FieldNode core at FND-CAL-001 v0.3; budget treated as a value-engineering target
---

# NoiseMap sizing calculations

On paper, NoiseMap meets eight of its fifteen requirements (four by calculation, four by design), has three at risk, misses none and leaves four that only tests can settle. Under NSM-DDR-002 R10 is relaxed to 3.5 kg. With the design made constructable (NSM-DDR-003: sawn and drilled V-blocks, a bent sheet arm saddle with two bands, fixings throughout, and the FieldNode core without its small-pole V-blocks and bands), the node weighs **3.45 kg against 3.5 kg (R10)**, a margin of only 0.05 kg. An automatic interval rule at slow data rates brings R12 within fair use at every spreading factor. Energy is not a concern: the design load is 12.2 mW, 12 % of FieldNode's 100 mW allowance, which gives 53 days without sun and keeps the node in credit even on the hot clear days that stop FieldNode charging. The measuring range reaches 35 dBA with no margin on the ICS-43434 (34.9 dBA) and with 7 dB of margin on the IM72D128 (27.9 dBA), and tops out at 113 dBA. Accuracy (R3) is at risk: an assumed uncertainty budget gives ±2.9 dB, and a facade behind the pole can add up to 2.4 dB before a site correction. Under NSM-DDR-001 D1 the $100 `budget_usd` applies to the NoiseMap parts; it is a value-engineering target, not a limit. The constructable NoiseMap parts are estimated at $72.00, $28.00 under the target; the full node with the FieldNode core is $211.00.

Every number in this note is printed by `docs/04-calcs/sizing.py` (run from the repo root: `python docs/04-calcs/sizing.py`), which also writes `docs/04-calcs/results.csv`. The tag in brackets, for example [A1], is the line of the script's output that carries the number. The script imports `PARAMS`, `derived()` and the part volumes from `cad/src/model.py`, reads `bom/bom.csv` and `budget_usd` in `project.yaml`, and takes FieldNode energy figures from FND-CAL-001 v0.1 and its mass from FND-CAL-001 v0.3.

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
| Mass | Aluminium 2.70, stainless steel 7.90, ASA 1.07, nylon 1.15, foam 0.030 g/cm³ from model volumes (printed parts counted solid); boards 15 g, cable 90 g, ties, tape and small parts 30 g; FieldNode base node 2.45 kg (FND-CAL-001 v0.3) less its small-pole V-blocks and 80 g of bands, which a street pole node leaves off (NSM-DDR-003) | Estimates |

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
- **Airtime (Table 3).** At SF9 each uplink takes 246.8 ms, 23.7 s a day. At SF10 the 35-byte frame takes 493.6 ms and 47.4 s a day, over The Things Network's 30 s [F2]. A stored record sent later carries a 4-byte time stamp (267.3 ms at SF9) [F2b]. The EU868 1 % duty cycle is met at every spreading factor.
- **Interval rule (NSM-DDR-002, item O4).** The core keeps 15 minutes at SF7 to SF9 and lengthens the interval automatically at slower data rates to the shortest that fits 30 s a day: 24 min at SF10 (29.6 s a day, 60 records), 48 min at SF11 (29.6 s, 30 records) and 87 min at SF12 (30.0 s, 16 records). The record stays 22 bytes; its fifteen sub-interval LAeq values then each span 1.6, 3.2 or 5.8 minutes [F2c]. **R12 is met on paper** with this rule, which follows FieldNode's own interval item.

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
- **Rain.** Rain on the foam gives broadband impulses that level statistics do not reliably separate from street noise. The method is a server-side flag from the nearest public weather station or radar rainfall, which needs no hardware.
- **Wind sensor option, not adopted.** A cup anemometer with a pulse output on FieldNode's second port would cost about $25 and weigh about 0.15 kg (indicative, unchecked), bringing the NoiseMap parts to $97.00 and the node to 3.60 kg, over R10 [I3]. Under NSM-DDR-002 (item O3) the level-based flag is the method, so no anemometer is fitted.
- **R11 is not verifiable at TRL 3.** The method is chosen; the threshold needs a field comparison with an anemometer, which is TRL 4 work and on hold.

## H. Mechanics (R10)

- **Mass.** The FieldNode base node is 2.45 kg; a street pole node leaves off its V-blocks (0.144 kg) and bands (0.08 kg), which gives 2.23 kg. To that the arm saddle, tube, flange and fixings add 0.391 kg, the arm bands and lanyard 0.129 kg, the head housing, cap and bolts 0.108 kg, the boards 0.015 kg, the windscreen and spike 0.023 kg, the cable and gland 0.099 kg, the street pole V-blocks and screws 0.314 kg, their bands 0.114 kg, and ties and small parts 0.030 kg [H1]: **3.45 kg against the relaxed 3.5 kg, so R10 is met on paper**, with 0.05 kg of margin [H2]. Sawing the V-blocks from 16 mm bar rather than 20 mm and drilling four 14 mm holes in each saves 0.144 kg [H2b].
- **History.** Version 0.2 also gave 3.45 kg, with machined, pocketed 110 x 60 x 40 mm V-blocks, a pocketed saddle, one arm band and the 2.41 kg FieldNode core with its small-pole parts left in. The constructable design (NSM-DDR-003) adds a second arm band, a tube flange, a head cap, a gland and fixings, and leaves the FieldNode small-pole parts off; the two roughly balance.
- **Wind on the arm.** At 35 m/s (750 Pa) the 383 mm arm takes 8.6 N, the head tube 3.8 N and the windscreen 2.4 N [H3]. The arm root sees 4.01 N·m from wind and 0.83 N·m from weight, 4.10 N·m combined; the 25 x 2 mm tube (770 mm³ section modulus) is stressed to 5.3 MPa, a factor of 27 on yield [H4]. The tip moves 0.26 mm in the gust.
- **Vibration.** The arm and head have a first mode near 70 Hz. Vortex shedding matches it at about 8.8 m/s across the arm and 14.1 m/s across the head [H5]. Stresses are low, but vibration at those speeds would add structure-borne noise at the microphone, and those intervals are windy enough to be flagged anyway.
- **Clamp.** The arm saddle now has two bands. Wind twists it about the pole with 4.86 N·m against 45.7 N·m of friction (factor 9.4), and the arm and head pull it down with 6.5 N against 800 N [H6]. Both depend on the assumed 1,000 N preload per band.
- **Pole load.** The node adds about 96 N at 3.5 to 4 m in a 35 m/s gust (81 N from FieldNode) [H7], which the pole owner should check.
- **Fit.** On a 60 mm pole the V contacts sit 21.2 mm either side of the centre line and on a 140 mm pole 49.5 mm, inside both the V-blocks' 106 mm mouth and the saddle's 109 mm mouth; poles up to 141 mm keep their contacts 3 mm inside both [H8], [H8b]. The street pole bands need about 369 to 558 mm. The fit to 60 to 140 mm poles is met by design; the 45 min installation time can only be timed.

## I. Cost (R13)

The BOM has 14 lines, all priced. Lines 1 to 6, the FieldNode core, total $139.00, the base node figure in the FieldNode BOM after its own design for construction (FND-DDR-003); lines 7 to 14, the NoiseMap parts, total **$72.00** [I1]. Value-engineering target: USD 100 (`budget_usd`, a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 72.00 for the NoiseMap parts (USD 28.00 under the target); the full node is USD 211.00 [I2]. **R13 is met on paper.** The constructable design added $10.00 to the NoiseMap parts (two-band saddle and tube flange $6.00, cable gland $1.00, fixings and lanyard $2.00, head cap $1.00) and the FieldNode core rose from $126.00 to $139.00 under FND-DDR-003.

## L. Results against every requirement

*Table 4. Requirement status (weakest first) [L].*

| ID | Requirement | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R3 | Accuracy | Expanded uncertainty 2.9 dB (assumed terms); facade bias up to +2.4 dB before site correction | ±2 dB, 40 to 100 dBA | **At risk** |
| R4 | Measuring range | ICS-43434 34.9 to 113 dBA; IM72D128 27.9 to 113 dBA | 35 to 110 dBA | **At risk** (no margin with ICS-43434) |
| R5 | Frequency weighting | -2.8 dB at 63 Hz before equalizing, ±0.8 dB after; port resonance 36 kHz | Class 2 limits, 63 Hz to 8 kHz | **At risk** (membrane, windscreen, head) |
| R8 | Ingress and weather | FieldNode IP65; head skirt, membrane, bored windscreen | IP65; driving rain; -20 to +50 °C | Not verifiable at TRL 3 |
| R9 | Calibration check | Calibrator fits the head with the windscreen off; offset stored in the head | 10 min or less | Not verifiable at TRL 3 |
| R11 | Contaminated data | Level-based wind flag; server rain flag | Flag wind above 5 m/s and heavy rain | Not verifiable at TRL 3 (method chosen; threshold on hold with TRL 4) |
| R14 | Service life | ASA, yearly windscreen, FieldNode cell swap | 5 years | Not verifiable at TRL 3 |
| R10 | Installation and mass | 3.45 kg constructable design; arm factor 27 on yield; clamp twist factor 9.4; fits 60 to 140 mm poles | 3.5 kg or less; 35 m/s gusts; two people, 45 min | Met on paper on mass (margin 0.05 kg); wind met on paper; time not verifiable at TRL 3 |
| R12 | Radio use | 15 min at SF7 to SF9 (23.7 s/day at SF9); 24, 48 and 87 min at SF10 to SF12 (at most 30.0 s/day) | 1 % duty cycle; 30 s/day | Met on paper (interval rule) |
| R7 | Energy | 5.81 Wh/day stored against 0.29 Wh/day; 53 days without sun (16 cold, aged, upper bound) | Neutral at 1.5 h; 14 days | Met on paper |
| R13 | Parts cost | NoiseMap parts $72.00; full node $211.00 | NoiseMap parts at or under the $100 value-engineering target | Met on paper (USD 28.00 under the target) |
| R1 | Privacy | No storage or radio in the head; firmware sends levels only | Levels only; published build hash | Met by design (rests on firmware) |
| R2 | Reported metrics | 22 bytes per 15 min | Metric set per D5 | Met by design |
| R6 | Time stamps | LoRaWAN network time | Within 2 s of UTC | Met by design |
| R15 | Openness | Repo licenses; method and format here | All published | Met by design |

Counts [L2]: 0 not met, 3 at risk, 4 not verifiable at TRL 3, 4 met on paper, 4 met by design.

## Checks against the TRL 2 figures

| TRL 2 claim (NSM-PRC-001 v0.2) | This note | Action |
| --- | --- | --- |
| Range about 35 to 115 dBA | 34.9 (27.9 with IM72D128) to 113 dBA | Precis and README updated |
| Processor about 5 mA; head 18 mW; node 21 mW, 0.51 Wh/day | 2.15 mA; head 9.7 to 11.5 mW; node 12.2 mW, 0.29 Wh/day (22.6 mW upper bound) | Precis, README and flow updated |
| Autonomy about 30 days | 53 days (37 at -20 °C) | Updated |
| Winter harvest about 5.8 Wh/day | 5.81 Wh/day | Stands |
| Airtime about 24 s/day at SF9; 47 s at SF10 | 23.7 s and 47.4 s | Stands |
| Mass about 2.3 kg; R10 met | 3.45 kg for the constructable design against the relaxed 3.5 kg (v0.2: 3.45 kg pocketed; v0.1: 3.32 kg, with the V-blocks wrongly modeled as flat plates) | Updated per NSM-DDR-002 and NSM-DDR-003 |
| Wind load on the panel about 50 N | 52.2 N (FND-CAL-001); 16 N more on the arm and head | Updated |
| Cost about $171 (core $119, NoiseMap $52) | $211.00 (core $139.00, NoiseMap $72.00 with the adapter and construction parts) | BOM, precis and README updated |
| Microphone 0.45 m from the pole; arm about 400 mm | 0.45 m; arm tube 383 mm between the flange socket and the head socket | Stands |
| Cable "far too slow" for audio | Too slow for raw audio, fast enough for a speech codec | Precis wording follows D2 |
