# Review note: NoiseMap

## Session 2026-10-01: design for construction and build plan (kit 1.7.0)

Kit 1.7.0 installed (`.kit/`, `.claude/commands/`, root `CLAUDE.md`). Following Amish's approval of the build plan format on 2026-09-30 and his instruction "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations", the design was checked for constructability with build123d and made buildable. Every change is in `docs/decisions/0003-design-for-construction.md` (NSM-DDR-003, draft, made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review).

### Design changes made for construction

- FieldNode core: the old FieldNode massing model is replaced by the constructable FieldNode (FND-DWG-001 Rev P3, copied unchanged into `cad/src/fieldnode_core.py`), built to FND-BLD-001 without its small-pole V-blocks and bands.
- Street pole V-blocks: the milled, pocketed 110 x 60 x 40 mm blocks are replaced by 112 x 63 x 16 mm blocks sawn from bar with four drilled 14 mm holes, on the FieldNode plate's own V-block screw holes; the bands run under a rebate at each back corner and through the plate's own slots. No new holes in the FieldNode plate.
- Arm saddle: the milled 10 mm plate with one band (which had no path) is replaced by a channel bent from 2.5 mm sheet with a V in each flange and two bands through slots in its web.
- Arm fixings: a bought tube flange with an M5 cross bolt on the saddle; a socket printed on the head with an M4 cross bolt. The arm tube is now 383 mm; the microphone position is unchanged.
- Head: card guides for the processor; two bosses, two M2 screws and a 0.5 mm gasket for the microphone board (keeping the 3 mm, 0.5 mm front cavity); a printed bottom cap with an M16 cable gland; the drip skirt given a 45 degree cone so it prints without support.
- Windscreen bored 40 mm (was 41 mm, which nothing held); bird spike screwed into a boss on the skirt, 26 mm off the axis.
- Safety lanyard and the sensor cable route modelled.
- `cad/src/model.py` rewritten around components with 62 constructability checks (`python cad/src/model.py --check`), all passing. STEP and STL re-exported; NSM-DWG-001 Rev P2 to P3; concept media regenerated.

### Results

- Mass 3.45 kg against R10's 3.5 kg, margin 0.05 kg (unchanged). Arm stress factor 24 to 27; clamp twist factor 4.2 to 9.4; 96 N added to the pole.
- Cost: value-engineering target USD 100 for the NoiseMap parts; estimated cost of the constructable design USD 72.00 (USD 28.00 under the target); full node USD 211.00 with the USD 139.00 FieldNode core. `budget_usd` unchanged.
- Requirement status unchanged: 0 not met, 3 at risk (R3, R4, R5), 4 not verifiable at TRL 3, 4 met on paper, 4 met by design.

### Documents

- New: `docs/05-build-plan.md` (NSM-BLD-001 v0.1) with `docs/05-build-plan/` (overview, saddle blank, 8 joint close-ups, 12 step pictures, head wiring) and making sketches `cad/drawings/NSM-DWG-101` to `106` from `cad/src/build_plan_media.py`; `docs/06-design-decisions.md` (NSM-DEC-001 v0.1); NSM-DDR-003.
- Revised: NSM-CAL-001 v0.3 (mass, arm, clamp and cost re-run; FieldNode mass from FND-CAL-001 v0.3); NSM-PRC-001, NSM-REQ-001 and NSM-PRB-001 v0.5; `bom/bom.csv` and `bom/bom-notes.md`; `README.md` (links line, "Building the prototype", figures); `project.yaml` (`design_state: constructable`, evidence).

### Proposed, awaiting Amish

