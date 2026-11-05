---
doc_id: NSM-RSK-001
title: NoiseMap risk register and hazard analysis
project: NoiseMap
doc_type: Risk register and hazard analysis
version: "0.1"
status: Draft
date: '2026-11-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-11-02'
  author: Amish Chadha
  change: First issue (kit 1.8 pipeline), with the first-pass design FMEA at stage P3
---

# NoiseMap risk register and hazard analysis

Top risks: measurement quality that paper cannot settle (R-2) and a privacy promise that rests on firmware, not physics (R-5); the top hazards are work at height beside traffic (H1) and a falling arm or head (H2). The FMEA's highest numbers are the hydrophobic membrane (F6, RPN 120), the level firmware (F10, 105), the V-block bands (F1, 96), and the lanyard and privacy firmware (F4 and F11, 90 each). Method: STANDARDS section 23. Likelihood, impact, severity and occurrence are scored 1 (low) to 5 (high); detection 1 (certain to be caught) to 5 (not detectable at TRL 3). All scores are the author's proposals, "Proposed, awaiting Amish".

## Project risk register

Table 1. Project risks.

| # | Risk | Cause | Effect | Likelihood | Impact | Owner (role) | Response |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R-1 | Co-design partner not yet agreed (NSM-PRB-001 open items) | No partner has confirmed the user needs | UR priorities and targets stay proposals | 3 | 4 | Amish | Approach a city noise team or university acoustics group (decided 2026-10-02); revise URS and PRS from their findings |
| R-2 | Measurement quality (PR-003 to PR-005) misses its targets | Membrane, windscreen and head diffraction unknown; facade bias | Accuracy claim cannot be made | 4 | 4 | Design lead | Reference meter at TRL 4 (on hold); keep every claim 'indicative' |
| R-3 | Mass margin of 0.05 kg is used up | A heavier windscreen or an anemometer is added | PR-010 not met | 3 | 3 | Design lead | Mass check on any added part (NSM-DDR-003 A2) |
| R-4 | ICS-43434 supply (end of life) | Maker listing | Microphone has to change | 4 | 2 | Design lead | Dual-footprint adapter board takes the IM72D128 (D3) |
| R-5 | Privacy claim is doubted | Firmware could in principle send audio; the cable could carry a speech codec | Loss of trust, no deployment | 3 | 4 | Amish | Open firmware, read-out protection, build hash; never claim privacy by physics (D2) |
| R-6 | Regulatory unknowns (radio, GDPR, battery) | Items marked to assess in NSM-REG-001 | Delay before any deployment | 3 | 3 | Regulatory consultant | Consult before any pilot; no product claim |
| R-7 | Options A and B within 10 %: choice delayed | Score gap 4.7 % | Wait for Amish | 3 | 2 | Amish | Decision request in NSM-PLN-001 |
| R-8 | TRL cap | Portfolio capped at TRL 3 | No testing to settle the at-risk items | 5 | 2 | Amish | Plan only; P4 on hold |
| R-9 | LoRaWAN airtime margin at SF12 | At SF12 the node uses 29.97 s of the 30 s a day it may transmit, leaving no room for time requests, joins or retries | Records lost or delayed at the cell edge | 3 | 3 | Design lead | Interval rule (NSM-DDR-002 O4); SF7 to SF9 expected in town; PR-002 and PR-012 stated for SF7 to SF9 only (NSM-DEC-001 decision 3) |

## Preliminary hazard analysis

Table 2. Hazards. Option A unless stated; the mains hazard H11 belongs to option C only.

| # | Hazard | Cause | Harm | Severity | Likelihood | Control | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | Work at height beside traffic | Fitting or servicing a node 4 m up a street pole | Fall; person struck by vehicle | 5 | 3 | Trained crew, owner's permission, fall protection, traffic management (NSM-PRC-001) | Medium |
| H2 | Falling part | Clamp slips, tube pulls out, wire rope fails | Head injury to a passer-by from 4 m | 5 | 2 | Two band clamps, cross bolts with nyloc nuts, lanyard (PR-017), check after the first storm | Low to medium |
| H3 | Wind load on the pole | 35 m/s gust on 0.1 m2 of panel, box and windscreen | Pole overload (about 96 N at 3.5 to 4 m) | 4 | 2 | Pole owner confirms the pole can take it; no more area without a check | Low |
| H4 | Lithium cell fault | Damaged, swollen or cold-charged cell | Heat, fire | 4 | 2 | Fuse, NTC, cold-charge lockout, no swollen cell; FieldNode core item | Low |
| H5 | Overhead lines and pole wiring | Reaching or opening a pole hatch | Electric shock | 5 | 2 | Keep clear of overhead lines; never open a pole's electrical hatch; no electrical connection to the pole | Low |
| H6 | Hearing damage | Calibrator at 94 dB held near the ear | Temporary threshold shift | 2 | 2 | Hearing protection if the calibrator sounds for more than a short check; 2 minutes against 60 allowed (STM S19) | Low |
| H7 | Sharp edges | Sawn aluminium bar, cut sheet, wire rope ends | Cuts | 2 | 3 | File and break edges (modelled 0.5 mm); gloves during build | Low |
| H8 | Privacy harm | Audio stored or sent, or believed to be | Loss of trust, complaints, legal exposure | 4 | 2 | Levels only by design; open firmware with a build hash; notice plate (PR-016); data protection review (NSM-REG-001 G6) | Medium until reviewed |
| H9 | Readings misused as legal evidence | Indicative data presented as certified | Wrong enforcement decision | 3 | 3 | Marked as indicative in every document; certified co-located meter needed for enforcement; out of scope | Low |
| H10 | Birds and the bird spike | Spike on the windscreen | Soft wording: harm to a bird | 2 | 2 | Blunt-tipped 3 mm rod, placed off the microphone axis; effect not claimed | Low |
| H11 | Option C only: mains voltage in the puck | Plugging into a live luminaire receptacle | Electric shock | 5 | 3 | Qualified electrician; isolated converter; not part of option A | Medium (not carried forward in A) |

