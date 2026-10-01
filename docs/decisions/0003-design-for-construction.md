---
doc_id: NSM-DDR-003
title: NoiseMap design for construction
project: NoiseMap
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction and open for his review
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** draft. Every change in Tables 1 and 2 was made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review. The items in Table 3 are proposed, awaiting Amish.

## Context

On 2026-09-30 Amish approved the build plan format and asked for it across all repos, and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The NoiseMap model of NSM-DDR-002 showed what the node does but was a massing model: several parts could not be made by the stated process, or had no fixing, and the FieldNode core inside it was the old FieldNode concept rather than the constructable FieldNode accepted under FND-DDR-003.

The changes keep what NoiseMap does: the microphone port 4.0 m up, 0.45 m from the pole face and pointing up; the 3 mm port and 0.5 mm front cavity that the frequency response calculation rests on; the 90 mm windscreen; levels only over the M12 cable; the standard FieldNode core; 60 to 140 mm poles with no drilling of the pole; the core and the arm turning independently. Nothing here changes the pitch or the safety case. Every change is in `cad/src/model.py`, which now runs 62 constructability checks (`python cad/src/model.py --check`): parts that must touch do touch, parts that must stay apart are apart by the stated clearance, no NoiseMap part overlaps another, and the V contacts of a 60 mm and a 140 mm pole stay inside the V-blocks and the saddle. All 62 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The FieldNode core was the old FieldNode massing model: a tube bracket standing on the lid, no fixing between the box and the back plate, ports in one row. FieldNode has since been made constructable (FND-DDR-003, accepted by Amish on 2026-09-30). | The core is now the constructable FieldNode of FND-DWG-001 Rev P3, copied unchanged into `cad/src/fieldnode_core.py` and set out from the street pole. It is built to its own plan, FND-BLD-001, without its small-pole V-blocks and band clamps, which a street pole node does not fit. | One design for the core across the portfolio; the FieldNode build plan already shows how to make it. |
| P2 | Street pole V-blocks 110 x 60 x 40 mm pocketed from top and bottom to 4 mm walls and an 8 mm web: a CNC milling job, not a workshop one. No fixing to the back plate was shown, and the bands were drawn as rings cut short at the blocks, with no path to anything. | V-blocks 112 x 63 x 16 mm sawn from 70 x 16 mm bar, with a true 90 degree V (106 mm mouth, point 10 mm from the back face) and four 14 mm drilled lightening holes. Each is held by two M4 countersunk screws in FieldNode's own V-block screw holes (18 mm each side of centre). Each band runs round the pole, along the block's sides, under a 9 x 2 mm rebate at each back corner, through FieldNode's own band slots (51 mm each side) and across the box side of the plate. | Sawing, filing and drilling only. The FieldNode back plate needs no new holes. The pole sits where the concept put it, so every load and the core's position are unchanged. 16 mm bar and the holes keep the mass of the pocketed blocks. A band cannot pass the FieldNode slots without the rebates, because the blocks are wider than the slot spacing. |
| P3 | Arm saddle: a 10 mm plate 60 x 90 mm with a 6 mm milled pocket on the pole side (a milling job), seating a 60 mm pole on the pocket floor so it could rock; one band, drawn as a ring cut short at the saddle. | A channel bent from 2.5 mm 5052-H32 sheet, 114 mm wide, web 124 mm tall, flanges standing 65 mm out, each flange cut with a 90 degree V (109 mm mouth). Two bands, 40 mm above and below the arm, run round the pole, through slots in the web and across its outside. | A bending shop can make it. The pole bears on four V edges at every size from 60 to 140 mm. Two bands resist twist with a factor of 9.4 (one band: 4.2) [NSM-CAL-001 H6]. |
| P4 | The arm tube was butted against the saddle with no fixing; only welding could join them. | A bought aluminium tube flange (railing floor flange) bolted to the web with three M5 screws, nyloc nuts inside the channel; the tube goes 25 mm into its socket and an M5 cross bolt passes through both. | Bought part, hand tools only, and the arm can be taken off the saddle. |
| P5 | At the head, the tube ended against a collar ring round the head with no fixing. | An arm socket printed on the head housing (33 mm OD, 25 mm deep); the tube goes to the bottom of it and an M4 cross bolt passes through both. The arm tube is now 383 mm between the two sockets. | One printed part instead of two, and the head is held square to the arm. The microphone position is unchanged. |
| P6 | Inside the head, the processor board and the microphone board floated; the bottom was open, and the cable was to enter "through a gland" that the model did not have. | Two printed card guides hold the processor board. The microphone board is held by two M2 screws on two printed bosses under the top plate, with a 0.5 mm closed-cell gasket round the port that forms the 3 mm, 0.5 mm deep front cavity. A printed bottom cap with an M16 cable gland closes the bottom, held by two M3 screws through the head wall. | Every part inside the head now has a fixing. The gasket keeps the front cavity the calculations use, so the 36.2 kHz port resonance stands [NSM-CAL-001 B3]. |
| P7 | The drip skirt was a flat 12 mm overhang that a printer cannot make without support. | The same 64 mm skirt, a 4 mm rim with a 45 degree cone under it. | Prints without support; sheds water the same way. |
| P8 | The windscreen was bored 41 mm for a 40 mm head, so nothing held it. | Bored 40 mm, pushed down over the head until it sits on the port membrane. | The foam grips the head; same 90 mm ball and position. |
| P9 | The bird spike stood in the top of the foam with nothing holding it. | A 3 mm stainless rod with an M3 thread, screwed into a heat-set insert in a boss on the skirt 26 mm from the head axis; it rises through the foam to 160 mm above the port, the height the concept gave. Unscrew it before lifting the windscreen off. | It has a fixing and keeps birds off the ball. Its effect on the response is open (Table 3, A1). |
| P10 | The safety lanyard was in the BOM but had no attachment. | A 2 mm stainless wire rope with thimbles and ferrules, looped round the pole above the saddle and round the arm beside the flange. | It holds the arm if the bands slip. |
| P11 | The sensor cable ran through other parts and had no route. | It runs from the core's port A down below the back plate, up the pole on the side away from the core, outside the saddle, along the side of the arm and into the gland from below with a drip loop, tied to the pole and the arm. | A real path, clear of every part [model checks]. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Mass | 3.45 kg, unchanged, against R10's 3.5 kg; margin 0.05 kg [NSM-CAL-001 H2]. | The second band, flange, cap, gland and fixings added mass; leaving off FieldNode's small-pole V-blocks and bands (0.22 kg) and the lighter V-blocks paid for it. |
| Cost | BOM lines 1 to 6 follow the FieldNode BOM after FND-DDR-003 ($126.00 to $139.00). Lines 7, 8, 12 and 13 repriced. NoiseMap parts $62.00 to $72.00; value-engineering target $100, so $28.00 under; full node $211.00 [I1], [I2]. `budget_usd` unchanged. | Parts added for construction. |
| Arm and clamp | Arm stress factor 24 to 27, clamp twist factor 4.2 to 9.4, 96 N added to the pole (was 97 N) [H3] to [H7]. | Shorter tube, two bands. |
| Drawing | NSM-DWG-001 Rev P2 to P3; making sketches NSM-DWG-101 to 106 added. | Follows the model. |
| Documents | NSM-CAL-001 v0.3; NSM-PRC-001 and NSM-REQ-001 updated for the new figures. No requirement changed status. | Follows the model. |

