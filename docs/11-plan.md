---
doc_id: NSM-PLN-001
title: NoiseMap project plan
project: NoiseMap
doc_type: Project plan
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

# NoiseMap project plan

Current stage: P3, design outputs (TRL 3, paper). The next gate is P4, verification, which is on hold under the portfolio cap. Decision requested: choose between concept options A and B (within 10 %) or confirm A as the design of record (NSM-DDR-004, "Proposed, awaiting Amish"). Method: STANDARDS sections 19 and 23.

## Workstreams

Table 1. Workstreams.

| Workstream | Owner (role) | Deliverable | Status |
| --- | --- | --- | --- |
| Problem and users | Design lead | NSM-PRB-001 with users and stakeholders | Done (v0.7) |
| STEM check | Design lead | NSM-STM-001, `docs/04-calcs/stem_check.py` | Done; independent review recorded |
| Concept options | Design lead | NSM-OPT-001, three options modelled at D3, NSM-DDR-004 | Done; choice awaiting Amish |
| Requirements and traceability | Design lead | NSM-URS-001, NSM-PRS-001, NSM-RTM-001 | Done; no gaps |
| Calculations | Design lead | NSM-CAL-001 | Done (option A) |
| CAD | Design lead | `cad/src/model.py` (kit 1.9, D3), STEP, drawings NSM-DWG-001 and 101 to 106 | Done |
| Build plan and BOM | Design lead | NSM-BLD-001, `bom/bom.csv` | Done |
| Regulatory, feasibility, risk, market | Design lead, regulatory consultant | NSM-REG-001, NSM-FEA-001, NSM-RSK-001, NSM-MKT-001 | Done; several items to assess |
| Co-design | Partner (to find) | Reviewed URS and PRS | Not started (no partner agreed) |
| Verification (TRL 4) | Test lead | Test plans, reference-meter comparison | On hold (portfolio cap) |

## Resources needed

Table 2. Resources. Planned work only; nothing here is started or purchased. Costs are not estimated where a partner or consultant would set them (to assess).

| Resource | Deliverable | Effort | Estimated cost (USD) |
| --- | --- | --- | --- |
| Acoustics partner with a class 1 meter | Side-by-side comparison for PR-003 to PR-005 | To assess | To assess |
| Regulatory consultant | Items marked to assess in NSM-REG-001 | To assess | To assess |
| Data protection adviser | GDPR review of the levels-only claim | To assess | To assess |
| Workshop with sawing, bending and printing | Prototype parts (TRL 4) | To assess | NoiseMap parts 72.00 plus FieldNode core 139.00 per node (priced BOM) |

## Stage gates

Table 3. Stages (P4 to P6 on hold while the stage cap is P3).

| Stage | Gate criteria | Status |
| --- | --- | --- |
| P0 Proposal | PRB with users, STM, OPT, REG, FEA, PLN | Passed |
| P1 Definition | URS, PRS draft, RSK, MKT | Passed |
| P2 Design inputs | PRS with targets, CAL, RTM, DDR, STM closed | Passed |
| P3 Design outputs | Model (D3), STEP, drawings, priced BOM, build plan, DEC, design FMEA, traceability complete | Reached 2026-11-02 |
| P4 Verification | Test plans and reports, reliability plan | On hold |
| P5 Validation | Field trial with a partner | On hold |
| P6 Commercialization | Launch plan, with a named deployment partner | On hold |

## Next steps and decision requested

1. Amish decides the concept (NSM-DDR-004): carry A, carry B, or carry A and offer B as a companion node.
2. Find the co-design partner decided on 2026-10-02 and revise NSM-URS-001 and NSM-PRS-001 with them.
3. When the cap is lifted: plan the TRL 4 reference-meter comparison for the three at-risk requirements. Not started.

## References

Every source cited in this repository's documents, Chicago style. Items marked (2026-11-02) were found or read in the kit 1.9.1 upgrade session; the others were cited in earlier documents.

- Bello, Juan Pablo, et al. 2018. "SONYC: A System for the Monitoring, Analysis and Mitigation of Urban Noise Pollution." https://arxiv.org/abs/1805.00889.
- Bitter, H. DNMS: Digital Noise Measurement Sensor. https://github.com/hbitter/DNMS.
- Bruitparif. La Meduse. https://www.bruitparif.fr/la-meduse/.
- European Environment Agency. Noise. https://www.eea.europa.eu/en/topics/in-depth/noise.
- European Environment Agency. Health risks caused by environmental noise in Europe (citing WHO 2018). https://www.eea.europa.eu/publications/health-risks-caused-by-environmental.
- European Parliament and Council. 2002. Directive 2002/49/EC. https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32002L0049.
- European Parliament and Council. 2014. Directive 2014/53/EU. https://eur-lex.europa.eu/eli/dir/2014/53/oj (2026-11-02).
- European Parliament and Council. 2016. Regulation (EU) 2016/679. https://eur-lex.europa.eu/eli/reg/2016/679/oj (2026-11-02).
- International Electrotechnical Commission. 2013. IEC 61672-1. https://webstore.iec.ch/en/publication/5708.
- TDK InvenSense. ICS-43434. https://invensense.tdk.com/products/ics-43434/.
- The Things Network. Fair Use Policy. https://www.thethingsnetwork.org/forum/t/the-things-network-fair-use-policy/47689 (2026-11-02).
- US Environmental Protection Agency. EPA identifies noise levels affecting health and welfare. https://www.epa.gov/archive/epa/aboutepa/epa-identifies-noise-levels-affecting-health-and-welfare.html.
- Zhaga Consortium. Book 18. https://zhagastandard.org/books/overview/smart-interface-between-outdoor-luminaires-and-sensing-communication-modules-18.html (2026-11-02).
- National Institute for Occupational Safety and Health. NIOSH Noise: a 50-year timeline. https://www.cdc.gov/niosh/bulletin/2022/noise-50.html (2026-11-02).
- PCE Instruments. PCE-430. https://pce-instruments.com/eu/measuring-instruments/test-meters/sound-level-meter-noise-level-meter-pce-instruments-class-1-sound-level-meter-pce-430-det_5971611.htm (2026-11-02).
- Dasenic. ICS-43434 listing. https://dasenic.com/product/tdk-invensense-ics-43434-3491 (2026-11-02).
