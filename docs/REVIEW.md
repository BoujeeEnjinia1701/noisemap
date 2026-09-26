# Review note: NoiseMap

## Session 2026-09-25: TRL 3

On 2026-09-25 Amish asked for this batch of repos to go through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed this repo's TRL 2 items one by one, so every item that carried a recommendation is adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. This session ran `/advance-trl3` on that basis and stopped at TRL 3.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (NSM-DDR-001 v0.1, status proposed): D1 to D13 adopted as recommended for TRL 3, open for Amish's review; O1 to O4 left open.
- `docs/04-calcs/01-sizing.md` (NSM-CAL-001 v0.1), `docs/04-calcs/sizing.py` and `docs/04-calcs/results.csv`: measuring range, frequency response and port resonance, reflections and an uncertainty budget, processor load and power, energy, record format, airtime, link capacity for privacy, wind and rain flagging, arm stress, vibration and clamp margins, mass and cost, with a status for all 15 requirements. The script imports the model, reads the BOM and `project.yaml`, and prints every number the note quotes.
- `cad/src/model.py`: parametric build123d model (FieldNode core envelope per FND-DWG-001, street pole adapter for 60 to 140 mm poles, arm with saddle and band, head with acoustic port and front cavity, microphone board, processor, windscreen, cable). Exports `cad/step/` and `cad/stl/` for `noisemap-assembly`, `noisemap-head` and `noisemap-mount`, and runs a clash check (none beyond attachment contacts).
- `cad/src/sheets.py` and `cad/drawings/NSM-DWG-001.svg`, `.pdf`, `.png`: general arrangement at Rev P1, 1:10, marked "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". NSM-DWG-001 was free because the concept blueprint is NSM-DWG-010.
- `bom/bom.csv` (14 lines, all priced with a supplier or supplier type) and `bom/bom-notes.md`: the FieldNode core now uses the FieldNode BOM figures ($126.00); new line 14, street pole adapter. NoiseMap parts $62.00 against the $100 budget; full node $188.00.
- `cad/src/concept_media.py` now builds from `model.py`; all media re-rendered (hero, blueprint, cutaway, exploded, flow, `model.glb`, `viewer.html`) and checked by eye; temporary `media/_views*` folders deleted.
- NSM-PRB-001, NSM-PRC-001 and NSM-REQ-001 revised to v0.3; `README.md` (TRL badge, budget scope, TRL 3 numbers, privacy wording, links) and `project.yaml` (`trl: 3`, `trl_target: 3`, evidence list) updated. PDFs rebuilt in `docs/pdf/`.

### Requirement status (NSM-CAL-001, Table 4)

1 not met, 4 at risk, 4 not verifiable at TRL 3, 2 met on paper, 4 met by design.

| ID | Status | Key number |
| --- | --- | --- |
| R10 Installation and mass | **Not met** | 3.32 kg against 3 kg (3.10 kg with pocketed V-blocks and saddle); wind margins met on paper |
| R3 Accuracy | At risk | Expanded uncertainty 2.9 dB on assumed terms; facade bias up to 2.4 dB before a site correction |
| R4 Measuring range | At risk | ICS-43434 34.9 to 113 dBA (no margin at 35); IM72D128 27.9 to 113 dBA |
| R5 Frequency weighting | At risk | -2.8 dB at 63 Hz equalized to ±0.8 dB; port resonance 36.2 kHz; membrane and windscreen unknown |
| R12 Radio use | At risk | 23.7 s/day at SF9; 47.4 s/day at SF10 (over 30 s) |
| R8, R9, R11, R14 | Not verifiable at TRL 3 | Ingress, calibration time, wind threshold, service life |
| R7, R13 | Met on paper | 5.81 Wh/day for 0.29 Wh/day, 53 days without sun; NoiseMap parts $62.00 |
| R1, R2, R6, R15 | Met by design | R1 rests on firmware (D2) |

