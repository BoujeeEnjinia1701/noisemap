# Review note: NoiseMap

## Session 2026-09-25: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (NSM-PRB-001 v0.2): problem, users, operating context, constraints, prior work with cited sources (EEA, WHO via EEA, EU Directive 2002/49/EC, US EPA, SONYC, DNMS, Bruitparif, IEC 61672-1), out of scope, open questions; co-design checklist kept.
- `docs/02-concept.md` (NSM-PRC-001 v0.2): how it works, 12 numbered components, first-order numbers with assumptions, key design choices, safety, privacy and data-use notes, open questions.
- `docs/03-requirements.md` (NSM-REQ-001 v0.2): 15 measurable requirements (R1 to R15) with targets, verification and concept status, plus a design case and assumptions.
- `cad/src/concept_media.py`: massing model of the node (FieldNode enclosure, board, cell, 6 W panel and bracket, pole clamps, microphone arm, printed head, MEMS microphone, level processor, windscreen with bird spike, M12 cable), each part with a BOM number; street pole, sidewalk, road and a 1.75 m person as grey context. Also draws a two-row data and energy flow diagram in the kit's style, because the kit's flow function takes only numeric losses.
- `media/`: `hero.png`, `concept-blueprint.png`, `.pdf` and `.svg`, `model.glb` and `viewer.html`, `exploded.png` (callouts 1 to 12 match the BOM), `cutaway.png` (enclosure and microphone head sectioned), `flow.png` (estimates labeled). Temporary `media/_views*` folders removed.
- `bom/bom.csv`: 13 lines with indicative USD prices; `bom/bom-notes.md` updated.
- `README.md`: hero image and links line, then the required sections (Concept rationale, Burning platform, Where it could be used with industry and country tables, What sparked the idea) expanded with cited figures; Problem, Concept, Key components and Safety updated to match.
- `project.yaml`: unchanged (pitch and problem remain correct).
- `docs/pdf/`: branded PDFs of the three controlled documents.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Measuring range | about 35 to 115 dBA (self-noise about 29 dBA) | R4 at risk at the low end |
| Average load | about 21 mW, 0.51 Wh/day | Within FieldNode's about 115 mW sensor allowance |
| Autonomy without sun | about 30 days | R7 met |
| Winter harvest, standard 6 W panel | about 5.8 Wh/day | R7 met |
| Uplink | 22 bytes per 15 min, about 24 s/day airtime at SF9 | R12 met at SF9; not met at SF10 |
| Mass on pole | about 2.3 kg | R10 met |
| Parts cost | about $171 (FieldNode core about $119, NoiseMap parts about $52) | R13 not met ($100 budget) |

Requirements not met or at risk:

- **R13 (cost) not met:** about $171 against $100.
- **R11 (flag wind and rain) not met:** the concept has no wind or rain sensing.
- **R12 (radio) not met at SF10:** 96 records a day would take about 47 s of airtime against the 30 s fair-use limit; 30-minute records would be needed on distant links.
- **R3 (accuracy) at risk:** housing, membrane, windscreen and pole reflections are unverified.
- **R4 at risk below about 35 dBA** and **R5 at risk below about 60 Hz** (microphone limits).

### Proposed, awaiting Amish

1. **Budget.** Options: (a) raise `budget_usd` to $175; (b) keep $100 and cost the FieldNode core under FieldNode, leaving about $52 of NoiseMap parts, within budget; (c) a cheaper mains or USB powered Wi-Fi variant like DNMS where power exists, which drops the solar and LoRaWAN core. Recommendation: (b), with the full per-node cost of about $171 stated wherever deployment is discussed. `project.yaml` is unchanged.
2. **Privacy claim.** The cable and radio links are far too slow for raw audio but could in principle carry a heavily compressed speech codec, so the guarantee rests on open head firmware with read-out protection and a published build hash. Recommendation: state it this way in all public copy, and do not claim privacy "by physics".
3. **Microphone.** ICS-43434 (widely used, but listed by TDK as end of life) or Infineon IM72D128 (supported by DNMS; specification not checked in this session). Recommendation: a small adapter board that takes either.
4. **Processing in the head** (Cortex-M4F class board) rather than on FieldNode's STM32WL. Recommendation: head, so the cable carries levels only.
5. **Metrics and interval:** 15-minute records with 1-minute LAeq, L10, L90, LAFmax, LAFmin and LCeq. Recommendation: adopt.
6. **Wind flagging** (R11): infer from the level data, or add a small wind sensor at extra cost. Recommendation: study both at TRL 3.
7. **Calibration:** a shared 94 dB, 1 kHz sound calibrator (not in the per-node cost) and one side-by-side comparison with a class 1 meter per deployment. Recommendation: adopt.
8. **Public notice** on each pole linking to this repository. Recommendation: yes.
9. **First partner and street** for co-design.

### Safety concerns

- Work at height beside traffic when installing; pole owner's permission, trained crews, traffic management.
- Falling parts from 4 m: safety lanyard on the arm; about 50 N wind load on the panel to check.
- LiFePO4 cell (about 19 Wh): fusing and cold-charge lockout.
- Hearing: bench tests near the upper range need hearing protection.
- Misuse of data: readings are indicative and must not be presented as certified measurements.
- Privacy: any change to the head firmware or to a higher data-rate link needs a fresh privacy review.

### Notes and gaps

- The FieldNode pole kit fits 40 to 60 mm poles; street poles need larger clamps (BOM line 6). This should be raised with FieldNode, not changed there.
- In the exploded view the microphone (callout 9) and processor (callout 10) are small at this scale and partly hidden by their callout circles. In the hero image the node is small against the 5 m pole, which is true to scale.
- Sources that could not be fetched were left out: the UNEP Frontiers 2022 city noise figures, the WHO 2018 guideline text itself (its road traffic values are cited through the EEA), India's CPCB noise standards and monitoring network, and the Infineon IM72D128 product page. The India, Sub-Saharan Africa and Latin America rows in the README therefore carry no cited figure.
- Microphone and processor currents are typical class values, not datasheet figures.
- The legacy `cad/src/model.py` placeholder is untouched (TRL 3 work).

### Recommended next step

Review this note and the media, then decide items 1 to 3. If approved, run `/advance-trl3` to check the noise floor, frequency response, power and wind load by calculation, define the wind-flagging method, and produce the parametric model and drawing sheet.
