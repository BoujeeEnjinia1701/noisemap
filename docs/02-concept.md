---
doc_id: NSM-PRC-001
title: NoiseMap design precis
project: NoiseMap
doc_type: Design precis
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Populate to TRL 2 (architecture, first-order numbers, safety, media)
---

# NoiseMap design precis

NoiseMap is a clamp-on street pole noise node. A digital MEMS microphone about 4 m above the ground feeds a small processor in the microphone head, which turns the sound into A- and C-weighted levels once a second and discards the audio within milliseconds. Only levels cross the cable to a standard FieldNode core, which sends a 22-byte record every 15 minutes over LoRaWAN. First-order numbers suggest the node draws about 21 mW, runs about 30 days without sun and measures from about 35 to 115 dBA, but the parts cost of about $171 is over the $100 budget.

![Figure 1. NoiseMap on a street pole with a 1.75 m person for scale](../media/hero.png)

## How it works

1. **Sense.** The MEMS microphone, port facing up inside a foam windscreen, streams 24-bit samples over I²S at 48 kHz to the level processor.
2. **Weight and integrate.** The processor applies A and C frequency weighting as digital filters, squares and averages the result, and computes each second the A-weighted equivalent level (LAeq,1s), the Fast time-weighted maximum and minimum (LAFmax, LAFmin) and the C-weighted equivalent level (LCeq,1s). Samples live in a small RAM buffer that is overwritten about every 20 ms.
3. **Hand over levels only.** Once a second the head sends about 12 bytes of levels to the FieldNode core over a 9,600 baud UART in the M12 cable. The head has no flash storage for data and no radio.
4. **Summarize.** The FieldNode core builds a 15-minute record: fifteen 1-minute LAeq values, the 15-minute LAeq, LAFmax and LAFmin, L10 and L90 (from the 900 one-second values), LCeq and a status byte, 22 bytes in all.
5. **Send.** The core sends each record over LoRaWAN to the lab's TwinKit gateway, a city server or The Things Network, and stores it in flash if the link is down. Night indicators (Lnight, Lden) are computed on the server from the 15-minute records.

![Figure 2. Data and energy flow (estimates)](../media/flow.png)

## Main components

