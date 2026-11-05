---
doc_id: NSM-FEA-001
title: NoiseMap feasibility assessment
project: NoiseMap
doc_type: Feasibility assessment
version: "0.1"
status: Draft
date: '2026-11-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-11-02'
  author: Amish Chadha
  change: First issue (kit 1.8 pipeline)
---

# NoiseMap feasibility assessment

The pole clamp node (option A) is feasible as a paper design: the physics and arithmetic hold (NSM-STM-001, all 24 claims within known science, 3 of them closed by calculation), it is modelled at detail level D3 with 89 parts and no overlaps, and its parts cost is USD 72.00 against a USD 100 target. What cannot be settled on paper is measurement quality: accuracy, range at the quiet end and frequency response are rated at risk and need a class 1 reference meter at TRL 4, which is on hold. Method: STANDARDS section 23.

Table 1. Feasibility by aspect (option A unless stated).

| Aspect | Assessment | Rating | Risks and notes | Evidence |
| --- | --- | --- | --- | --- |
| Design | Levels computed in the head, a FieldNode core for power and radio, an arm to put the microphone 4.0 m up and 0.45 m off the pole. Dimensions and interfaces are modelled and 62 fit checks pass | High | Mass margin is 0.05 kg (R10, now PR-010): any added part needs a mass check | NSM-STM-001 S10 to S12, NSM-CAL-001 H, cad/fidelity.json |
| Measurement quality | Microphone data support 27.9 to 119 dB SPL with the IM72D128 fitted by default (103 to 108 dBA with the ICS-43434) and A and C weighting after equalizing; expanded uncertainty 2.9 dB on assumed terms against 2 dB | Medium | Membrane, windscreen and head diffraction are unknown; facade bias up to 2.4 dB before a site correction; these need a reference meter | NSM-CAL-001 A to C, NSM-PRS-001 PR-003 to PR-005 |
| Materials | Aluminium sections, stainless bands and fixings, printed ASA head, polycarbonate box, open-cell foam | High | Foam and membrane ageing; galvanic couple is small by area ratio | NSM-STM-001 S15, S16 |
| Manufacturing and assembly | V-blocks sawn from 16 mm bar, saddle bent from 2.5 mm sheet, head printed in ASA; a making sketch for each made part and a picture for each step | High | Needs sawing, bending, printing and fine soldering; no certified trade; bought tube flange dimensions to confirm when parts are bought | NSM-BLD-001, NSM-DDR-003 |
| Power and controls | 12.2 mW load, 5.81 Wh/day harvest at 1.5 sun hours, 53 days without sun; no feedback loop | High | Cold-weather charging relies on FieldNode's lockout | NSM-STM-001 S5, S6, S17, NSM-CAL-001 D and E |
| Radio | 22 byte record, 23.7 s/day at SF9, interval rule at slow data rates | High | Needs gateway coverage; fair use is a community rule | NSM-STM-001 S7, S8, S18 |
| Supply of parts | The ICS-43434 is listed end of life by its maker; the IM72D128 is the alternative on the same adapter board | Medium | Single sources for the modules; prices indicative (September 2026 estimates) | bom/bom.csv, NSM-DDR-001 D3 |
| Regulatory | No certification claimed; GDPR, radio and battery items to assess | Medium | See NSM-REG-001 | NSM-REG-001 |
| Concept options B and C | Both are feasible as designs (STM S20 to S24). B is cheap and simple but measures at a facade; C needs mains inside and a lighting operator | B Medium, C Low | C fails the no-electrical-connection constraint of the pitch | NSM-OPT-001 |

Ratings: High, Medium, Low.
