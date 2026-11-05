---
doc_id: NSM-PRS-001
title: NoiseMap product requirements and specifications
project: NoiseMap
doc_type: Product requirements and specifications
version: "0.6"
status: Draft
date: '2026-11-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold (as NSM-REQ-001)
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
- version: "0.5"
  date: '2026-10-01'
  author: Amish Chadha
  change: Status figures from NSM-CAL-001 v0.3 (constructable design, NSM-DDR-003); R13 stated against the value-engineering target
- version: "0.6"
  date: '2026-11-02'
  author: Amish Chadha
  change: Kit 1.8 migration from NSM-REQ-001 to PRS; each R becomes a PR with the same target, verification and status, traced to a UR (NSM-URS-001); tolerance and units added; PR-016 and PR-017 added
---

# NoiseMap product requirements and specifications

What the design must do, each requirement traced to a user need in NSM-URS-001. This document replaces NSM-REQ-001: each R number is now a PR number (old number in the "Was" column), with the same target, verification and status. Targets are proposals for review with a co-design partner and must be revised with one before the design is frozen. The metric set (PR-002) and the budget scope (PR-013) follow NSM-DDR-001 D5 and D1; the relaxed mass limit (PR-010), the wind flag method (PR-011) and the interval rule (PR-012) follow NSM-DDR-002; all were decided by Amish, 2026-09-25: go with recommendation. Status comes from the TRL 3 calculation note NSM-CAL-001 v0.3; "met on paper" means met by calculation only. PR-016 and PR-017 are new in this migration and describe parts of the design that were already in the build plan. Seventeen requirements: one not met on paper (PR-003), two at risk (PR-004, PR-005), six to verify at TRL 4 (PR-008, PR-009, PR-011, PR-014, PR-016 and the install time of PR-010), the rest met on paper or by design.

Design case: one node on a 114.3 mm street pole 0.45 m behind the curb, microphone 4.0 m above the sidewalk and 0.45 m from the pole face, in a mixed street with traffic by day and bars at night. This is concept option A of NSM-OPT-001; options B and C are scored against the same user requirements and are not designed to these targets.

Table 1. Product requirements and specifications.