Table 1. Main components. Numbers match the exploded view (Figure 3) and `bom/bom.csv`.

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | FieldNode enclosure | IP65 polycarbonate box, about 200 x 150 x 90 mm, vent and gland | From FieldNode, unchanged |
| 2 | FieldNode power and radio board | MPPT charger with cold-charge lockout, STM32WL-class LoRaWAN module, SPI flash, M12 ports | From FieldNode, unchanged |
| 3 | LiFePO4 cell | One 3.2 V 6 Ah cell | FieldNode standard is enough |
| 4 | Solar panel | 6 W, about 290 x 200 mm, doubling as a hood | FieldNode standard is enough |
| 5 | Panel tilt bracket | Flat-bar posts, about 35° tilt | From FieldNode |
| 6 | Pole mounting kit | Back plate and band clamps for 60 to 140 mm poles | Larger clamps than FieldNode's 40 to 60 mm kit |
| 7 | Microphone arm | 25 mm aluminum tube, about 400 mm reach toward the street | Keeps the microphone about 0.45 m from the pole face |
| 8 | Microphone head housing | 3D-printed ASA tube, 40 mm OD x 150 mm, drip skirt, acoustic membrane | Proposed, awaiting Amish |
| 9 | MEMS microphone | ICS-43434 class I²S, 65 dB SNR, 120 dB SPL overload ([TDK InvenSense](https://invensense.tdk.com/products/ics-43434/)) | Listed as end of life; alternative proposed, awaiting Amish |
| 10 | Level processor | Cortex-M4F class low-power board (STM32L4 class) | Proposed, awaiting Amish |
| 11 | Windscreen and bird spike | 90 mm open-cell foam ball, bored to fit the head | Replace about yearly (estimate) |
| 12 | Sensor cable | M12 5-pin, about 1.5 m, 3.3 V and UART | FieldNode standard pinout |

![Figure 3. Exploded view with BOM numbers](../media/exploded.png)

![Figure 4. Cutaway: FieldNode enclosure with cell and board (lower left), microphone head with processor and microphone inside the windscreen bore (upper right)](../media/cutaway.png)

## First-order numbers

All values are estimates for concept review and will be checked at TRL 3.

Table 2. First-order numbers.

| Quantity | Estimate | Basis and assumptions | Requirement |
| --- | --- | --- | --- |
| Microphone self-noise | about 29 dBA | 94 dB SPL reference minus 65 dB SNR (datasheet class value) | |
| Lower measuring limit | about 35 dBA | Self-noise 6 dB below the signal adds about 1 dB; correctable by subtracting the noise floor | R4 at risk below 35 dBA |
| Upper measuring limit | about 115 dBA | 120 dB SPL acoustic overload point, 5 dB margin for peaks | R4 met |
| Raw audio rate | about 1.2 Mbit/s, held only in RAM | 48 kHz x 24 bits | R1 |
| Level data over the cable | about 0.1 kbit/s | About 12 bytes per second including framing | R1 met by design |
| Uplink record | 22 bytes per 15 min, 96 uplinks/day | 15 x 1-byte 1-minute LAeq (0.5 dB steps), 6 statistics, 1 status | R2 met |
| Radio airtime | about 0.25 s per uplink, about 24 s/day | SF9 at 125 kHz, 35 bytes with LoRaWAN overhead; The Things Network fair use allows 30 s of uplink per day per node ([TTN](https://www.thethingsnetwork.org/docs/lorawan/duty-cycle/)) | R12 met at SF9 or faster; **not met** at SF10 without longer intervals |
| Microphone and processor power | about 18 mW | About 0.5 mA microphone and 5 mA processor at 3.3 V (typical class values, to be confirmed) | |
| Total load from the cell | about 21 mW, about 0.51 Wh/day | Head 18 mW, FieldNode core and radio about 1 mW, rails 90 % efficient | Within FieldNode's about 115 mW sensor allowance |
| Battery autonomy | about 30 days | 15.4 Wh usable (19.2 Wh cell, 80 %) | R7 met |
| Winter solar harvest | about 5.8 Wh/day into the cell | 6 W x 1.5 peak sun hours x 0.8 derating x 0.85 charger x 0.95 cell | R7 met (about 11 times the load) |
| Mass on the pole | about 2.3 kg | FieldNode about 1.7 kg, arm 0.25 kg, head and windscreen 0.15 kg, cable and larger clamps 0.2 kg | R10 met |
| Wind load on the panel | about 50 N | 0.058 m², 35 m/s gust, force coefficient 1.2 | R10, bracket to check |
| Parts cost | about $171 (FieldNode core about $119, NoiseMap parts about $52) | Indicative prices, see `bom/bom.csv` | R13 **not met** |

The numbers above are for the electronics only. The accuracy of the measurement depends on the housing, the membrane, the windscreen, reflections from the pole and nearby facades, and wind, none of which can be settled on paper.

## Key design choices

- **Levels, never audio.** The only data that leaves the microphone head are levels once a second. The head has no data storage and no radio, and the firmware has no code path that writes or sends samples. Proposed, awaiting Amish.
- **Where privacy comes from.** The 9,600 baud cable link is far too slow for raw audio (about 1.2 Mbit/s), and the LoRaWAN link averages well under 100 bit/s under duty-cycle and fair-use limits. Neither alone rules out a heavily compressed speech codec, so the privacy guarantee rests on open, auditable head firmware with read-out protection and a published build hash. This is stated plainly so no one relies on a stronger claim. Proposed, awaiting Amish.
- **Processing in the head, not in FieldNode.** Keeping the audio next to the microphone means the M12 cable only ever carries levels. Proposed, awaiting Amish.
- **Standard FieldNode core.** At about 21 mW the node fits FieldNode's sensor allowance with its standard 6 W panel and one cell, so no power upgrade is needed. Proposed, awaiting Amish.
- **Microphone about 4 m above the ground, 0.45 m from the pole, pointing up.** This matches noise-mapping practice and reduces the pole reflection. Proposed, awaiting Amish.
- **A and C weighting.** LAeq and its statistics follow common practice; LCeq, and the difference LCeq minus LAeq, flags amplified bass from venues that A weighting under-reports. Proposed, awaiting Amish.
- **Microphone part.** The ICS-43434 is widely used (DNMS supports it) but TDK lists it as end of life. The Infineon IM72D128 is the alternative DNMS already supports. Proposed: design for either on a small adapter board, awaiting Amish.
- **Field calibration.** Each node is checked with a sound calibrator (94 dB at 1 kHz) at install and at each windscreen change, and compared with a class 1 reference meter at one site. Proposed, awaiting Amish.

## Safety

> **Safety:** Installing on a street pole is work at height next to traffic. Install only with the pole owner's permission, by trained crews, with fall protection and traffic management as local rules require. Keep clear of overhead power lines and street-light wiring, and never open a pole's electrical hatch.

> **Safety:** The node contains a LiFePO4 cell of about 19 Wh. Fuse the cell, charge only within the cell maker's temperature limits (FieldNode's cold-charge lockout applies), and do not install a node with a swollen or damaged cell.

> **Safety:** A falling part from 4 m can injure people below. Fit a secondary safety lanyard to the microphone arm and check the clamps after the first storm.

> **Safety:** Do not test the node near its upper range with loudspeakers or calibrators at close range without hearing protection.

**Privacy.** No images, audio recordings or personal identifiers leave the device; only sound levels are stored or sent. Check local data protection law before any deployment, publish the head firmware and its build hash, and put a notice on the pole saying what is measured and where the design is documented.

**Use of the data.** NoiseMap readings are indicative. They are not certified measurements and must not be presented as legal evidence without a co-located certified instrument.

## Open questions for TRL 3

- Measure the frequency response and noise floor of the chosen microphone in the printed head, with and without the acoustic membrane and windscreen.
- Check the low-frequency response below about 60 Hz, which limits LCeq for amplified bass.
- Decide how to flag wind- and rain-contaminated intervals without a wind sensor (for example, from the spread of 1-second levels or low-frequency energy), or add a small wind sensor.
- Estimate the error from reflections off the pole and nearby facades at 0.45 m.
- Confirm processor current at 48 kHz with A and C filtering; check whether a lower sample rate is acceptable.
- Choose the first co-design partner and street, and agree how residents and the city will share the data.

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html).
