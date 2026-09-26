# NoiseMap

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Smart Cities · **TRL:** 2 of 9 (concept formulated) · **Prototype budget:** about $100 USD · **Difficulty:** 2 of 5

A sound level meter node that records decibel levels only, never audio, to map traffic and nightlife noise.

![NoiseMap concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [Review note](docs/REVIEW.md)

## Concept rationale

Most noise disputes turn on one question: how loud was it, and when? A sound level meter answers that with a few numbers per second; it does not need to keep any sound. NoiseMap puts a digital MEMS microphone and a small processor in a head about 4 m above the street, turns the sound into A- and C-weighted levels on the spot, and passes only those levels to the lab's standard FieldNode solar and LoRaWAN core. Because audio never leaves the head, residents, venues and the city can all accept the data without anyone fearing that the street is being listened to.

It is open and garage-buildable because the people who most need the evidence, residents' groups and small city noise teams, cannot buy certified monitoring terminals by the dozen. A MEMS microphone, a microcontroller board, a printed housing and a foam windscreen cost about $52 on top of FieldNode, and the open firmware lets anyone check that the node measures levels and nothing else.

## Burning platform

Noise is one of the largest environmental health burdens in cities. In the EU about 92 million people are exposed to harmful road traffic noise, and long-term transport noise is linked to about 66,000 premature deaths and about 50,000 new cases of cardiovascular disease a year ([EEA](https://www.eea.europa.eu/en/topics/in-depth/noise)). The WHO recommends keeping road traffic noise below 53 dB Lden and 45 dB Lnight ([EEA, citing WHO 2018](https://www.eea.europa.eu/publications/health-risks-caused-by-environmental)), stricter than the 55 dB Lden threshold used for EU reporting.

Yet official noise maps are mostly modeled and, in the EU, reviewed only every five years ([Directive 2002/49/EC](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32002L0049)), while complaints pile up without measurements behind them. By 2018 New York City's 311 line had logged more than 2.3 million noise complaints since 2010, more than for any other issue ([Bello et al., SONYC](https://arxiv.org/abs/1805.00889)).

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
| India | Dense, fast-growing cities with heavy traffic and horn use, where official monitoring covers few sites and residents' groups often lack data. |
| Sub-Saharan Africa | Rapidly growing cities such as Lagos and Nairobi, with busy roads, generators and street trade, have little or no routine noise monitoring. |
| Latin America | Large cities with active street nightlife, where a level-only design helps win residents' trust in public sensors. |

## What sparked the idea

It came out of a September 2026 review of Design Molecule's applied research areas against the open projects already in the lab. The trigger in the wider world is that open, low-cost noise sensing already works, as the Sensor.Community DNMS project shows ([DNMS](https://github.com/hbitter/DNMS)), but there is still no open, solar-powered street node designed from the start so that it cannot keep or send audio.

## Problem

Noise harms sleep and health, but cities measure it rarely and residents' complaints lack data. Official maps are modeled averages, certified monitors are few and costly, and any microphone on a pole raises the fear of eavesdropping.

## Concept

A sound level meter node that records decibel levels only, never audio, to map traffic and nightlife noise.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

First-order estimates (to be checked at TRL 3): about 21 mW average draw, about 30 days without sun on the standard FieldNode cell, a measuring range of about 35 to 115 dBA, a 22-byte record every 15 minutes, about 2.3 kg on the pole and about $171 in parts, over the $100 budget. See the [requirements](docs/03-requirements.md), including the requirements not yet met.

## Key components

- Digital I²S MEMS microphone (ICS-43434 class, part choice awaiting Amish) in a printed head, pointing up
- Level processor in the head computing A- and C-weighted levels once a second; audio stays in its RAM
- Standard FieldNode core: IP65 enclosure, 6 W panel, one LiFePO4 cell, MPPT charger and LoRaWAN radio
- 90 mm foam windscreen with bird spike
- Aluminum arm and band-clamp pole mount, no drilling

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Installing on a street pole is work at height beside traffic. The node contains a LiFePO4 cell of about 19 Wh: fuse it and charge only within the maker's temperature limits. Fit a safety lanyard to the microphone arm. Readings are indicative, not certified measurements.
>
> Privacy by design: no images, audio recordings or personal identifiers leave the device; only aggregate counts or levels are stored. Check local data protection law before any deployment. Street furniture and pole mounts must be installed only with the asset owner's permission, by trained crews, with fall protection and traffic management as local rules require.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (NSM-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `NSM-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab. Smart cities set.