*Table 3. Proposed, awaiting Amish.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | The bird spike now stands 26 mm off the microphone axis instead of on it, inside the windscreen. A 3 mm rod that close may change the response slightly at the highest frequencies. | (a) the side spike as modelled, and measure the response with and without it at TRL 4; (b) no spike, and replace the foam more often; (c) a spike on a wire hoop clipped to the skirt, clear of the foam. | (a): it is the simplest fixing, and the response is already to be measured at TRL 4 (R5 at risk). |
| A2 | The R10 mass margin is still 0.05 kg on catalogue masses. | (a) accept, weigh the prototype at TRL 4; (b) look for more mass now (a 2 mm saddle saves about 0.03 kg). | (a). |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan NSM-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`); open items are in the design decisions register NSM-DEC-001.
- Requirement status is unchanged: 0 not met, 3 at risk (R3, R4, R5), 4 not verifiable at TRL 3, 4 met on paper, 4 met by design (NSM-CAL-001 v0.3).
- The photoreal renders (`media/render-*.png`), `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` still show the concept arm saddle, V-blocks, head and FieldNode bracket; they need updating on Amish's Mac, where Blender is.
- If FieldNode changes its back plate, the V-block screw holes, the band slots or the clamp heights, the street pole V-blocks must follow, and `cad/src/fieldnode_core.py` must be copied again.
