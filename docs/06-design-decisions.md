---
doc_id: NSM-DEC-001
title: NoiseMap design decisions register
project: NoiseMap
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the build plan; budget treated as a value-engineering target
---

# NoiseMap design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Accept the design for construction | Accept the changes P1 to P11 as made, or ask for changes | Accept: each keeps what the node does, and the model's 62 constructability checks pass | Every made component and joint | NSM-DDR-003 |
| 2 | Bird spike position | (a) side spike in the skirt boss, 26 mm off the microphone axis, as modelled, and measure the response with and without it at TRL 4; (b) no spike, change the foam more often; (c) a spike on a wire hoop clipped to the skirt | (a) | Spike, skirt boss (sections 3.5 and 3.10) | NSM-DDR-003, A1 |
| 3 | R10 mass margin of 0.05 kg | (a) accept and weigh the prototype at TRL 4; (b) look for more mass now, for example a 2 mm saddle (about 0.03 kg) | (a) | None now | NSM-DDR-003, A2 |
| 4 | First co-design partner and street | Partner and site to be named | None yet | Pole size and site checks at installation; not part of the bench build | NSM-DDR-001, O1 |
| 5 | M12 sensor port pin assignment | Agreed across FieldNode's adopting projects (FieldNode's own open decision) | None yet; NoiseMap needs 3.3 V, ground and one UART pair | Which conductor goes where at the FieldNode end of the cable | FieldNode FND-DDR-001, O2 |

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
| 2026-09-30 | Make every design physically buildable while drawing the build plan; keep open decisions out of the build plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | NSM-DDR-003 (changes open for review, item 1 above) |
| 2026-10-01 | `budget_usd` is a value-engineering target, not a limit | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens" | This register, NSM-CAL-001 v0.3 |
