---
doc_id: NSM-MKT-001
title: NoiseMap market and viability
project: NoiseMap
doc_type: Market and viability
version: "0.1"
status: Draft
date: '2026-11-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-11-02'
  author: Amish Chadha
  change: First issue (kit 1.8 pipeline)
---

# NoiseMap market and viability

NoiseMap is for residents' groups, city noise teams and researchers who need street-level noise evidence in many places and cannot buy certified terminals by the dozen; an open design lets them inspect what is measured. Public prices for certified terminals were not found in this session, so the cost comparison below rests on the SONYC parts cost and on the priced BOM, and the certified-terminal price is "to assess". Method: STANDARDS section 23. Prices and benchmarks carry the date they were checked.

Table 1. Market segments.

| Segment | Target users and region | Competitive benchmark (cited price) | Estimated cost per unit (USD) | Value proposition |
| --- | --- | --- | --- | --- |
| City environmental health and noise teams | Nightlife districts, depots, main roads; EU and US cities | Certified class 1 monitoring terminals: price to assess (no public list price found; the PCE Instruments class 1 meter page shows "price excl. VAT" without a figure, checked 2026-11-02). SONYC research node: about USD 80 in parts each (Bello et al. 2018, cited in NSM-PRB-001) | NoiseMap parts 72.00; full node 211.00 (priced BOM, September 2026 estimates) | Many more measurement points per budget, inspectable levels-only firmware |
| Residents' associations and citizen science | Streets with bars, markets, delivery routes | Sensor.Community DNMS: open design on a Teensy and ESP8266, mains or USB and Wi-Fi (https://github.com/hbitter/DNMS, cited in NSM-PRB-001); kit price to assess | 211.00 (option A); about 38 for the balcony node (option B, estimate) | Evidence from a device they can inspect, at street height |
| Licensing authorities and venue operators | Entertainment districts | Same as city teams; a shared, trusted record is the product | 211.00 | One record both sides can read |
| Researchers and students | Universities, public health programs | SONYC and Bruitparif Meduse (https://www.bruitparif.fr/la-meduse/); Meduse price to assess | 211.00 | Open data format and calibration method |
| Transport and planning departments | Main roads, school streets | Class 1 terminals, price to assess | 211.00 | Before and after evidence for calming and surfaces |

Component price signal (not a node price): a distributor lists the ICS-43434 microphone at USD 1.61 each at a minimum order of 10,000 (https://dasenic.com/product/tdk-invensense-ics-43434-3491, checked 2026-11-02, currency inferred from the $ sign), which is why the microphone is a small part of the USD 7 BOM line for the adapter board.

## Open route

Who would build it: a university acoustics group, a makerspace or a city noise team with a workshop; the build needs sawing, bending, a printer and fine soldering but no certified trade. How it spreads: through the repository, workshops, and Sensor.Community-style volunteer groups (NSM-PRB-001 O1). What keeps it open: CERN-OHL-S-2.0 for hardware and MIT for software, which require changes to be shared back, and a published firmware build hash so anyone can check the levels-only claim. A commercial route (a certified product) is out of scope; certification would be a separate project (NSM-REG-001).

Viability, on paper: the NoiseMap parts are USD 28 under the USD 100 target, but the full node at USD 211 exceeds twice that target because the FieldNode core is costed in its own repository; whether USD 211 is cheap enough for residents' groups is to assess with a co-design partner.

## Sources

- Bello, Juan Pablo, et al. 2018. "SONYC: A System for the Monitoring, Analysis and Mitigation of Urban Noise Pollution." https://arxiv.org/abs/1805.00889 (cited in NSM-PRB-001 on 2026-10-02).
- Bitter, H. DNMS: Digital Noise Measurement Sensor. https://github.com/hbitter/DNMS (cited in NSM-PRB-001 on 2026-10-02).
- Bruitparif. La Meduse. https://www.bruitparif.fr/la-meduse/ (cited in NSM-PRB-001 on 2026-10-02).
- PCE Instruments. PCE-430 class 1 sound level meter page. https://pce-instruments.com/eu/measuring-instruments/test-meters/sound-level-meter-noise-level-meter-pce-instruments-class-1-sound-level-meter-pce-430-det_5971611.htm (read 2026-11-02; no price shown).
- Dasenic. TDK InvenSense ICS-43434 listing. https://dasenic.com/product/tdk-invensense-ics-43434-3491 (read 2026-11-02).
