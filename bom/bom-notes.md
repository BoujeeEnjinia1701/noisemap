# BOM notes

Costs are indicative (September 2026 estimates) until suppliers are selected. Line numbers match the callouts in `media/exploded.png` and the part keys in `cad/src/model.py`. Every line is priced; `docs/04-calcs/sizing.py` reads this file and checks the totals (NSM-CAL-001, section I).

- Lines 1 to 6 are the standard FieldNode core, $139.00, priced as in the FieldNode BOM after its design for construction (FND-DDR-003). Under NSM-DDR-001 D1 (decided by Amish, 2026-09-25: go with recommendation) the core is costed in the FieldNode repo; its small-pole V-blocks and bands stay in its price but are not fitted on a street pole.
- Lines 7 to 14 are NoiseMap parts, estimated at $72.00. Value-engineering target: USD 100 (`budget_usd`, a hypothetical control target, not a limit); the estimate is USD 28.00 under it. The full node is $211.00.
- Line 14, the street pole adapter, is new at TRL 3: FieldNode's V-blocks seat poles up to 71 mm, and street poles are 60 to 140 mm. The NoiseMap V-blocks use the FieldNode back plate's own V-block screw holes and band slots, so the plate needs no new holes.
- A cup anemometer for wind flagging (about $25) is not included: the level-based wind flag was decided instead (NSM-DDR-002, O3).
- The V-blocks (line 14) are sawn from 16 mm bar with four drilled lightening holes, and the arm saddle (line 7) is bent from 2.5 mm sheet with two bands and a bought tube flange (NSM-DDR-003).
- A sound calibrator (94 dB at 1 kHz) is a shared lab tool and is not in the per-node cost (D7).
- The street pole is not part of the BOM.