| ID | Traces to | Category | Title | Requirement | Target | Tolerance | Units | Verification | Status | Was |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PR-001 | UR-001 | Software | Levels only | No audio samples are stored or leave the microphone head; only levels cross the cable or the radio. | No data storage in the head; cable carries levels only; firmware published with a build hash and read-out protection | none | n/a | Design review, firmware audit, cable capture (TRL 3 design review; audit and capture at TRL 4) | Met by design; the guarantee rests on the firmware, since the cable could carry a speech codec (NSM-DDR-001 D2) | R1 |
| PR-002 | UR-002 | Software | Reported metrics | Each 15 minute record (at SF7 to SF9; at SF10 to SF12 the interval and the fifteen sub-interval values lengthen, 1.6 to 5.8 minutes each, NSM-DDR-002) shall carry fifteen 1-minute LAeq, LAeq, LAFmax, LAFmin, L10, L90, LCeq and a device status. | 22 bytes per record | exact | bytes | Design review (TRL 3) | Met by design at SF7 to SF9; sub-intervals longer at SF10 to SF12 | R2 |
| PR-003 | UR-003 | Performance | Accuracy | LAeq,15min shall agree with a co-located class 1 meter after field calibration. | 2 | max, 40 to 100 dBA | dB | Analysis (NSM-CAL-001 C3, TRL 3); side-by-side field test (TRL 4) | Not met on paper: expanded uncertainty 2.9 dB (3.1 dB with the reference meter) on assumed terms against 2 dB; facade bias up to 2.4 dB (2.7 dB in a canyon) before a site correction; relaxing the target is Amish's decision | R3 |
| PR-004 | UR-004 | Performance | Measuring range | The node shall measure from 35 to 110 dBA (A-weighted). | 35 to 110 | min and max | dBA | Analysis (NSM-CAL-001 A1, TRL 3); bench test (TRL 4) | At risk: ICS-43434 34.9 dBA to 113 dB SPL, which is 103 to 108 dBA for traffic; IM72D128 (fitted by default) 27.9 dBA to 119 dB SPL, 109 to 114 dBA | R4 |
| PR-005 | UR-005 | Performance | Frequency weighting | A and C weighting shall follow IEC 61672-1 within class 2 tolerances from 63 Hz to 8 kHz (goal). | Class 2, 63 Hz to 8 kHz | class 2 limits | Hz | Analysis (NSM-CAL-001 B, TRL 3); bench test (TRL 4) | At risk: roll-off equalized to 0.8 dB at 63 Hz; membrane, windscreen and head diffraction unknown | R5 |
| PR-006 | UR-006 | Software | Time stamps | Each record shall be time-stamped within 2 s of UTC. | 2 | max | s | Design review (LoRaWAN network time, TRL 3) | Met by design | R6 |
| PR-007 | UR-007 | Electrical | Energy | The node shall be energy neutral at 1.5 peak sun hours and run 14 days without sun. | 1.5 h; 14 days | min | h; days | Analysis (NSM-CAL-001 D and E, TRL 3); bench test (TRL 4) | Met on paper (5.81 Wh/day for 0.29 Wh/day; 53 days) | R7 |
| PR-008 | UR-010 | Materials | Ingress and weather | The enclosure shall be IP65 and the microphone head shall survive driving rain from -20 to +50 degrees C. | IP65; -20 to +50 | range | IP code; degrees C | Spray test and thermal chamber (TRL 4) | To verify at TRL 4 | R8 |
| PR-009 | UR-012 | Usability | Calibration check | A field check with a 94 dB, 1 kHz calibrator shall take 10 minutes or less and store the offset on the node. | 10 | max | min | Timed trial (TRL 4) | To verify at TRL 4 | R9 |
| PR-010 | UR-008, UR-009 | Physical architecture | Installation, mass and wind | Two trained people shall fit it in 45 minutes with no drilling or pole wiring on poles of 60 to 140 mm; it shall weigh 3.5 kg or less (relaxed from 3 kg, NSM-DDR-002) and withstand 35 m/s gusts. | 45 min; 60 to 140 mm; 3.5 kg; 35 m/s | max; range; max; min | min; mm; kg; m/s | Analysis (NSM-CAL-001 H, TRL 3); timed trial and weighing (TRL 4) | Met on paper on mass (3.45 kg, margin 0.05 kg), wind and fit; install time to verify at TRL 4 | R10 |
| PR-011 | UR-011 | Software | Contaminated data | Intervals with wind above about 5 m/s or heavy rain shall be flagged: wind by a level-based flag, rain on the server from weather data (NSM-DDR-002). | 5 | about | m/s | Field comparison with a weather station (TRL 4) | To verify at TRL 4: method chosen, threshold needs field data | R11 |
| PR-012 | UR-013 | Electrical | Radio use | Radio use shall stay within the EU868 1 % duty cycle and The Things Network fair use of 30 s uplink a day, with a 15 minute interval at SF7 to SF9 lengthened automatically at SF10 to SF12. | 30; 1 | max | s/day; % | Analysis (NSM-CAL-001 F, TRL 3) | Met on paper: 23.7 s/day at SF9; 29.97 s/day at SF12, with almost no margin for join, time requests and retries | R12 |
| PR-013 | UR-014 | Physical architecture | Parts cost | The NoiseMap parts (BOM lines 7 to 14) shall cost at or under the value-engineering target; the FieldNode core is costed in the FieldNode repo and the full node cost is stated. | 100 | max | USD | Priced BOM (NSM-CAL-001 I, TRL 3) | Met on paper: USD 72.00, USD 28.00 under the target; full node USD 211.00 | R13 |
| PR-014 | UR-010 | Materials | Service life | The node shall last 5 years outdoors with a yearly windscreen change and one battery change. | 5 | min | years | Design review (TRL 3); ageing test (TRL 4) | To verify at TRL 4 | R14 |
| PR-015 | UR-015 | Software | Openness | Hardware, firmware, calibration method and data format shall be published under the repo licenses. | CERN-OHL-S-2.0; MIT | exact | n/a | Design review (TRL 3) | Met by design | R15 |
| PR-016 | UR-016 | Safety | Public notice | Each node shall be installed with a notice plate on the pole saying what is measured (levels only) and linking to this repository (NSM-DDR-001 D8). | 1 plate per pole | min | plate | Design review (TRL 3); inspection at installation (TRL 4) | To verify at TRL 4: the plate is part of the installation, not of the BOM | new |
| PR-017 | UR-009 | Safety | Falling-part retention | A safety lanyard of 2 mm stainless wire rope shall hold the microphone arm to the pole if the arm clamp slips. | 1 lanyard | min | lanyard | Design review (build plan Step 11, TRL 3); pull test at TRL 4 | Met by design (modelled in cad/src/model.py, BOM line 13) | new |

Categories: physical architecture, performance, materials, usability, packaging and transport, safety, electrical, software. Status: met on paper, met by design, at risk, not met, over target, withdrawn, to verify at TRL 4.

## Assumptions

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
