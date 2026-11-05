---
doc_id: NSM-REG-001
title: NoiseMap regulatory and standards register
project: NoiseMap
doc_type: Regulatory and standards register
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

# NoiseMap regulatory and standards register

Which standards and regulations bear on a street sound level node, where, and what is needed. Not legal advice; anything marked "to assess" needs a qualified reviewer before any product claim. Seven of fourteen items are marked to assess and none is a certification NoiseMap holds. NoiseMap is a research and educational prototype and a non-certified indicative instrument; it must not be presented as a class 1 or class 2 sound level meter or as legal evidence. Method: STANDARDS section 23. Dates are the day a link was found or read in the 2026-11-02 session; where a standard number is "as known" or "as cited earlier", the text was not re-read and that is said in the row.

Table 1. Regulatory and standards register.

| # | Standard or regulation | Jurisdiction | What it covers | Applicability to this design | Owner (role) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| G1 | Directive 2002/49/EC, assessment and management of environmental noise (Lden, Lnight, 4.0 m assessment height) | EU | Strategic noise maps and indicators | Gives the 4.0 m height and the indicators NoiseMap reports against; the node is not a mapping instrument under it | Design lead | Does not apply as a compliance duty; used as the measurement convention. Source: EUR-Lex, checked 2026-11-02 |
| G2 | IEC 61672-1:2013, sound level meters, specifications | International | Class 1 and class 2 sound level meters; weighting and tolerances | NoiseMap follows the definitions of A and C weighting where practical (PR-005) and must not be presented as a class 1 or class 2 instrument. Source: IEC webstore, cited in NSM-PRB-001 (2026-10-02) | Design lead | Does not apply as certification; certification needed later if a class is ever claimed (TRL 4 and later, on hold) |
| G3 | ETSI EN 300 220 series, short-range devices 25 MHz to 1000 MHz; EU868 duty cycle of 1 % | EU | Radio parameters and duty cycle in the 868 MHz band | The LoRaWAN radio of the FieldNode core; airtime in NSM-CAL-001 F (PR-012). Number as cited in the earlier NSM-REQ-001 R12; text not re-read in this session | Design lead | Applies; met on paper for duty cycle (NSM-CAL-001 F) |
| G4 | Radio Equipment Directive 2014/53/EU | EU | Placing radio equipment on the EU market (essential requirements, conformity, marking) | A node with its own radio is radio equipment; the FieldNode module's conformity may carry over only if the module is used within its approval. Source: EUR-Lex, https://eur-lex.europa.eu/eli/dir/2014/53/oj, checked 2026-11-02 | Regulatory consultant | To assess; certification needed later for any product placed on the market |
| G5 | The Things Network fair use policy (30 s uplink airtime per day per node) | Network (community) | Shared network airtime | Drives the interval rule at SF10 to SF12 (PR-012). Source: https://www.thethingsnetwork.org/forum/t/the-things-network-fair-use-policy/47689, checked 2026-11-02 (policy page listed by search; the 30 s figure is as cited in NSM-REQ-001 R12) | Design lead | Applies; met on paper (NSM-CAL-001 F) |
| G6 | Regulation (EU) 2016/679, General Data Protection Regulation | EU | Personal data; a recording of speech could be personal data | NoiseMap stores and sends levels only, by design (PR-001); whether a level time series at a street can ever identify a person is to assess. Source: EUR-Lex, https://eur-lex.europa.eu/eli/reg/2016/679/oj, checked 2026-11-02 | Data protection adviser | To assess with a data protection adviser before any deployment; other jurisdictions to assess |
| G7 | Low Voltage Directive 2014/35/EU and EMC Directive 2014/30/EU | EU | Electrical safety and electromagnetic compatibility of equipment | Option A runs from a 3.2 V cell and a 6 W panel, which is below the Low Voltage Directive's mains range, so only EMC is expected to apply; option C has mains inside. Directive numbers as known; links not checked in this session | Regulatory consultant | To assess (A: EMC; C: both) |
| G8 | Battery rules for lithium cells: UN transport tests (UN 38.3), IEC 62133-2 cell safety, Regulation (EU) 2023/1542 | International, EU | Safe lithium cells, transport and battery placing on the market | The 19 Wh LiFePO4 cell is a FieldNode core part; the cell maker's test reports are the evidence. Numbers as known; texts not checked in this session | Regulatory consultant | To assess (FieldNode core item; cited once there) |
| G9 | IEC 60529, degrees of protection (IP code) | International | Ingress protection ratings | PR-008 asks for IP65; no rating is claimed for the printed head, only a design intent (drip skirt, membrane, bored windscreen). Number as known | Design lead | Applies as a target; certification needed later |
| G10 | Pole and column loading, for example the EN 40 series for lighting columns | EU, national | Loads a column is designed to carry | The node adds about 96 N at 3.5 to 4 m in a 35 m/s gust (NSM-CAL-001 H); the pole owner confirms the pole can take it. Which national rule applies is to assess | Pole owner | To assess per jurisdiction and pole |
| G11 | ANSI C136.41 dimming receptacle and Zhaga Book 18 (outdoor luminaire sensor and communication nodes) | US (ANSI), international (Zhaga) | The receptacle on a luminaire that a sensing node plugs into | Only option C. Zhaga Book 18 edition 3.0 (April 2021) adds a hybrid with an ANSI C136.41 receptacle. Source: https://zhagastandard.org/books/overview/smart-interface-between-outdoor-luminaires-and-sensing-communication-modules-18.html, checked 2026-11-02 | Lighting operator | To assess (option C only) |
| G12 | IEC 62368-1, safety of audio/video, information and communication equipment | International | Product safety including isolation and creepage | Only option C (mains converter inside a sealed puck); not a STEM row. Number as known; text not checked | Regulatory consultant and electrician | To assess (option C only); certification needed later |
| G13 | Work at height and traffic management at installation (national rules) | National | Fall protection, lifts, traffic control | The safety notes in NSM-PRC-001; installation is by trained crews with the pole owner's permission | Installer | Applies at installation; local rules to assess |
| G14 | Noise exposure limits for people using a calibrator (NIOSH recommended 85 dBA for 8 h, 3 dB exchange) | US guidance, widely used | Hearing protection time at 94 dB | The 94 dB calibrator check is about 2 minutes (STM S19, PR-009). Source: https://www.cdc.gov/niosh/bulletin/2022/noise-50.html, checked 2026-11-02 | Technician | Applies as guidance; met by design |

