---
doc_id: NSM-DEC-001
title: NoiseMap design decisions register
project: NoiseMap
doc_type: Design decisions register
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the build plan; budget treated as a value-engineering target
  - version: "0.2"
    date: '2026-10-02'
    author: Amish Chadha
    change: Amish approved the recommendations for open decisions 1 to 5 (NSM-DDR-003 accepted); moved to decisions made
---

# NoiseMap design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The tube flange's three holes fall on a 45 mm circle, its base is 60 mm across or less, and its socket takes a 25 mm tube 25 mm deep | The saddle web holes and the band clearance (4 mm) assume it | NSM-DDR-003, P4 |
| 2 | The processor board is no wider than 26 mm and no longer than 70 mm | It must fit the card guides printed in the head | NSM-DDR-003, P6 |
| 3 | The windscreen is a 90 mm ball and takes a 40 mm bore, or comes bored to 40 mm | The push fit on the head and the head's position in the ball | NSM-DDR-003, P8 |
| 4 | The band clamps close on poles from 60 to 140 mm, and the torque that gives 1,000 N of preload | The calculation note assumes that preload for every clamp margin | NSM-CAL-001, H6 |
| 5 | The membrane's acoustic transparency and size from its maker's datasheet | It sits in the sound path; its effect is part of R5 | NSM-DDR-001, D13 |
| 6 | 70 x 16 mm aluminium bar is stocked; if only 20 mm is, the blocks gain about 0.11 kg | The R10 margin is 0.05 kg | NSM-CAL-001, H2b |
| 7 | The FieldNode back plate as built matches FND-DWG-101 (V-block screw holes 18 mm each side, band slots 51 mm each side, at 20 and 270 mm up) | The street pole V-blocks use those holes and slots | NSM-DDR-003, P2 |

## Value engineering

Value-engineering target: USD 100 for the NoiseMap parts (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 72.00 (USD 28.00 under the target). The full node with the FieldNode core, which is costed in the FieldNode repository, is USD 211.00. Main cost drivers and savings worth trying:

- The largest NoiseMap lines are the arm and saddle with its flange and two bands (USD 16), the street pole adapter (USD 10), the sensor cable and gland (USD 9), the windscreen and spike, the level processor and the fixings (USD 8 each).
- Making the design constructable added USD 10 (two-band saddle and tube flange USD 6, fixings and lanyard USD 2, cable gland USD 1, head cap USD 1). The FieldNode core rose from USD 126 to USD 139 under its own design for construction.
- Savings worth trying: a printed or folded tube socket in place of the bought flange (about USD 3); one band size bought in a box for all four bands; an M12 cable with a moulded strain relief in place of the separate gland; the processor and microphone on one board once the head design settles (TRL 4 work).

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D13: budget scope (NoiseMap parts only), privacy resting on open firmware, dual-footprint microphone, processing in the head, 15-minute records, shared calibrator, public notice, standard FieldNode core, microphone 4.0 m up and 0.45 m off the pole, A and C weighting, printed ASA head | Amish: "i accept all your recommendations, go with them across all repos." | NSM-DDR-001, NSM-DDR-002 |
| 2026-09-25 | R10 relaxed to 3.5 kg with lighter V-blocks and saddle (O2); level-based wind flag (O3); interval rule at slow data rates (O4) | Amish, same instruction | NSM-DDR-002 |
| 2026-09-30 | FieldNode core made constructable (the core NoiseMap now uses) | Amish: "i accept your recommended changes on design that are currently being sent across for my approval" | FieldNode FND-DDR-003 |
| 2026-09-30 | Make every design physically buildable while drawing the build plan; keep open decisions out of the build plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | NSM-DDR-003 (changes accepted on 2026-10-02, below) |
| 2026-10-01 | `budget_usd` is a value-engineering target, not a limit | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens" | This register, NSM-CAL-001 v0.3 |
| 2026-10-02 | Design for construction accepted: the changes P1 to P11, as made | Amish: "i approve your recommendations for all 555 open decisions." | NSM-DDR-003 |
| 2026-10-02 | Bird spike: the side spike in the skirt boss, 26 mm off the microphone axis, as modelled; the response is measured with and without it at TRL 4 | Amish: "i approve your recommendations for all 555 open decisions." | NSM-DDR-003, A1 |
| 2026-10-02 | R10 mass margin of 0.05 kg accepted; the prototype is weighed at TRL 4 | Amish: "i approve your recommendations for all 555 open decisions." | NSM-DDR-003, A2 |
| 2026-10-02 | First co-design partner to approach: a city environmental noise team or a university acoustics group that can put a Class 1 reference sound level meter beside the node on the test street; a Sensor.Community group is a useful second contact for volunteer hosts | Amish: "i approve your recommendations for all 555 open decisions." | NSM-DDR-001, O1 |
| 2026-10-02 | M12 sensor port pinout: ask FieldNode to adopt its own candidate pinout for both ports (pin 1 switched rail, pin 2 data A, pin 3 ground, pin 4 data B, pin 5 analog); NoiseMap uses pin 1 at 3.3 V, pin 3 ground and pins 2 and 4 for the UART pair | Amish: "i approve your recommendations for all 555 open decisions." | FieldNode FND-DDR-001, O2 |
