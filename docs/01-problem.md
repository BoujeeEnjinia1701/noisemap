---
doc_id: NSM-PRB-001
title: NoiseMap problem statement
project: NoiseMap
doc_type: Problem statement
version: "0.6"
status: Draft
date: '2026-10-02'
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
  change: Populate to TRL 2 (problem, users, context, constraints, prior work, open questions)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3; budget scope, privacy wording and open questions updated per NSM-DDR-001
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-10-01'
  author: Amish Chadha
  change: Cost figures from NSM-CAL-001 v0.3; budget as a value-engineering target
- version: "0.6"
  date: '2026-10-02'
  author: Amish Chadha
  change: First co-design partner to approach, decided on 2026-10-02 (NSM-DEC-001)
---

# NoiseMap problem statement

Traffic and nightlife noise harm sleep and health, but most cities know their noise levels only from computer models updated every few years, and residents who complain have no measurements of their own. The gap is a low-cost, open street node that measures sound levels continuously and, by design, never records or sends audio.

## The problem

Environmental noise is a large and well-documented health burden. In Europe, road traffic is the main source: about 92 million people in the EU are exposed to harmful day-evening-night road traffic noise, and long-term exposure to transport noise is linked to about 66,000 premature deaths and about 50,000 new cases of cardiovascular disease each year ([EEA](https://www.eea.europa.eu/en/topics/in-depth/noise)). The WHO recommends keeping road traffic noise below 53 dB Lden and 45 dB Lnight, stricter than the 55 dB Lden and 50 dB Lnight thresholds used for EU reporting ([EEA, citing WHO 2018](https://www.eea.europa.eu/publications/health-risks-caused-by-environmental)). In the United States, the EPA identified 55 dB outdoors as the level that prevents activity interference and annoyance as long ago as 1974 ([US EPA](https://www.epa.gov/archive/epa/aboutepa/epa-identifies-noise-levels-affecting-health-and-welfare.html)).

Measurement lags far behind. The EU Environmental Noise Directive requires strategic noise maps for large agglomerations, reviewed at least every five years, using the Lden and Lnight indicators ([Directive 2002/49/EC](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32002L0049)). These maps are mostly calculated from traffic models, so they show long-term averages well but miss what residents complain about: bar and club noise at 2 a.m., delivery trucks before dawn, construction, and street events. Most cities outside Europe have no maps at all.

Complaints are frequent but carry little evidence. When the SONYC team described their network in 2018, New York City's 311 line had logged more than 2.3 million noise complaints since 2010, more than for any other issue ([Bello et al., SONYC](https://arxiv.org/abs/1805.00889)). An officer who arrives an hour later often finds the noise has stopped. A resident with a phone app has an uncalibrated reading from inside a flat, which a licensing hearing can dismiss.

Continuous monitoring exists but is costly or intrusive. Certified class 1 monitoring terminals are priced for agencies and are deployed a few at a time. Research networks have shown low-cost sensors work, but some record short audio clips to identify sources (the SONYC nodes sampled 10-second clips at random, encrypted, during a limited period), and any microphone on a pole raises the fear that it is listening to conversations.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Residents and residents' associations | Credible, continuous evidence of night-time noise near their homes, from a device they can inspect | Streets with bars, clubs, markets, delivery routes |
| City environmental health or noise team | Low-cost measurement to target enforcement and check complaints | Nightlife districts, construction sites, depots |
| Transport and planning departments | Before and after evidence for traffic calming, low-noise surfaces, speed limits and truck routes | Main roads, school streets |
| Licensing authorities and venue operators | Shared, trusted data to set and check conditions on late licences | Entertainment districts |
| Researchers and students | Open, documented level data linked to health, sleep and urban form studies | Universities, public health programs |
| Pole or asset owner | A light clamp-on device that needs no drilling or mains connection | Street lighting and signal poles |

Operating context: clamped to an existing street pole with the microphone about 4 m above the ground (the 4.0 ± 0.2 m assessment height the EU uses for strategic noise maps, [Directive 2002/49/EC, Annex I](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32002L0049)), outdoors for years in sun, rain, dust, wind and temperatures from about -20 °C to +50 °C (estimate of the design range), usually with no daytime power at the pole.

## Constraints

- Garage-buildable prototype. The $100 value-engineering target covers the NoiseMap parts, estimated at $72.00; the FieldNode core is costed in the FieldNode repo ($139.00), so a full node is about $211 (NSM-DDR-001 D1, NSM-CAL-001).
- Built on the lab's shared **FieldNode** power and radio core, as the FieldNode README lists NoiseMap among its intended users.
- Privacy by design: no images, audio recordings or personal identifiers leave the device; only sound levels are stored or sent. The guarantee rests on open, auditable head firmware with read-out protection and a published build hash, not on the data links alone (NSM-DDR-001 D2).
- Clamp-on mounting with no drilling, welding or electrical connection to the pole.
- Open hardware (CERN-OHL-S-2.0) and open firmware (MIT), so any city or residents' group can audit what the device measures.
- Measurements should follow the definitions of IEC 61672-1 for sound level meters ([IEC](https://webstore.iec.ch/en/publication/5708)) where practical, but the node is not a certified instrument and must not be presented as one.

## Prior work

- **Sensor.Community DNMS.** An open Digital Noise Measurement Sensor that reads an ICS-43434 MEMS microphone over I²S, or an IM72D128 through a PDM to I²S converter, on a Teensy board and reports LAeq, LAmin and LAmax to the Sensor.Community network through an ESP8266 ([DNMS on GitHub](https://github.com/hbitter/DNMS)). It is mains or USB powered and uses Wi-Fi, which suits balconies but not most street poles.
- **SONYC (Sounds of New York City).** A research network of low-cost acoustic sensors, about $80 in parts each, with 45 deployed in New York when described; it measured sound levels continuously and also sampled encrypted audio clips for machine listening ([Bello et al.](https://arxiv.org/abs/1805.00889)).
- **Bruitparif Méduse.** A four-microphone sensor used in Paris neighborhoods and on construction sites that measures levels and locates the main source directions several times a second ([Bruitparif](https://www.bruitparif.fr/la-meduse/)).
- **Certified monitoring terminals.** Class 1 instruments used by agencies and airports; accurate and traceable, but priced for a handful of sites.

No open, solar-powered, LoRaWAN street node that is designed never to store or transmit audio was found.

## Out of scope

- Recording, storing or transmitting audio in any form, including short clips for source identification.
- Identifying people, voices or conversations.
- Certified or legally binding measurement (class 1 or legally certified instruments).
- Indoor noise and occupational noise exposure.
- Enforcement actions based on the node alone.

## User research and co-design

This design is for communities the author is not part of, so requirements come from the people who will use it.

- [ ] Identify a local partner organization. First candidate to approach (decided 2026-10-02, not yet agreed): a city environmental noise team or a university acoustics group that can put a Class 1 reference sound level meter beside the node on the test street; a Sensor.Community group is a useful second contact for volunteer hosts
- [ ] Run co-design sessions with intended users; record who, where and what was learned
- [ ] Validate load, distance, terrain and cost assumptions in the field
- [ ] Revise requirements (REQ) from findings before freezing the design

## Open questions

- Which partner and street first? Decided by Amish on 2026-10-02 (NSM-DDR-001 O1): the first candidate to approach is a city environmental noise team or a university acoustics group that can put a Class 1 reference sound level meter beside the node on the test street; a Sensor.Community group is a useful second contact for volunteer hosts. Not yet agreed with any partner.
- 1-minute detail: fifteen 1-minute LAeq values in each 15-minute record. Decided by Amish, 2026-09-25: go with recommendation (NSM-DDR-001 D5).
- Low-frequency levels for amplified bass: LCeq in each record. Decided by Amish, 2026-09-25: go with recommendation (D5, D12).
- Public notice: a plate on each pole saying what is measured, with a link to this repository. Decided by Amish, 2026-09-25: go with recommendation (D8).