Status: to assess, applies, does not apply, met by design, certification needed later.

## Sources

- European Parliament and Council. 2002. Directive 2002/49/EC relating to the assessment and management of environmental noise. https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32002L0049 (cited in NSM-PRB-001).
- International Electrotechnical Commission. 2013. IEC 61672-1, Electroacoustics: Sound level meters, Part 1. https://webstore.iec.ch/en/publication/5708 (cited in NSM-PRB-001).
- European Parliament and Council. 2014. Directive 2014/53/EU on radio equipment. https://eur-lex.europa.eu/eli/dir/2014/53/oj (found 2026-11-02).
- The Things Network. Fair Use Policy. https://www.thethingsnetwork.org/forum/t/the-things-network-fair-use-policy/47689 (found 2026-11-02).
- European Parliament and Council. 2016. Regulation (EU) 2016/679 (General Data Protection Regulation). https://eur-lex.europa.eu/eli/reg/2016/679/oj (found 2026-11-02).
- Zhaga Consortium. Book 18, smart interface between outdoor luminaires and sensing and communication modules. https://zhagastandard.org/books/overview/smart-interface-between-outdoor-luminaires-and-sensing-communication-modules-18.html (read 2026-11-02).
- National Institute for Occupational Safety and Health. NIOSH Noise: a 50-year timeline. https://www.cdc.gov/niosh/bulletin/2022/noise-50.html (found 2026-11-02).
