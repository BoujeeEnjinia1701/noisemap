---
doc_id: NSM-DDR-001
title: NoiseMap TRL 2 review decisions
project: NoiseMap
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the TRL 2 review items adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, and the items that remain open
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted. On 2026-09-25 Amish accepted all recommendations ("i accept all your recommendations, go with them across all repos"). D1 to D13 and O2 to O4 are decided by Amish, 2026-09-25: go with recommendation (see NSM-DDR-002). O1 has no recommendation and remains "Proposed, awaiting Amish".

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed nine items as "Proposed, awaiting Amish", eight of them with a recommendation, and the design precis NSM-PRC-001 v0.2 listed its key design choices as proposed. On 2026-09-25 Amish asked for this batch of repos to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed the NoiseMap items one by one. Every item that carries a recommendation is therefore adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. Items without a recommendation stay open. Later on 2026-09-25 Amish accepted all recommendations across the portfolio; the status column below records that, and NSM-DDR-002 lists what changed.

## Options considered

The options for each item are those in `docs/REVIEW.md` (session 2026-09-25, /populate, items 1 to 9) and in NSM-PRC-001 v0.2, Key design choices.

## Decision

*Table 1. Items decided.*

| # | Item | Recommendation adopted | Status |
| --- | --- | --- | --- |
| D1 | Budget (review item 1) | Option (b): keep `budget_usd` at $100 and redefine it to cover the NoiseMap parts only; the FieldNode core is costed in the FieldNode repo ($126.00, FND-CAL-001). The full per-node cost is stated wherever deployment is discussed. R13 is restated accordingly. No new budget figure was recommended, so `budget_usd` is unchanged. | Decided by Amish, 2026-09-25: go with recommendation |
| D2 | Privacy claim (item 2) | State in all public copy that the guarantee rests on open head firmware with read-out protection and a published build hash; never claim privacy "by physics". NSM-CAL-001 confirms this: the cable could carry a speech codec, and the radio a few minutes of it a day. | Decided by Amish, 2026-09-25: go with recommendation |
| D3 | Microphone (item 3) | A small adapter board that takes either the ICS-43434 (I²S, end of life) or the IM72D128 (PDM); the level processor accepts both interfaces. | Decided by Amish, 2026-09-25: go with recommendation |
| D4 | Processing location (item 4) | Levels computed in the head on a Cortex-M4F class board, so the cable carries levels only. | Decided by Amish, 2026-09-25: go with recommendation |
| D5 | Metrics and interval (item 5) | 15-minute records with 1-minute LAeq, LAeq, LAFmax, LAFmin, L10, L90 and LCeq (22 bytes). This also settles the problem statement's questions on 1-minute detail and C weighting. | Decided by Amish, 2026-09-25: go with recommendation |
| D6 | Wind flagging (item 6) | Study both options at TRL 3: done in NSM-CAL-001 section G (level-based wind flag with no added cost; cup anemometer about $25 and 0.15 kg). The choice between them is new item O3. | Decided by Amish, 2026-09-25: go with recommendation |
| D7 | Calibration (item 7) | A shared 94 dB, 1 kHz calibrator outside the per-node cost, and one side-by-side comparison with a class 1 meter per deployment. | Decided by Amish, 2026-09-25: go with recommendation |
| D8 | Public notice (item 8) | A notice on each pole saying what is measured, linking to this repository. | Decided by Amish, 2026-09-25: go with recommendation |
| D9 | Levels, never audio (precis choice) | No data storage and no radio in the head; firmware has no path that writes or sends samples. | Decided by Amish, 2026-09-25: go with recommendation |
| D10 | Standard FieldNode core (precis choice) | Standard FieldNode enclosure, 6 W panel and one cell; NoiseMap draws 12.2 mW, 12 % of FieldNode's 100 mW design allowance. | Decided by Amish, 2026-09-25: go with recommendation |
| D11 | Microphone position (precis choice) | Port 4.0 m above the sidewalk, 0.45 m from the pole face, facing up, on an arm with its own band clamp. | Decided by Amish, 2026-09-25: go with recommendation |
| D12 | A and C weighting (precis choice) | LAeq and statistics, plus LCeq for amplified bass. | Decided by Amish, 2026-09-25: go with recommendation |
| D13 | Head housing (precis component 8) | 3D-printed ASA tube with drip skirt and hydrophobic acoustic membrane. | Decided by Amish, 2026-09-25: go with recommendation |

*Table 2. Items raised at TRL 3 (O2 to O4 decided under NSM-DDR-002; O1 open).*

| # | Item | Status |
| --- | --- | --- |
| O1 | First co-design partner and street (review item 9, problem statement). No recommendation was made. | Proposed, awaiting Amish |
| O2 | R10 mass: the node is 3.32 kg against 3 kg (NSM-CAL-001 section H). Options: (a) pocket the V-blocks and saddle (about 3.10 kg, still over); (b) relax R10 to 3.5 kg; (c) both. Recommendation: (c). New at TRL 3. | Decided by Amish, 2026-09-25: go with recommendation (c); applied under NSM-DDR-002 |
| O3 | R11 wind flag method: (a) level-based flag from a Z-weighted band below 40 Hz, no cost; (b) add a cup anemometer on FieldNode's second port (about $25, 0.15 kg, which worsens O2). Rain is flagged on the server from weather data in both. Recommendation: (a), with a field comparison to set the threshold. New at TRL 3. | Decided by Amish, 2026-09-25: go with recommendation (a); the field comparison is TRL 4 work, on hold |
| O4 | R12 at SF10 and slower: lengthen the interval automatically (24 min at SF10, 87 min at SF12) on The Things Network, as FieldNode proposes. New at TRL 3; follows the FieldNode decision. | Decided by Amish, 2026-09-25: go with recommendation; interval rule written into NSM-PRC-001 and NSM-REQ-001 |

## Consequences

- `project.yaml`: only the TRL fields change. `budget_usd` stays at $100 (D1 redefines what it covers; no new figure was recommended). No reworded pitch or problem was recommended, so they are unchanged.
- NSM-PRB-001, NSM-PRC-001 and NSM-REQ-001 are revised to v0.3. The key design choices are no longer "proposed". R13 is redefined to cost the NoiseMap parts only, with the full node cost stated. R12's target is unchanged.
- The BOM now prices the FieldNode core at the FieldNode figure of $126.00 (TRL 2 used $119) and adds a street pole adapter (line 14), so the NoiseMap parts are $62.00 and the full node $188.00.
- NSM-CAL-001 corrects several TRL 2 figures (load 21 to 12.2 mW, autonomy 30 to 53 days, upper range 115 to 113 dBA, mass 2.3 to 3.32 kg); see its section on checks.
- The changes made when O2 to O4 were decided are listed in NSM-DDR-002.
- TRL 4 is on hold by Amish's instruction. Nothing in this record authorizes building or testing.
