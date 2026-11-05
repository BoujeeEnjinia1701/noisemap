---
doc_id: NSM-DDR-004
title: NoiseMap concept selection
project: NoiseMap
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-11-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-11-02'
  author: Amish Chadha
  change: 'First issue: concept selection among options A, B and C, proposed to Amish'
---

# 0004: Concept selection

- **Date:** 2026-11-02
- **Status:** Proposed, awaiting Amish. Nothing here is decided.

## Context

Kit 1.8 requires at least two concept options with different working principles, scored against the user requirements. NoiseMap was designed before kit 1.8, so the current design is option A and is not redesigned without Amish's go. Options B and C were added and modelled at detail level D3 (kit 1.9).

## Options

- **A, pole clamp node:** solar, own cell, LoRaWAN, microphone 4 m up on an arm (the current design).
- **B, balcony post node:** USB power, home Wi-Fi, microphone and radio on one board in a clamped box.
- **C, luminaire socket node:** twist-locks into the luminaire receptacle, takes luminaire power, LoRaWAN, microphone about 6 m up.

## Scores

Weighted totals from NSM-OPT-001 Table 2 (maximum 245): A 171, B 163, C 152. A leads B by 4.7 %, which is inside the 10 % band of STANDARDS section 21, so no pick is made. A leads C by 11.1 %.

## Decision requested

| # | Decision | Options | Recommendation |
| --- | --- | --- | --- |
| 1 | Which concept is carried forward | (a) A only; (b) B only; (c) A as the street node and B as a low-cost companion for residents; (d) C | Proposed, awaiting Amish: no pick between A and B. If forced, (c) serves both user groups, but it adds a second design to maintain and changes the scope, so it is Amish's to decide. C is not recommended (mains voltage, work at height, loses the no-electrical-connection constraint) |

## Consequences

Until Amish decides, option A stays the design of record: the drawing, priced BOM and build plan describe A only; `concept_chosen` is "A (proposed)". If B is chosen, the BOM, build plan and calculations for B must be written (not started). If C is chosen, a mains-safety review (NSM-REG-001 G12) comes first.
