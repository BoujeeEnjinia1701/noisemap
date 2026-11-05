---
doc_id: NSM-URS-001
title: NoiseMap user requirements
project: NoiseMap
doc_type: User requirements
version: "0.1"
status: Draft
date: '2026-11-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-11-02'
  author: Amish Chadha
  change: First issue (kit 1.8 pipeline); drawn from the users and context in NSM-PRB-001 and the existing requirements
---

# NoiseMap user requirements

What the people who would live with, buy, fit or study the node need, written from their side. The product requirements that meet these needs are in the product requirements (`03-requirements.md`, NSM-PRS-001) and the links to evidence are in the traceability matrix (`03b-traceability.md`). Sources are the user types and stakeholders in NSM-PRB-001 (Tables 1 and 2). No co-design partner has yet reviewed these needs (NSM-PRB-001 open items), so all priorities are proposals, "Proposed, awaiting Amish".

Table 1. User requirements.

| ID | Category | Title | Need | Priority | Source |
| --- | --- | --- | --- | --- | --- |
| UR-001 | Regulatory | No eavesdropping | The people on the street can be sure no audio of them is stored or leaves the device; only sound levels do. | High | Residents and associations; venue operators (PRB Table 1) |
| UR-002 | Performance | Night-time evidence | A continuous record of how loud it was and when, at the street, in a form a council or licensing panel can use (LAeq, peaks, a low-frequency measure). | High | Residents; city environmental health team; licensing authority |
| UR-003 | Performance | Credible accuracy | Readings close enough to a class 1 reference meter to be trusted at a hearing, with the uncertainty stated. | High | City environmental health team; licensing authority; researchers |
| UR-004 | Performance | Quiet to loud | The node resolves a quiet residential night and a loud motorcycle or siren. | High | Residents; city environmental health team |
| UR-005 | Performance | Bass from venues | Levels that reflect low-frequency amplified music as well as A-weighted traffic noise. | Medium | Residents; licensing authority; venue operators |
| UR-006 | Performance | Events can be dated | Each record carries a trusted time so a complaint can be matched to a level. | Medium | Licensing authority; residents |
| UR-007 | Deployment and assembly | No power at the pole | The node runs for years without mains power or visits, through dull weeks. | High | Pole or asset owner; city environmental health team |
| UR-008 | Deployment and assembly | Clamp on, nothing drilled | Two trained people fit it to an existing pole in one short visit with no drilling, welding or wiring into the pole. | High | Pole or asset owner |
| UR-009 | Safety | Light and wind-proof | The load on the pole stays small, the node stays put in a storm, and a falling part cannot land on a passer-by. | High | Pole or asset owner; public |
| UR-010 | Environment and durability | Outdoors for years | The node works in sun, rain, dust and -20 to +50 degrees C for about five years. | Medium | City environmental health team; pole owner |
| UR-011 | Usability | Know which data are spoiled | Records made in wind or heavy rain are marked so analysts can leave them out. | Medium | Researchers; city environmental health team |
| UR-012 | Maintenance | Quick field check | A technician can check the node against a calibrator in a few minutes at the pole. | Medium | City environmental health team; researchers |
| UR-013 | Regulatory | Shares the airwaves fairly | Radio use stays within the licence-free band rules and shared network fair use. | Medium | City environmental health team; network operators |
| UR-014 | Cost | Cheap enough for many streets | The parts for one node are affordable for a residents' group or a small city team. | High | Residents' associations; city environmental health team |
| UR-015 | Regulatory | Open and checkable | Hardware, firmware, calibration method and data format are published so anyone can audit what is measured. | High | Residents; researchers; city teams |
| UR-016 | Regulatory | Public notice | Passers-by can read on the pole what is measured and where to find the design. | Medium | Residents; venue operators; pole owner |

Categories: deployment and assembly, performance, usability, safety, environment and durability, logistics, maintenance, cost, regulatory. Priorities: High, Medium, Low.