Key numbers: design load 12.2 mW (12 % of FieldNode's 100 mW allowance; 22.6 mW upper bound); processor 2.15 mA at 13.2 % load; 22-byte record; arm stress factor 24; clamp twist factor 4.2; 97 N added to the pole at 35 m/s.

Corrections to TRL 2 numbers: load 21 to 12.2 mW; autonomy 30 to 53 days; upper range 115 to 113 dBA (crest factor); mass 2.3 to 3.32 kg (FieldNode is now 2.41 kg, and the adapter was missing); cost $171 to $188 for a full node (FieldNode core $119 to $126, adapter added); the cable is too slow for raw audio but not for a speech codec.

### Decisions recorded (NSM-DDR-001)

Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review: D1 budget covers the NoiseMap parts only, FieldNode core costed in FieldNode (`budget_usd` unchanged at 100; R13 redefined); D2 privacy stated as resting on open firmware, never "by physics"; D3 dual-footprint microphone adapter; D4 processing in the head; D5 15-minute records with 1-minute LAeq and the listed statistics; D6 wind flagging studied (NSM-CAL-001 section G); D7 shared calibrator and one side-by-side per deployment; D8 public notice on each pole; D9 to D12 precis choices (levels only, standard FieldNode core, microphone position, A and C weighting); D13 printed ASA head. No pitch or problem rewording was recommended, so neither changed.

### Still awaiting Amish

1. **O1, first co-design partner and street.** No preference stated.
2. **O2, R10 mass (new).** Options: (a) pocket the V-blocks and saddle (3.10 kg, still over); (b) relax R10 to 3.5 kg; (c) both. Recommendation: (c). Not applied.
3. **O3, wind flag method (new).** Options: (a) level-based flag, no cost; (b) cup anemometer on FieldNode's second port (about $25, 0.15 kg). Rain flagged on the server in both. Recommendation: (a), with a field comparison to set the threshold. Not applied.
4. **O4, airtime at SF10 and slower (new).** Lengthen the interval automatically on The Things Network (24 min at SF10, 87 min at SF12), following FieldNode's item 8. Not applied.

### Cross-repo consistency

- FieldNode (FND-CAL-001, FND-DDR-001): NoiseMap now uses FieldNode's TRL 3 figures: core $126.00, mass 2.41 kg, 100 mW design allowance, 4.0 mWh/day core, 7.75 Wh/day worst-month harvest, two M12 5-pin ports with one switched rail each, 15 min default. No conflict on power or radio. FieldNode's review listed NoiseMap at $119; that figure is now $126.00 here, which removes the discrepancy it noted.
- Conflict to raise with FieldNode, not edited there: FieldNode's mount seats 40 to 71 mm poles, and street poles need 60 to 140 mm, so NoiseMap adds its own adapter (line 14). A street pole kit variant in FieldNode would serve AirStreet, CurbCount and other pole-mounted siblings too.
- FieldNode's sun shield (its review item 4) matters little to NoiseMap: at 0.29 Wh/day the node stays in credit on FieldNode's hot clear day (0.8 Wh clean, 0.3 Wh dusty) without it.
- The pinout of the M12 port is still FieldNode O2; NoiseMap needs 3.3 V, ground and one UART pair.
- CityTwin assumes 96 NoiseMap uplinks a day; unchanged at 15 min. TwinKit's airtime figures (sized for 20-byte payloads) agree with Table 3 of NSM-CAL-001 at SF9 (246.8 ms); the 35-byte NoiseMap frame is slightly longer at SF7 and SF10.
- LampNode proposes hosted 12 V power on lighting poles as an option for NoiseMap; NoiseMap stays on FieldNode solar, which LampNode's recommendation (a) allows.

### Safety concerns

- Work at height beside traffic when installing; pole owner's permission, trained crews, traffic management.
- Clamp preload (assumed 1,000 N) carries every wind and slip margin; installers need a torque figure. The node adds about 97 N of wind load at 3.5 to 4 m that the pole owner should check.
- Falling parts from 4 m: safety lanyard on the arm; the arm and head may vibrate near 70 Hz in 9 to 14 m/s winds.
- LiFePO4 cell (about 19 Wh): fusing and the FieldNode 0 to 45 °C charge lockout.
- Hearing: bench checks near the upper range need hearing protection.
- Privacy: the links could carry a speech codec, so the head firmware, its read-out protection and build hash are safety-critical for public trust; any firmware change needs a fresh privacy review.
- Misuse of data: readings are indicative and must not be presented as certified measurements.

### Gaps and notes

- Citations: the ICS-43434 figures were checked on the TDK page (SNR 65, sensitivity -26 dBFS, AOP 120 dB SPL, 60 Hz to 20 kHz, end of life); the IM72D128's 72 dB(A) SNR, PDM interface and IP57 rating were checked in the DNMS README and are now cited; Codec 2 bit rates were checked on rowetel.com. Still unchecked, flag kept: the Infineon IM72D128 product page (returned 404), the IEC 61672-1 class 2 tolerance table (values used are approximate), UNEP Frontiers 2022 city figures (the page carries no figures; the chapter PDF was not read), India's CPCB standards (fetch disallowed) and the WHO 2018 guideline text. WebSearch was not used. The README region rows for India, Sub-Saharan Africa and Latin America still carry no cited figure.
- Assumed values only tests can settle: microphone and processor currents, the IM72D128 overload point and roll-off, windscreen insertion loss, the uncertainty terms, band preload, the wind threshold.
- Media: in the exploded view the microphone (callout 9) is a few millimeters across and hidden under its callout; in the hero the node is small against the 5 m pole, which is true to scale. The model is shifted down by the mean of the enclosure and microphone heights so the kit's cutaway (a Y section at the parts' mean Y) passes through both the enclosure and the head; the adapter, panel, bracket and cable are left out of the cutaway.
- The drawing is at 1:10 on ANSI B and leaves space unused; the head detail is small at that scale.
- Existing material beyond TRL 3: `build-log/README.md` (scaffold only) is present, untouched and not extended. `electronics/` and `firmware/` are empty. No test, build or firmware material was created.

### Recommended next step

TRL 4 is on hold by Amish's instruction; this repo stops at TRL 3. The next step is Amish's review of NSM-DDR-001 (D1 to D13) and a choice on O1 to O4, plus a note to FieldNode about a street pole mounting variant. For the record only, TRL 4 would need: a bench build of the head with both microphones; a lab test report (TST, `environment: lab`) covering noise floor, frequency response with membrane and windscreen, linearity against a calibrator and reference meter, processor and microphone current, and cable capture showing levels only; weighing of the arm and adapter; and build log entries. None of this has been started.

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