> **Safety:** installing on a street pole is work at height next to traffic, and the node carries a lithium cell and a falling-part risk. See the safety section of NSM-PRC-001.

## Design FMEA (first pass, P3)

Table 3. Failure modes of option A. RPN = severity x occurrence x detection. Scores are first-pass paper estimates; none is measured.

| # | Item | Function | Failure mode | Effect | Cause | S | O | D | RPN | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | V-blocks and bands | Hold the core to the pole | Band slips or breaks | Core rotates or falls | Preload loss, corrosion, vibration | 8 | 3 | 4 | 96 | Torque to a stated value; check after the first storm (NSM-PRC-001 safety note); keep preload 1,000 N (NSM-CAL-001 H6) |
| F2 | Arm saddle and bands | Hold the arm to the pole | Saddle fatigue crack or band slip | Arm and head fall 4 m | Wind cycling, sheet bend cracks | 9 | 2 | 4 | 72 | Lanyard (PR-017); 2.5 mm 5052-H32 sheet bent across the grain's safe radius (to confirm with the shop) |
| F3 | Arm tube and cross bolts | Carry the head | Tube pulls out of flange or socket | Head hangs on lanyard | Loose cross bolt | 8 | 2 | 3 | 48 | Nyloc nuts and threadlocker (BLD Step 5 and 8); lanyard |
| F4 | Safety lanyard | Retain the arm | Wire rope or ferrule fails | Arm falls | Wrong ferrule or nick in the wire | 9 | 2 | 5 | 90 | Four ferrules and two thimbles by the plan; inspect at each foam change |
| F5 | Head housing | Keep the electronics dry and fixed | UV cracking or warping of the printed ASA | Water in the head | UV, heat cycling, print layer weakness | 6 | 3 | 4 | 72 | Print orientation and 3 mm wall (NSM-DDR-003); inspect yearly |
| F6 | Hydrophobic membrane | Keep water out of the port while passing sound | Clogs or tears | Water at the microphone; level error | Dirt, bird contact, age | 6 | 4 | 5 | 120 | Replace with the foam; port protected by the windscreen |
| F7 | Foam windscreen | Reduce wind noise | Degrades or soaks | Wind noise, level bias | UV, rain | 4 | 5 | 3 | 60 | Yearly change (PR-014) |
| F8 | Cable and gland | Carry levels and 3.3 V | Chafing or gland leak | Loss of data; water entry | Rubbing on the arm, wrong cable diameter | 6 | 3 | 4 | 72 | Cable ties, gland sized to 4 to 8 mm cable; route in BLD Step 12 |
| F9 | LiFePO4 cell and charger | Store solar energy | Charged below 0 degrees C | Plating, capacity loss, in rare cases a safety event | Charger lockout fails | 7 | 2 | 4 | 56 | FieldNode cold-charge lockout and fuse; do not fit a swollen cell |
| F10 | Level processor firmware | Compute A and C levels | Wrong gain or filter | Biased levels reported as true | Coefficient or scaling error | 7 | 3 | 5 | 105 | Open firmware; field check with a 94 dB calibrator at install (PR-009); site correction |
| F11 | Firmware privacy | Send levels only | A code path sends samples | Loss of trust, data protection exposure | Added debug feature | 9 | 2 | 5 | 90 | Read-out protection, published build hash, review of every release (PR-001) |
| F12 | MEMS microphone | Convert sound to a signal | Clips above its overload point (119 dB SPL for the IM72D128, 113 for the ICS-43434) or sits at its noise floor | Wrong peak or night level | Overload; self-noise at 35 dBA | 5 | 4 | 3 | 60 | Use the IM72D128 where quiet levels matter (PR-004); flag clipped seconds |
| F13 | Solar panel | Charge the cell | Soiling or shading | Less harvest | Dust, bird droppings | 3 | 4 | 3 | 36 | Panel doubles as a hood; 20 times margin on energy (NSM-CAL-001 E1) |
| F14 | LoRaWAN link | Send the record | No gateway or join fails | Records stored in flash, then late | Poor coverage, antenna | 3 | 4 | 2 | 24 | Flash store and forward; gateway survey before install |
| F15 | Clock | Time-stamp records | Drift over weeks | Records misaligned with events | Crystal drift | 3 | 3 | 3 | 27 | LoRaWAN network time resync (PR-006) |
