---
doc_id: NSM-REQ-001
title: NoiseMap requirements
project: NoiseMap
doc_type: Requirements
version: "0.2"
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
---

# NoiseMap requirements

These requirements are proposed targets for concept review, awaiting Amish, and must be revised with a co-design partner before the design is frozen. Status is judged against the first-order estimates in NSM-PRC-001; "met" means met on paper only. Two requirements are **not met** by the current concept (R11 wind flagging and R13 cost), one is met only in part (R12 at slow data rates), and three are at risk (R3, R4 at the low end, R5 at low frequencies).

Design case: one node on a street pole 0.45 m behind the curb, microphone about 4 m above the ground and 0.45 m from the pole face, in a mixed street with traffic by day and bars at night.

Table 1. Requirements.

| ID | Requirement | Target | Verification | Concept status |
| --- | --- | --- | --- | --- |
| R1 | Privacy: no audio samples are stored or leave the microphone head; only levels cross the cable or the radio | No data storage in the head; cable carries levels only; head firmware published with a build hash | Design review, firmware audit, cable capture | Met by design; see NSM-PRC-001 on the limits of the physical argument |
| R2 | Reported metrics | Per 15 min: 1-minute LAeq, LAeq, LAFmax, LAFmin, L10, L90, LCeq, device status | Design review | Met by design (22 bytes per record) |
| R3 | Accuracy of LAeq,15min against a co-located class 1 meter | Within ±2 dB from 40 to 100 dBA, after field calibration | Side-by-side field test | At risk: housing, windscreen and reflections unverified |
| R4 | Measuring range | 35 to 110 dBA | Bench test with calibrator and reference source | Upper end met (about 115 dBA); **at risk** at 35 dBA (self-noise about 29 dBA) |
| R5 | Frequency weighting | A and C weighting as defined in IEC 61672-1, within class 2 tolerances from 63 Hz to 8 kHz (goal) | Bench test against a reference meter | At risk below about 60 Hz (microphone roll-off) |
| R6 | Time stamps | Each record time-stamped within 2 s of UTC | Design review (LoRaWAN network time) | Plausible |
| R7 | Energy | Energy neutral at 1.5 peak sun hours; 14 days without sun | Energy budget, bench test | Met (about 5.8 Wh/day for 0.51 Wh/day; about 30 days) |
| R8 | Ingress and weather | IP65 enclosure; microphone head survives driving rain; -20 °C to +50 °C | Spray test, thermal chamber | By design, unverified |
| R9 | Calibration check | Field check with a 94 dB, 1 kHz calibrator in 10 min or less; offset stored on the node | Timed trial | Plausible |
| R10 | Installation and mass | Two trained people, 45 min, no drilling or pole wiring; 3 kg or less; withstands 35 m/s gusts | Timed trial, weighing, bracket calculation | Met on mass (about 2.3 kg); wind load about 50 N to check |
| R11 | Contaminated data | Intervals with wind above about 5 m/s or heavy rain are flagged | Field comparison with a weather station | **Not met:** no wind or rain sensing in the concept |
| R12 | Radio use | Within EU868 1 % duty cycle and The Things Network fair use (30 s uplink per day) | Airtime calculation | Met at SF9 or faster (about 24 s/day); **not met** at SF10 without 30-minute records |
| R13 | Parts cost | $100 or less per node | Priced BOM | **Not met:** about $171 (NoiseMap-specific parts about $52) |
| R14 | Service life | 5 years outdoors, with a yearly windscreen change and one battery change | Design review, UV-stable materials | Unverified |
| R15 | Openness | Hardware, firmware, calibration method and data format published under the repo licenses | Design review | Met by design |

Table 2. Assumptions behind the targets.

| Assumption | Value | Source or basis |
| --- | --- | --- |
| Microphone height | about 4 m above the ground | 4.0 ± 0.2 m assessment height for EU strategic noise maps ([Directive 2002/49/EC, Annex I](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32002L0049)) |
| Quietest night level to resolve | about 35 dBA | Quiet residential street at night (estimate) |
| Loudest level to resolve | about 110 dBA | Close pass of a loud motorcycle or siren (estimate) |
| Peak sun hours, winter design case | 1.5 h | Mid-latitude winter (estimate) |
| Wind speed that spoils readings with a foam windscreen | about 5 m/s | Common practice (estimate, to be checked) |
| Microphone data | 65 dB SNR, 120 dB SPL overload | ICS-43434 product page ([TDK InvenSense](https://invensense.tdk.com/products/ics-43434/)) |

> **Safety:** Requirements R8 and R10 involve work at height beside traffic and a lithium cell. See the safety section of NSM-PRC-001.
