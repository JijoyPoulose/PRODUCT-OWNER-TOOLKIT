# Ceremony Playbook

Each ceremony has a **purpose, inputs, a timed agenda, and outputs**. If a ceremony isn't producing its outputs, fix it or drop it.

Timings assume a two-week sprint and a team of 5–9 people. Scale them in proportion for other setups.

---

## 1. Backlog refinement

**Purpose:** Get the next 1–2 sprints of work to meet the [Definition of Ready](definition-of-ready.md).
**When:** Mid-sprint, 60 minutes, once or twice per sprint. Aim to spend about 10% of team capacity on it.
**Who:** PO (runs it), developers, QA. Invite SMEs for specific items only.

**Inputs (the PO prepares these before the session)**
- [ ] Top 10–15 items ordered by priority
- [ ] `story_lint.py` run on each; the obvious gaps fixed beforehand
- [ ] Open questions noted on each item

| Time | Agenda item |
|---|---|
| 5 min | Context: sprint goal outlook and any priority changes since last time |
| 40 min | Walk items top-down: clarify, split, write or refine AC, identify dependencies, estimate |
| 10 min | Readiness check: which items meet DoR? Assign an owner and date to each open question |
| 5 min | Preview the next refinement's focus |

**Outputs:** 1.5–2 sprints of items meeting DoR · questions with owners · items labelled `ready`

---

## 2. Sprint planning

**Purpose:** Commit to a sprint goal and a plan for reaching it.
**When:** Day 1, up to 2 hours.
**Who:** The whole Scrum team.

**Inputs**
- [ ] Prioritized, *ready* backlog
- [ ] Team capacity (holidays, PTO, support rotation)
- [ ] Last sprint's throughput and carry-over
- [ ] Draft sprint goal from the PO

| Time | Agenda item |
|---|---|
| 10 min | Review: last sprint's results, carry-over, capacity |
| 15 min | PO proposes the sprint goal and explains why it matters now |
| 45 min | Team selects items to meet the goal, keeping load at 80% of capacity or less |
| 40 min | Team plans the *how*: tasks, pairing, risks |
| 10 min | Confirm the goal, then a confidence vote (1–5 fingers) |

### Sprint goal template

> **This sprint we will** [outcome],
> **so that** [who benefits / why now],
> **and we'll know we succeeded when** [observable, testable result].

*Example:* This sprint we will flag shipments missing invoices before cutoff, so that clerks can chase documents in time, and we'll know we succeeded when a flagged shipment appears in the queue in staging with notification under 5 minutes.

A good sprint goal is: ✅ one coherent outcome · ✅ achievable even if some items drop · ❌ not "complete stories 1–8"

**Outputs:** sprint goal · sprint backlog · identified risks

---

## 3. Sprint review

**Purpose:** Inspect the increment with stakeholders and adapt the backlog. It is **a working session, not a status presentation.**
**When:** Last day, 60 minutes.
**Who:** Scrum team plus invited stakeholders (see [stakeholder map](stakeholder-map.md)).

**Inputs**
- [ ] Working software in a demo environment. No slides of screenshots.
- [ ] Demo script: who demos which story, and the user scenario for each
- [ ] Current metrics (outcome and `backlog_health.py`)
- [ ] Specific questions for stakeholders

| Time | Agenda item |
|---|---|
| 5 min | PO: sprint goal, and whether it was met (be candid about what wasn't done) |
| 25 min | Team demos done work only, framed as user scenarios |
| 15 min | Stakeholder feedback, captured live as backlog items |
| 10 min | PO: roadmap and metric update, and what's likely next |
| 5 min | Confirm changes to backlog priority |

**Outputs:** feedback items added to the backlog · priority adjustments · stakeholder alignment on next steps

---

## 4. Retrospective

See [retro-formats.md](retro-formats.md).

## 5. Three Amigos (as needed)

**Purpose:** PO, developer and QA align on one complex story *before* refinement.
**When:** 15–30 minutes, for stories with business rules or edge cases.

1. The PO explains the intent and rules.
2. The developer raises feasibility and technical edge cases.
3. QA asks "what if…?" and drafts test scenarios.
4. Everyone leaves with the Given/When/Then written.

---

## Ceremony health check (review each PI)

| Ceremony | Producing its outputs? | Right people? | Right length? | Action |
|---|---|---|---|---|
| Refinement | | | | |
| Planning | | | | |
| Review | | | | |
| Retro | | | | |
