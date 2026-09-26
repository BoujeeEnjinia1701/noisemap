---
doc_id: NSM-DDR-002
title: NoiseMap recommendations accepted
project: NoiseMap
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's acceptance of all recommendations and the changes made in this repo
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted. Every item below with a recommendation is decided by Amish, 2026-09-25: go with recommendation. Items without a recommendation remain "Proposed, awaiting Amish".

## Context

On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." NSM-DDR-001 had adopted D1 to D13 for TRL 3 work, open for his review, and left O1 to O4 as "Proposed, awaiting Amish". O2, O3 and O4 each carried a recommendation; O1 did not. TRL 4 remains on hold by Amish's instruction, and the repo stays at TRL 3.

## Decision

*Table 1. Items newly decided and what changed in the repo.*

| # | Item | Decision (the recommended option) | What changed |
| --- | --- | --- | --- |
| D1 | Budget scope | `budget_usd` stays $100 and covers the NoiseMap parts only; FieldNode core costed in FieldNode | No change to `budget_usd` ($100); R13 already restated in NSM-REQ-001 v0.3; wording updated to "decided" |
| D2 | Privacy claim | Guarantee rests on open head firmware, read-out protection and a published build hash; never "by physics" | Status wording only |
| D3 | Microphone | Adapter board for ICS-43434 or IM72D128 | Status wording only |
| D4 | Processing location | Levels computed in the head | Status wording only |
| D5 | Metrics and interval | 15-minute, 22-byte records with 1-minute LAeq and statistics | Status wording only |
| D6 | Wind flagging study | Both options studied at TRL 3 | Superseded by O3 |
| D7 | Calibration | Shared 94 dB calibrator; one class 1 side-by-side per deployment | Status wording only; the side-by-side is TRL 4 work, on hold |
| D8 | Public notice | Notice on each pole linking to the repository | Status wording only |
| D9 to D13 | Precis choices | Levels only; standard FieldNode core; microphone at 4.0 m, 0.45 m off the pole; A and C weighting; printed ASA head | Status wording only |
| O2 | R10 mass | Option (c): pocket the V-blocks and saddle, and relax R10 from 3 kg to 3.5 kg | `cad/src/model.py`: V-blocks pocketed from top and bottom (4 mm walls, 8 mm web), saddle pocketed 6 mm deep; the V notch geometry was also corrected (v0.1 had cut each block to a flat 10 mm plate). STEP and STL re-exported. NSM-DWG-001 Rev P1 to P2. NSM-REQ-001 R10 target 3 kg to 3.5 kg. NSM-CAL-001 v0.1 to v0.2: mass 3.32 kg (flawed geometry) to 3.45 kg pocketed, 3.96 kg solid; R10 not met to met on paper, margin 0.05 kg. BOM lines 7 and 14 describe the pockets; prices unchanged |
| O3 | R11 wind flag method | Option (a): level-based flag from the Z-weighted band below 40 Hz; rain flagged on the server | No anemometer added. NSM-PRC-001 and NSM-REQ-001 state the method; NSM-CAL-001 records the anemometer as a rejected option. The field comparison that sets the threshold is TRL 4 work, on hold |
| O4 | R12 airtime at SF10 and slower | Lengthen the interval automatically: 24 min at SF10, 48 min at SF11, 87 min at SF12 | Firmware rule written into NSM-PRC-001 (how it works, step 5) and NSM-REQ-001 R12. NSM-CAL-001 [F2c]: at most 30.0 s/day at every spreading factor; R12 at risk to met on paper. Aligns with FieldNode's interval item (cross-repo action) |

*Table 2. Items still open.*

| # | Item | Status |
| --- | --- | --- |
| O1 | First co-design partner and street. No recommendation was made. | Proposed, awaiting Amish |

## Consequences

- Requirement status (NSM-CAL-001 v0.2): 0 not met, 3 at risk (R3, R4, R5), 4 not verifiable at TRL 3 (R8, R9, R11, R14), 4 met on paper (R7, R10, R12, R13), 4 met by design (R1, R2, R6, R15). Before: 1 not met (R10), 4 at risk (R3, R4, R5, R12).
- The R10 margin is only 0.05 kg; any added part needs a mass check. Shorter V-blocks or dropping FieldNode's unused small-pole V-blocks would add margin.
- NSM-PRB-001, NSM-PRC-001 and NSM-REQ-001 go from v0.3 to v0.4; NSM-DDR-001 from v0.1 to v0.2; NSM-CAL-001 from v0.1 to v0.2. Concept media are re-rendered from the updated model.
- Cross-repo actions, not made here: ask FieldNode for a street pole mounting variant for 60 to 140 mm poles; align the interval rule with FieldNode's interval item; agree the M12 pinout (FieldNode O2).
- TRL 4 is on hold by Amish's instruction. `trl` and `trl_target` stay at 3. Nothing here authorizes building, testing, purchasing, PCB work or firmware beyond a sketch.
