# User Story Map: [Product / Epic]

**Persona:** [link to persona] · **Goal:** [what the user is trying to achieve end to end]

A story map arranges the backlog along the **user's journey** instead of as a flat list. It helps you:

- see gaps in the journey
- define a thin, end-to-end MVP
- plan releases that each deliver usable value

## How to build it (a 60–90 minute workshop)

1. **Backbone:** list the user's activities left to right, in the order they happen.
2. **Steps:** under each activity, add the user tasks.
3. **Details:** under each task, add stories, with the most essential at the top.
4. **Slice:** draw horizontal lines. Everything above the first line is the **walking skeleton**: the thinnest version that works end to end.
5. **Validate:** walk the map as the persona and tell their story. Look for gaps.

## Map

| | **Activity 1:** Receive shipment data | **Activity 2:** Validate documents | **Activity 3:** File entry | **Activity 4:** Release & notify |
|---|---|---|---|---|
| **Steps** | Import manifest · View shipment | Check invoice · Check classification | Calculate duties · Submit | Receive release · Notify importer |
| **🦴 Release 1: Walking skeleton** | Manual upload of one manifest | Flag missing invoice | Submit a single entry | Show release status |
| **Release 2: Usable** | Bulk upload | Invoice OCR | Auto duty calculation | Email notification |
| **Release 3: Delightful** | Carrier API sync | HS code suggestions | Batch filing | Importer self-service portal |

*The example is generic cross-border filing. Replace it with your domain.*

## Release slices

| Release | Outcome it proves | Success metric | Target |
|---|---|---|---|
| 1: Walking skeleton | The end-to-end flow works for one shipment | One shipment filed through the new flow | |
| 2: Usable | Clerks can use it for daily volume | ≥ 80% of shipments go through the new flow | |
| 3: Delightful | Measurable efficiency gain | −30% handling time per entry | |

## Gaps and questions found while walking the map

- [ ]
