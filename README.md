# NoiseMap

**Area:** Smart Cities · **Status:** Concept · **Prototype budget:** about $100 USD · **Difficulty:** 2 of 5

A sound level meter node that records decibel levels only, never audio, to map traffic and nightlife noise.

## Concept rationale

Level-only measurement gives evidence without any privacy risk.

## Burning platform

Environmental noise is a recognized health risk in dense cities.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| _To be developed_ | |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| _To be developed_ | |

## What sparked the idea

It came out of a September 2026 review of Design Molecule's applied research areas against the open projects already in the lab.

## Problem

Noise harms sleep and health, but cities measure it rarely and residents' complaints lack data.

## Concept

A sound level meter node that records decibel levels only, never audio, to map traffic and nightlife noise.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- MEMS microphone with on-device A-weighted level calculation
- FieldNode core
- Windscreen
- Pole mount

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

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

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab. Smart cities set.
