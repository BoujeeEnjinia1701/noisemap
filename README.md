# NoiseMap

![TRL 3](https://img.shields.io/badge/TRL-3%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827) [![DOI](https://zenodo.org/badge/1388477501.svg)](https://zenodo.org/badge/latestdoi/1388477501) [![REUSE compliant](https://github.com/BoujeeEnjinia1701/noisemap/actions/workflows/reuse.yml/badge.svg)](https://github.com/BoujeeEnjinia1701/noisemap/actions/workflows/reuse.yml) [![Archived in Software Heritage](https://archive.softwareheritage.org/badge/origin/https://github.com/BoujeeEnjinia1701/noisemap/)](https://archive.softwareheritage.org/browse/origin/?origin_url=https://github.com/BoujeeEnjinia1701/noisemap)

**Area:** Smart Cities · **TRL:** 3 of 9 (proof of concept on paper) · **Value-engineering target:** $100 USD for the NoiseMap parts, estimated $72 (FieldNode core costed separately) · **Difficulty:** 2 of 5

A sound level meter node that records decibel levels only, never audio, to map traffic and nightlife noise.

![NoiseMap: street pole sound level meter that records decibels only, never audio, product render](media/render-hero.png)

[Exploded render](media/render-exploded.png) · [Studio render](media/render-node.png) · [Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [Exploded view](media/exploded.png) · [General arrangement NSM-DWG-001 (PDF)](cad/drawings/NSM-DWG-001.pdf) · [STEM check](docs/01b-stem-check.md) · [Concept options](docs/02a-concept-options.md) · [Requirements](docs/03-requirements.md) · [Traceability](docs/03b-traceability.md) · [Calculations NSM-CAL-001](docs/04-calcs/01-sizing.md) · [Prototype build plan](docs/05-build-plan.md) · [Design decisions](docs/06-design-decisions.md) · [Review note](docs/REVIEW.md)

## Concept rationale

Most noise disputes turn on one question: how loud was it, and when? A sound level meter answers that with a few numbers per second; it does not need to keep any sound. NoiseMap puts a digital MEMS microphone and a small processor in a head about 4 m above the street, turns the sound into A- and C-weighted levels on the spot, and passes only those levels to the lab's standard FieldNode solar and LoRaWAN core. The head firmware sends levels only, and it is open and published with a build hash, so residents, venues and the city can check for themselves that the street is not being listened to.

It is open and garage-buildable because the people who most need the evidence, residents' groups and small city noise teams, cannot buy certified monitoring terminals by the dozen. A MEMS microphone, a microcontroller board, a printed housing, a foam windscreen, an arm and a street pole adapter cost about $72 on top of the FieldNode core, and the open firmware lets anyone check that the node measures levels and nothing else.

## Burning platform

Noise is one of the largest environmental health burdens in cities. In the EU about 92 million people are exposed to harmful road traffic noise, and long-term transport noise is linked to about 66,000 premature deaths and about 50,000 new cases of cardiovascular disease a year ([EEA](https://www.eea.europa.eu/en/topics/in-depth/noise)). The WHO recommends keeping road traffic noise below 53 dB Lden and 45 dB Lnight ([EEA, citing WHO 2018](https://www.eea.europa.eu/publications/health-risks-caused-by-environmental)), stricter than the 55 dB Lden threshold used for EU reporting.

Yet official noise maps are mostly modeled and, in the EU, reviewed only every five years ([Directive 2002/49/EC](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32002L0049)), while complaints pile up without measurements behind them. By 2018 New York City's 311 line had logged more than 2.3 million noise complaints since 2010, more than for any other issue ([Bello et al., *Communications of the ACM*, 2018](https://arxiv.org/pdf/1805.00889)).

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| Municipal environmental health | Continuous levels to check complaints and target enforcement in nightlife districts |
| Transport and road authorities | Before and after evidence for speed limits, low-noise surfaces and truck routes |
| Hospitality licensing and night-time economy | Shared, trusted data for late-licence conditions between venues and residents |
| Construction | Monitoring agreed noise limits at site boundaries near homes |
| Public health research | Open level data linked to sleep and cardiovascular studies |
| Community groups and citizen science | Independent, inspectable evidence for council meetings and planning hearings |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| European Union | About 92 million people are exposed to harmful road traffic noise ([EEA](https://www.eea.europa.eu/en/topics/in-depth/noise)); strategic maps are modeled and updated every five years, so street-level measurements add what the maps miss. |
| United States | The EPA set 55 dB outdoors as the level that prevents interference and annoyance in 1974 ([US EPA](https://www.epa.gov/archive/epa/aboutepa/epa-identifies-noise-levels-affecting-health-and-welfare.html)); noise was New York City's most common 311 complaint when SONYC was described in 2018 ([Bello et al.](https://arxiv.org/abs/1805.00889)). |
| France (Paris region) | Bruitparif already deploys sensors in lively Paris neighborhoods and on construction sites ([Bruitparif](https://www.bruitparif.fr/la-meduse/)); an open, low-cost node could extend coverage to smaller towns. |
| India | The national real-time noise network launched in 2011 with 35 stations in seven metros, five terminals per city, with expansion to 25 cities planned ([Press Information Bureau, Government of India](https://www.pib.gov.in/newsite/erelcontent.aspx?relid=71212&reg=3&lang=2)); a few fixed terminals per city leave most streets unmeasured. |
| Sub-Saharan Africa (Nigeria) | The UN Environment Programme lists Ibadan among the cities worldwide where acceptable noise levels are surpassed ([UNEP, Frontiers 2022](https://www.unep.org/news-and-stories/press-release/deadly-wildfires-noise-pollution-and-disruptive-timing-life-cycles)); a low-cost open node can give such cities measured data. |
| Southeast Asia (Thailand, Vietnam) | Bangkok and Ho Chi Minh City are also on UNEP's list of cities where acceptable noise levels are surpassed ([UNEP, Frontiers 2022](https://www.unep.org/news-and-stories/press-release/deadly-wildfires-noise-pollution-and-disruptive-timing-life-cycles)). |

## What sparked the idea

The idea traces back to Stratumseind, a nightlife street in Eindhoven, the Netherlands, which the municipality and the Dutch Institute for Technology, Safety & Security (DITSS), with the police and local businesses, turned into a living lab. The lab tested acoustic sensors that locate breaking glass and fireworks and recognize voices under high stress, to spot rising aggression ([The Hague Security Delta](https://securitydelta.nl/services/innovation/living-labs/stratumseind)). Leon Verver, director of DITSS, said, "We are not listening in on people or record what they're saying" ([The Next Web, 2018](https://thenextweb.com/the-next-police/2018/06/08/1128392/)). People on the street had to take that on trust, and legal research on the lab argued that such collective monitoring can still limit what individuals do, even without identifying anyone ([Galič, *Ars Aequi*, 2019](https://www.researchgate.net/publication/333673572_Surveillance_privacy_and_public_space_in_the_Stratumseind_Living_Lab_the_smart_city_debate_beyond_data)). NoiseMap starts from the opposite end: measure loudness only, and publish the firmware so that residents can check the claim instead of trusting it.

## Problem

Noise harms sleep and health, but cities measure it rarely and residents' complaints lack data. Official maps are modeled averages, certified monitors are few and costly, and any microphone on a pole raises the fear of eavesdropping.

## Concept

A sound level meter node that records decibel levels only, never audio, to map traffic and nightlife noise.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

TRL 3 calculations ([NSM-CAL-001](docs/04-calcs/01-sizing.md), paper estimates): 12.2 mW average draw, 53 days without sun on the standard FieldNode cell, a measuring range of 27.9 dBA to 119 dB SPL with the IM72D128 microphone fitted by default (34.9 dBA to 113 dB SPL with the ICS-43434, which is only 103 to 108 dBA for traffic), a 22-byte record every 15 minutes, an estimated $72 of NoiseMap parts against a $100 value-engineering target and about $211 for a full node with the FieldNode core. Made constructable (sawn V-blocks, a bent sheet arm saddle with two bands, fixings throughout), the node weighs 3.45 kg, within the 3.5 kg of R10 (relaxed from 3 kg), and an automatic interval rule keeps airtime within fair use at slow data rates; accuracy, measuring range and frequency response remain at risk. See the [requirements](docs/03-requirements.md) and the decision records [NSM-DDR-001](docs/decisions/0001-trl2-review-decisions.md), [NSM-DDR-002](docs/decisions/0002-recommendations-accepted.md) and [NSM-DDR-003](docs/decisions/0003-design-for-construction.md).

**Status at TRL 3 (on paper):** of 17 product requirements, 9 are met (4 on paper, 5 by design), 2 are at risk (measuring range and frequency response, PR-004 and PR-005), 1 is not met on paper (total uncertainty, PR-003: 2.9 to 3.1 dB against a 2 dB target) and 5 are to verify at TRL 4. Nothing has been built or tested; TRL 4 is on hold.

## STEM check

Every physical, chemical and biological claim of the three concept options was checked against known science ([NSM-STM-001](docs/01b-stem-check.md)): 24 claims, 21 within known science, 3 plausible (the loudest level the microphone can take, the mass margin and street-canyon reflections) and none failing. An independent reviewer who saw only the checks and the calculation note tried to refute every verdict. Two problems were fixed under Amish's standing instruction of 2026-10-23: the microphone clipped at 113 dB SPL, which is only 103 to 108 dBA for traffic, so the Infineon IM72D128 (126 dB SPL overload point) is now fitted by default, and stainless fixings that touch aluminium are sealed against road-salt corrosion. Two findings change targets and go to Amish: PR-003 is not met on paper, and PR-002 and PR-012 hold by design only at LoRaWAN spreading factors 7 to 9.

## Concept options

Three working principles were modelled in detail and scored against the user requirements ([NSM-OPT-001](docs/02a-concept-options.md)): **A, pole clamp node** (the current design, 89 parts, 3.5 kg), **B, balcony post node** (USB power and Wi-Fi, 28 parts, 1.0 kg) and **C, luminaire socket node** (power and LoRaWAN from the streetlight, 24 parts, 0.2 kg). A scores 171, B 163 and C 152. A and B are within 10 %, so **both go to Amish; the choice is proposed, awaiting Amish** ([NSM-DDR-004](docs/decisions/0004-concept-selection.md)). The current design, option A, stays the design of record.

![Concept options at one scale](media/options.png)

## Key components

- Digital MEMS microphone on an adapter board that takes an ICS-43434 or an IM72D128, in a printed head, pointing up
- Level processor in the head computing A- and C-weighted levels once a second; audio stays in its RAM
- Standard FieldNode core: IP65 enclosure, 6 W panel, one LiFePO4 cell, MPPT charger and LoRaWAN radio
- 90 mm foam windscreen with bird spike
- Aluminum arm on a bent sheet saddle with its own two band clamps, and street pole V-blocks for 60 to 140 mm poles that fit the FieldNode back plate; no drilling of the pole

The priced bill of materials is in [bom/bom.csv](bom/bom.csv); the parametric model is [cad/src/model.py](cad/src/model.py) (kit 1.9 interface, `components(option)` for each option, detail level D3: real stock, every screw, nut and band, edge breaks; `cad/fidelity.json`), with STEP files in `cad/step/` (a file per part of option A and an assembly per option) and STL in `cad/stl/`.

## Building the prototype

The [prototype build plan](docs/05-build-plan.md) (NSM-BLD-001) shows how to make each component and fit it to the next, with a making sketch for every made part and a picture for every assembly step. The FieldNode core is built to its own plan and gets two larger V-blocks sawn from aluminium bar in place of its own; the arm saddle is bent from sheet by a local shop; the head and its cap are printed in ASA; the rest is bought. The work needs basic metalwork, 3D printing and fine soldering, and no certified trade. Every decision is indexed in the [design decisions register](docs/06-design-decisions.md).

![NoiseMap prototype: every component pulled apart and numbered in build order](docs/05-build-plan/overview.png)

## Safety

> Installing on a street pole is work at height beside traffic. The node contains a LiFePO4 cell of about 19 Wh: fuse it and charge only within the maker's temperature limits. Fit a safety lanyard to the microphone arm. Readings are indicative, not certified measurements.
>
> Privacy by design: no images, audio recordings or personal identifiers leave the device; only sound levels are stored or sent. The guarantee rests on the open head firmware and its published build hash. Check local data protection law before any deployment. Street furniture and pole mounts must be installed only with the asset owner's permission, by trained crews, with fall protection and traffic management as local rules require.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, STEM check, concept and concept options, user and product requirements, traceability, calculations, build plan, design decisions, regulatory, feasibility, risk, market and plan |
| `cad/src/` | build123d Python source, the source of truth for all geometry: `model.py` (kit 1.9 interface), option parts (`nsm_parts.py`, `nsm_options.py`), product appearance model (`product_model.py`), drawing sheet (`sheets.py`), STL export (`export_stl.py`), concept media and build plan pictures |
| `cad/step/`, `cad/stl/` | STEP per part of option A (`cad/step/A/`) and an assembly per option; STL assemblies and printed parts for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | General arrangement NSM-DWG-001 Rev P5 and the making sketches NSM-DWG-101 to 106 |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

| Document | ID |
| --- | --- |
| [Problem statement](docs/01-problem.md) | NSM-PRB-001 |
| [STEM check](docs/01b-stem-check.md) | NSM-STM-001 |
| [Design precis](docs/02-concept.md) | NSM-PRC-001 |
| [Concept options](docs/02a-concept-options.md) | NSM-OPT-001 |
| [User requirements](docs/03a-user-requirements.md) | NSM-URS-001 |
| [Product requirements and specifications](docs/03-requirements.md) | NSM-PRS-001 |
| [Traceability matrix](docs/03b-traceability.md) | NSM-RTM-001 |
| [Calculation note](docs/04-calcs/01-sizing.md) | NSM-CAL-001 |
| [Prototype build plan](docs/05-build-plan.md) | NSM-BLD-001 |
| [Design decisions register](docs/06-design-decisions.md) | NSM-DEC-001 |
| [Concept selection](docs/decisions/0004-concept-selection.md) | NSM-DDR-004 |
| [Regulatory and standards register](docs/07-regulatory.md) | NSM-REG-001 |
| [Feasibility](docs/08-feasibility.md) | NSM-FEA-001 |
| [Risk register, hazard analysis and design FMEA](docs/09-risk.md) | NSM-RSK-001 |
| [Market and viability](docs/10-market.md) | NSM-MKT-001 |
| [Project plan](docs/11-plan.md) | NSM-PLN-001 |

Earlier decision records are in `docs/decisions/` (NSM-DDR-001 to NSM-DDR-003). Pipeline stage: P3 of P0 to P6 (the portfolio cap). Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID, a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `NSM-PRC-001/v1.0`; run `python .kit/render.py --check` to validate.

## Credits

Designed by Amish Chadha. See [CONTRIBUTORS.md](CONTRIBUTORS.md) for roles. To cite this design, use [CITATION.cff](CITATION.cff) (GitHub shows it as "Cite this repository").

AI assistance (Claude) was used to accelerate concept renders, prototype documentation and first-pass sizing calculations. Design direction and all decisions are Amish Chadha's, recorded in this repository's decision records (`docs/decisions/`).

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab.