See the design decisions register: accept NSM-DDR-003; bird spike position (recommendation: the side spike as modelled, measured at TRL 4); the 0.05 kg mass margin (recommendation: accept, weigh at TRL 4); O1 co-design partner and street; the M12 pinout (FieldNode's open decision).

### Stale, to update on Amish's Mac

`media/render-hero.png`, `media/render-exploded.png`, `media/render-detail.png`, `media/card.png`, `media/social-preview.png` and `cad/src/product_model.py` still show the concept saddle, V-blocks, head and FieldNode bracket. The design changed visibly, so they need re-rendering with Blender.

### Recommended next step

Amish's review of NSM-DDR-003 and the open items in NSM-DEC-001. TRL 4 stays on hold; nothing here was built or bought.

## Session 2026-09-25: recommendations accepted

On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Every NoiseMap item with a recommendation is now **decided by Amish, 2026-09-25: go with recommendation**. The decisions are recorded in `docs/decisions/0002-recommendations-accepted.md` (NSM-DDR-002 v0.1), and NSM-DDR-001 is revised to v0.2.

### Decisions applied and what changed

- **D1 to D13** (NSM-DDR-001): status changed from "adopted for TRL 3, open for review" to decided. No further repo change; D1 had already kept `budget_usd` at $100 and redefined R13 to the NoiseMap parts.
- **O2, R10 mass, option (c)**: V-blocks pocketed from top and bottom (4 mm walls, 8 mm web) and the arm saddle pocketed 6 mm deep in `cad/src/model.py`; R10 relaxed from 3 kg to 3.5 kg. While doing this, a modeling error was found and fixed: the P1 model centered the V notch on the apex, which cut each V-block down to a flat 10 mm plate. With true 90° V-blocks, the solid node would be 3.96 kg; pocketed it is **3.45 kg** (v0.1 figure 3.32 kg). R10 goes from **not met** to **met on paper**, with a margin of only 0.05 kg. STEP and STL re-exported; NSM-DWG-001 Rev P1 to **P2**; BOM lines 7 and 14 describe the pockets (prices unchanged).
- **O3, wind flag, option (a)**: level-based flag from the Z-weighted band below 40 Hz; rain flagged on the server. No anemometer. R11 stays not verifiable at TRL 3; the field comparison that sets the threshold is TRL 4 work, on hold.
- **O4, airtime at slow data rates**: the core lengthens the interval automatically, 24 min at SF10, 48 min at SF11, 87 min at SF12, keeping 15 min at SF7 to SF9. Airtime goes from 47.4 s/day at SF10 (over the 30 s limit) to at most 30.0 s/day at every spreading factor. R12 goes from **at risk** to **met on paper**.
- Budget: `budget_usd` unchanged at $100 (NoiseMap parts $62.00; full node $188.00 with the $126.00 FieldNode core).
- Pitch and problem: no rewording was recommended, so `project.yaml` pitch and problem are unchanged; `trl_evidence` now lists NSM-DDR-002.
- Documents: NSM-PRB-001, NSM-PRC-001 and NSM-REQ-001 v0.3 to v0.4; NSM-CAL-001 v0.1 to v0.2 (script and `results.csv` re-run); NSM-DDR-001 v0.1 to v0.2; NSM-DDR-002 v0.1 new. PDFs, drawing and concept media regenerated (footers now designmolecule.com).
- README: "What sparked the idea" rewritten around the Stratumseind living lab in Eindhoven, whose sound sensors also analyzed voices for aggression ([The Next Web, 2018](https://thenextweb.com/the-next-police/2018/06/08/1128392/); [Galič, 2019](https://www.researchgate.net/publication/333673572_Surveillance_privacy_and_public_space_in_the_Stratumseind_Living_Lab_the_smart_city_debate_beyond_data)); the earlier text about how the idea was chosen is removed. TRL 3 summary and key components updated.

### Requirement status (NSM-CAL-001 v0.2, not met first)

0 not met, 3 at risk, 4 not verifiable at TRL 3, 4 met on paper, 4 met by design (before: 1 not met, 4 at risk, 4 not verifiable, 2 met on paper, 4 met by design).

| ID | Status | Key number |
| --- | --- | --- |
| R3 Accuracy | At risk | Expanded uncertainty 2.9 dB on assumed terms; facade bias up to 2.4 dB |
| R4 Measuring range | At risk | ICS-43434 34.9 to 113 dBA; IM72D128 27.9 to 113 dBA |
| R5 Frequency weighting | At risk | Membrane, windscreen and head diffraction unknown |
| R8, R9, R11, R14 | Not verifiable at TRL 3 | Ingress, calibration time, wind threshold, service life |
| R7, R10, R12, R13 | Met on paper | 53 days without sun; 3.45 kg against 3.5 kg; at most 30.0 s/day airtime; NoiseMap parts $62.00 |
| R1, R2, R6, R15 | Met by design | R1 rests on firmware (D2) |

### Still awaiting Amish

1. **O1, first co-design partner and street.** No recommendation; stays "Proposed, awaiting Amish".

### Cross-repo actions (not made here)

- FieldNode: a street pole mounting variant for 60 to 140 mm poles (NoiseMap carries its own adapter, BOM line 14); would also serve other pole-mounted siblings.
- FieldNode: align the automatic interval rule (24, 48, 87 min at SF10 to SF12) with FieldNode's interval item 8, which lives in the FieldNode core firmware.
- FieldNode: agree the M12 port pinout (FieldNode O2); NoiseMap needs 3.3 V, ground and one UART pair.

### Notes

- The R10 margin is 0.05 kg. Shorter (30 mm) V-blocks, or leaving FieldNode's unused small-pole V-blocks off street-pole nodes, would add margin; suggestions only.
- In the exploded view the BOM legend runs close to the callouts on the left, as before.

### TRL 4

TRL 4 remains on hold by Amish's instruction. `trl: 3` and `trl_target: 3` are unchanged. No build, test, purchasing, PCB or firmware work was done; the wind threshold field comparison and the class 1 side-by-side are on hold.

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

Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction; now decided by Amish, 2026-09-25: go with recommendation (NSM-DDR-002): D1 budget covers the NoiseMap parts only, FieldNode core costed in FieldNode (`budget_usd` unchanged at 100; R13 redefined); D2 privacy stated as resting on open firmware, never "by physics"; D3 dual-footprint microphone adapter; D4 processing in the head; D5 15-minute records with 1-minute LAeq and the listed statistics; D6 wind flagging studied (NSM-CAL-001 section G); D7 shared calibrator and one side-by-side per deployment; D8 public notice on each pole; D9 to D12 precis choices (levels only, standard FieldNode core, microphone position, A and C weighting); D13 printed ASA head. No pitch or problem rewording was recommended, so neither changed.

### Still awaiting Amish (as of this session; O2 to O4 since decided, see the session above)

1. **O1, first co-design partner and street.** No preference stated.
2. **O2, R10 mass (new).** Options: (a) pocket the V-blocks and saddle (3.10 kg, still over); (b) relax R10 to 3.5 kg; (c) both. Recommendation: (c). Decided by Amish, 2026-09-25: go with recommendation; applied under NSM-DDR-002.
3. **O3, wind flag method (new).** Options: (a) level-based flag, no cost; (b) cup anemometer on FieldNode's second port (about $25, 0.15 kg). Rain flagged on the server in both. Recommendation: (a), with a field comparison to set the threshold. Decided by Amish, 2026-09-25: go with recommendation; applied under NSM-DDR-002 (field comparison on hold with TRL 4).
4. **O4, airtime at SF10 and slower (new).** Lengthen the interval automatically on The Things Network (24 min at SF10, 87 min at SF12), following FieldNode's item 8. Decided by Amish, 2026-09-25: go with recommendation; applied under NSM-DDR-002.

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

### Proposed, awaiting Amish (items 1 to 8 since decided by Amish, 2026-09-25: go with recommendation; item 9 still open)

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

## Session 2026-09-26: sources strengthened

| README item | Old source | New source |
| --- | --- | --- |
| "What sparked the idea" (Stratumseind living lab) | The Next Web, 2018, standing alone for the lab's description | [The Hague Security Delta living lab page](https://securitydelta.nl/services/innovation/living-labs/stratumseind) for the lab's partners and acoustic aggression detection; The Next Web kept alongside only for the DITSS director's quote; Galič now identified as *Ars Aequi*, 2019 |
| India row | None | [Press Information Bureau, Government of India, 2011](https://www.pib.gov.in/newsite/erelcontent.aspx?relid=71212&reg=3&lang=2): national real-time noise network launched with 35 stations in seven metros |
| Sub-Saharan Africa row | None (Lagos and Nairobi, uncited) | Rewritten as Sub-Saharan Africa (Nigeria), citing the [UNEP Frontiers 2022 press release](https://www.unep.org/news-and-stories/press-release/deadly-wildfires-noise-pollution-and-disruptive-timing-life-cycles), which lists Ibadan among cities where acceptable noise levels are surpassed |
| Latin America row | None | Replaced with Southeast Asia (Thailand, Vietnam): Bangkok and Ho Chi Minh City, same UNEP source; no verifiable Latin American source was found this session |
| New York 311 figure (Burning platform) | arXiv abstract page (figure not on it) | [Full paper PDF](https://arxiv.org/pdf/1805.00889), *Communications of the ACM*, 2018, which contains the figure |

All other links in the four sourced README sections (EEA noise page, EEA briefing citing WHO 2018, Directive 2002/49/EC, US EPA 1974, Bruitparif) were fetched and confirmed on 2026-09-26. `docs/01-problem.md` did not cite The Next Web, so no controlled document changed. The INSPIRATIONS.md line for NoiseMap was updated to list the stronger source; the event is unchanged.

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose this repo for the first batch of product renders on 2026-09-26.

### What was done

`cad/src/product_model.py` adds a product appearance model for photoreal renders. It exposes `product_parts()` (45 parts: 36 shell, 8 internal, 1 context), `TITLE` and `RENDER_VIEWS` (hero with a short pole section, exploded, and a detail view without the pole). It imports `PARAMS`, `derived()` and `build_parts()` from `cad/src/model.py`; the pole adapter, tilt bracket, arm and head reuse the model.py solids, and every main dimension, height and interface is unchanged. It adds:

- The FieldNode enclosure split into body and lid at a parting line, with filleted edges, a gasket line, four lid screws, side ribs, an ePTFE vent, M12 port nuts, the knurled sensor cable plug and a dust cap on the spare port.
- A lid label that reads "NoiseMap, records sound levels only, no audio is stored or sent", with a teal "dB ONLY" band (kit accent #0F766E).
- A 6 W panel with an aluminium frame, dark cells, a cell grid and a junction box.
- Rounded back plate corners, V-block bolts, band clamp bolts, the arm band clamp housing and the collar screw.
- On the microphone head: grip grooves, a teal accent ring, a cable gland, the foam windscreen (fabric material) and a separate bird spike.
- Internals: the power and radio board with the LoRaWAN module and shield can, the cell with terminals and its cradle, the microphone adapter board and the level processor.
- The sensor cable along the model.py route with rounded bends, and a 1.13 m section of 114.3 mm street pole as context.

The README hero line now points to `media/render-hero.png`, with an "Exploded render" link; the orchestrator produces the render files.

### Differences from model.py (Proposed, awaiting Amish)

- **Lit status light on the lid.** Neither model.py nor the BOM shows a status light on the FieldNode enclosure. The render shows a small green light on the lid. Recommendation: keep it as an appearance cue and raise it with FieldNode as an optional light pipe from the board, costed there. Alternatively, remove it from the appearance model.
- **Lid label text.** The public notice (D8) is specified for the pole, not the enclosure. The render puts a "records sound levels only" label on the lid. Recommendation: keep the lid label and the pole notice both, with the wording checked by Amish before any public use.
- **Head grip grooves and accent ring.** Model.py shows a plain ASA tube. The grooves (0.6 mm deep) and the ring are cosmetic and leave the 3 mm wall, acoustic port and skirt unchanged. Recommendation: keep them for the render; revisit at TRL 4 if the print process makes them costly.
- **Cable plug and dust cap.** Model.py shows the M12 ports as plain cylinders; the render adds a plug on the sensor port and a cap on the spare port, and the cable starts at the plug. Recommendation: accept; this is appearance only.

### Status

This is an appearance model only: no tolerances, no fabrication detail, no PCB layout. `trl` stays 3, and TRL 4 remains on hold.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.

## Session 2026-10-02: open decisions decided

On 2026-10-02 Amish approved every recommendation written for the open decisions: "i approve your recommendations for all 555 open decisions." Nothing was built or tested; TRL 4 remains on hold.

### Decisions recorded

5 decisions moved from "Open decisions" to "Decisions made" in the design decisions register, dated 2026-10-02. Design for construction (NSM-DDR-003) accepted with its items A1 and A2; a city noise team or university acoustics group with a Class 1 reference meter named as the first partner to approach; FieldNode's candidate M12 pinout adopted for NoiseMap's port.

### Documents changed

- `docs/01-problem.md` (NSM-PRB-001 v0.6)
- `docs/02-concept.md` (NSM-PRC-001 v0.6)
- `docs/05-build-plan.md` (NSM-BLD-001 v0.2)
- `docs/06-design-decisions.md` (NSM-DEC-001 v0.2)
- `docs/decisions/0001-trl2-review-decisions.md` (NSM-DDR-001 v0.3)
- `docs/decisions/0002-recommendations-accepted.md` (NSM-DDR-002 v0.2)
- `docs/decisions/0003-design-for-construction.md` (NSM-DDR-003 v0.2)
- `README.md` (not a controlled document)
- `docs/pdf/`: every controlled document re-rendered.

### Follow-up actions to carry approved decisions into the design

The model, drawings, build plan pictures, BOM quantities and prices, and calculations were not changed in this session. These actions carry the approved decisions into them:

1. Decision 5 (docs): Cross-repo: ask FieldNode to adopt its candidate M12 pinout for both ports (pin 1 switched rail, pin 2 data A, pin 3 ground, pin 4 data B, pin 5 analog) and to label each port with its rail voltage; NoiseMap's port is set to 3.3 V.
2. Decision 5 (drawings): Show the M12 pin assignment (pin 1 at 3.3 V, pin 3 ground, pins 2 and 4 UART) on the wiring diagram and in the build plan's cable step, and add a 3.3 V port label.
3. Decision 5 (bom): BOM line 12: name the pin assignment in the sensor cable description at the next revision.
4. Decision 2 (docs): TRL 4 test plan (when TRL 4 starts): measure the response with and without the side spike.
5. Decision 3 (docs): TRL 4 test plan: weigh the prototype against R10 (3.5 kg).
6. Decision 1 (pictures): At the next render session on Amish's Mac, redraw the photoreal renders, card and social preview to the constructable design (arm saddle, V-blocks, head and FieldNode bracket).

### Points found in the review

Raised when the recommendations were written (2026-10-01) and not yet acted on:

- Cross-repo: each FieldNode port's rail voltage is chosen at build, and NoiseMap needs 3.3 V where SlopeWatch needs 12 V on the same pin; ports should be labelled with their rail voltage so a 3.3 V sensor is never plugged into a 12 V port.
- Renders still show the concept arm saddle, V-blocks, head and FieldNode bracket.

## Session 2026-10-02: approved follow-ups carried out

Amish, 2026-10-02, approved that every follow-up action from the open-decision sign-off be carried out. trl stays 3; no build or test work was done. Documents changed, with new versions: NSM-BLD-001 v0.3. Also changed: `bom/bom.csv` (lines 12 and 13) and `bom/bom-notes.md`; `cad/src/build_plan_media.py` (wiring picture), `cad/src/sheets.py` (NSM-DWG-001 Rev P4), `cad/src/concept_media.py`, `cad/src/product_model.py`.

### Approved follow-ups carried out

1. **Decision 5, ask FieldNode to adopt its pinout and label each port with its rail voltage: not done here, listed under Cross-repo actions.** NoiseMap's side is done: it uses pin 1 at 3.3 V, pin 3 ground and pins 2 and 4 for the UART pair, and its port is labelled 3.3 V.
2. **Decision 5, pin assignment on the wiring diagram and in the cable step, and a 3.3 V port label: done.** Figure 13 (`docs/05-build-plan/wiring.png`) shows the pin numbers and a "PORT A: 3.3 V" label; build plan 3.8 step 3, step 12 and safety stop S1 name the pins and the label; the GA sheet notes the pins; the appearance model carries the label beside port A.
3. **Decision 5, BOM line 12 names the pin assignment: done.** The label is in line 13 (about USD 0.50, inside the line's price). No price changed.
4. **Decision 2, TRL 4 test plan: measure the response with and without the side spike: not done, TRL 4 work (no test plans at the TRL 3 cap).**
5. **Decision 3, TRL 4 test plan: weigh the prototype against R10: not done, TRL 4 work.**
6. **Decision 1, appearance model for the constructable design: done.** `cad/src/product_model.py` now uses the built back plate (window, band slots), the side bird spike in its skirt boss with the matching windscreen, the built head gland, and adds the enclosure lugs and screws, cable glands, bracket and panel bolts; the concept hex bolts and the concept saddle fixings are gone. Render scenes exported (hero, exploded, detail views as listed in the file) to `/home/claude/renders/noisemap`. The photoreal renders, card and social preview are made on Amish's Mac next.

### Key results

- Requirement status changes: none (3 at risk, 4 not verifiable, 4 met on paper, 4 met by design, as before). Calculations re-run: output unchanged.
- Value-engineering target: USD 100. Estimated cost of the constructable design: USD 72 (USD 28 under the target). Mass unchanged at about 3.45 kg (R10 3.5 kg).
- Model: 62 constructability checks pass; the model did not change.
- Pictures regenerated: wiring diagram (Figure 13), NSM-DWG-001 (Rev P4), the concept media (blueprint, hero, cutaway, exploded, flow, viewer).

### Cross-repo actions

- **FieldNode (`fieldnode`):** adopt its candidate M12 pinout for both sensor ports (pin 1 switched rail, pin 2 data A, pin 3 ground, pin 4 data B, pin 5 analog), and label each port with its rail voltage, so that a 3.3 V sensor such as NoiseMap is never plugged into a 12 V port such as SlopeWatch's. Publish the pinout in the FieldNode documents.

### Proposed, awaiting Amish

- The approved decision fixes the pins (1, 3, and 2 and 4 as the UART pair) but not which of pins 2 and 4 carries the head's transmit. The wiring diagram and build plan put the head's transmit (levels out) on pin 2 (data A) and its receive on pin 4 (data B). Recommendation: accept, and confirm with FieldNode's firmware at TRL 4.

## 2026-10-02: photoreal renders redone on the constructable design

Rendered with Blender Cycles on Amish's Mac from the updated appearance model; captioned with `.kit/photo_caption.py`; `media/card.png` and `media/social-preview.png` regenerated with `.kit/cards.py`. Views: hero, exploded, detail. image_qc passes. Appearance deviations are those logged above as proposed, awaiting Amish.
