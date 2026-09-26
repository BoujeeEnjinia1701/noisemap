---
doc_id: NSM-REQ-001
title: NoiseMap requirements
project: NoiseMap
doc_type: Requirements
version: "0.4"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Populate to TRL 2 (numbered, measurable requirements with targets and concept status)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3; R13 redefined to the NoiseMap parts under NSM-DDR-001 D1; R2 metric set adopted (D5); status column from NSM-CAL-001
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# NoiseMap requirements

These requirements are targets for concept review and must be revised with a co-design partner before the design is frozen. The metric set (R2) and the budget scope (R13) follow NSM-DDR-001 D5 and D1; the relaxed mass limit (R10), the wind flag method (R11) and the interval rule (R12) follow NSM-DDR-002. All were decided by Amish, 2026-09-25: go with recommendation. Status is taken from the TRL 3 calculation note NSM-CAL-001 v0.2; "met on paper" means met by calculation only. None is not met; three are at risk (R3, R4, R5), four can be settled only by test (R8, R9, R11, R14), and eight are met on paper or by design.

Design case: one node on a 114.3 mm street pole 0.45 m behind the curb, microphone 4.0 m above the sidewalk and 0.45 m from the pole face, in a mixed street with traffic by day and bars at night.

Table 1. Requirements.

| ID | Requirement | Target | Verification | Status (NSM-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Privacy: no audio samples are stored or leave the microphone head; only levels cross the cable or the radio | No data storage in the head; cable carries levels only; head firmware published with a build hash and read-out protection | Design review, firmware audit, cable capture | Met by design; the guarantee rests on the firmware, since the cable could carry a speech codec (NSM-DDR-001 D2) |
| R2 | Reported metrics | Per 15 min: fifteen 1-minute LAeq, LAeq, LAFmax, LAFmin, L10, L90, LCeq, device status | Design review | Met by design (22 bytes per record) |
| R3 | Accuracy of LAeq,15min against a co-located class 1 meter | Within ±2 dB from 40 to 100 dBA, after field calibration | Side-by-side field test | **At risk**: expanded uncertainty 2.9 dB on assumed terms; facade bias up to 2.4 dB before a site correction |
| R4 | Measuring range | 35 to 110 dBA | Bench test with calibrator and reference source | **At risk**: ICS-43434 34.9 to 113 dBA (no margin); IM72D128 27.9 to 113 dBA |
| R5 | Frequency weighting | A and C weighting as defined in IEC 61672-1, within class 2 tolerances from 63 Hz to 8 kHz (goal) | Bench test against a reference meter | **At risk**: roll-off equalized to ±0.8 dB at 63 Hz; membrane, windscreen and head diffraction unknown |
| R6 | Time stamps | Each record time-stamped within 2 s of UTC | Design review (LoRaWAN network time) | Met by design |
| R7 | Energy | Energy neutral at 1.5 peak sun hours; 14 days without sun | Energy budget, bench test | Met on paper (5.81 Wh/day for 0.29 Wh/day; 53 days) |
| R8 | Ingress and weather | IP65 enclosure; microphone head survives driving rain; -20 °C to +50 °C | Spray test, thermal chamber | Not verifiable at TRL 3 |
| R9 | Calibration check | Field check with a 94 dB, 1 kHz calibrator in 10 min or less; offset stored on the node | Timed trial | Not verifiable at TRL 3 |
| R10 | Installation and mass | Two trained people, 45 min, no drilling or pole wiring; 60 to 140 mm poles; 3.5 kg or less (relaxed from 3 kg, NSM-DDR-002); withstands 35 m/s gusts | Timed trial, weighing, bracket calculation | Met on paper on mass (3.45 kg with pocketed V-blocks and saddle; margin 0.05 kg); wind met on paper; fit met by design; time not verifiable at TRL 3 |
| R11 | Contaminated data | Intervals with wind above about 5 m/s or heavy rain are flagged, wind by a level-based flag (no added sensor) and rain on the server from weather data (NSM-DDR-002) | Field comparison with a weather station | Not verifiable at TRL 3: method chosen; the threshold needs field data (TRL 4, on hold) |
| R12 | Radio use | Within EU868 1 % duty cycle and The Things Network fair use (30 s uplink per day); 15-minute interval at SF7 to SF9, lengthened automatically at SF10 to SF12 (NSM-DDR-002) | Airtime calculation | Met on paper: 23.7 s/day at SF9; 29.6, 29.6 and 30.0 s/day at 24, 48 and 87 min for SF10 to SF12 |
| R13 | Parts cost | NoiseMap parts (lines 7 to 14 of the BOM) $100 or less per node; the FieldNode core is costed in the FieldNode repo and the full node cost is stated | Priced BOM | Met on paper: NoiseMap parts $62.00; full node $188.00 with the $126.00 FieldNode core |
| R14 | Service life | 5 years outdoors, with a yearly windscreen change and one battery change | Design review, UV-stable materials | Not verifiable at TRL 3 |
| R15 | Openness | Hardware, firmware, calibration method and data format published under the repo licenses | Design review | Met by design |

Table 2. Assumptions behind the targets.

| Assumption | Value | Source or basis |
| --- | --- | --- |
| Microphone height | about 4 m above the ground | 4.0 ± 0.2 m assessment height for EU strategic noise maps ([Directive 2002/49/EC, Annex I](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32002L0049)) |
| Quietest night level to resolve | about 35 dBA | Quiet residential street at night (estimate) |
| Loudest level to resolve | about 110 dBA | Close pass of a loud motorcycle or siren (estimate) |
| Peak sun hours, winter design case | 1.5 h | Mid-latitude winter (estimate) |
| Wind speed that spoils readings with a foam windscreen | about 5 m/s | Common practice (estimate, to be checked) |
| Microphone data | ICS-43434: 65 dB SNR, 120 dB SPL overload, 60 Hz to 20 kHz; IM72D128: 72 dB(A) SNR | ICS-43434 product page ([TDK InvenSense](https://invensense.tdk.com/products/ics-43434/)); IM72D128 from the DNMS README ([DNMS](https://github.com/hbitter/DNMS)) |
| Street pole diameter | 60 to 140 mm, design case 114.3 mm | Common lighting and signal poles (estimate) |

> **Safety:** Requirements R8 and R10 involve work at height beside traffic and a lithium cell. See the safety section of NSM-PRC-001.
