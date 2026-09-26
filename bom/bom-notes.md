# BOM notes

Costs are indicative (September 2026 estimates) until suppliers are selected. Line numbers match the callouts in `media/exploded.png` and the part keys in `cad/src/model.py`. Every line is priced; `docs/04-calcs/sizing.py` reads this file and checks the totals (NSM-CAL-001, section I).

- Lines 1 to 6 are the standard FieldNode core, $126.00, priced exactly as in the FieldNode BOM (FND-CAL-001). Under NSM-DDR-001 D1 (decided by Amish, 2026-09-25: go with recommendation) the core is costed in the FieldNode repo and is outside the NoiseMap budget.
- Lines 7 to 14 are NoiseMap parts, $62.00, against the $100 `budget_usd`, a margin of $38.00. The full node is $188.00.
- Line 14, the street pole adapter, is new at TRL 3: FieldNode's V-blocks seat poles up to 71 mm, and street poles are 60 to 140 mm. The small V-blocks and bands stay in the FieldNode core price, so the full node cost is slightly conservative.
- A cup anemometer for wind flagging (about $25) is not included: the level-based wind flag was decided instead (NSM-DDR-002, O3).
- The V-blocks (line 14) and the arm saddle (line 7) are pocketed for mass (NSM-DDR-002, O2); prices are unchanged at this indicative level, although pocketing adds machining time.
- A sound calibrator (94 dB at 1 kHz) is a shared lab tool and is not in the per-node cost (D7).
- The street pole is not part of the BOM.
