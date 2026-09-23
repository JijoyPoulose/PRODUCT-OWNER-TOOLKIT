# [Short, outcome-focused title]

**Parent:** [Epic / Feature link] · **Objective:** [PI objective / OKR]

## Story

**As a** [specific role, not "user"]
**I want** [capability]
**So that** [measurable benefit]

## Context

Why this matters, a link to the PRD, and any data or screenshots.

## Acceptance criteria

```gherkin
Scenario: [Happy path]
  Given [precondition]
  When  [action]
  Then  [observable result]

Scenario: [Edge case / business rule]
  Given [precondition]
  When  [action]
  Then  [observable result]

Scenario: [Error / validation]
  Given [precondition]
  When  [invalid action]
  Then  [clear error and no side effects]
```

## Business rules

- BR-1:

## Out of scope

-

## Non-functional notes

Performance, security, audit, and accessibility requirements, if any apply.

## Dependencies

- [ ] None, or: [team / system / item] with owner and date

## Estimate

Story points: __

---

<details>
<summary><b>INVEST check</b> (tick before refinement)</summary>

- [ ] **I**ndependent: can be delivered without waiting on another story
- [ ] **N**egotiable: describes the need, not a locked design
- [ ] **V**aluable: a user or the business would notice if it shipped
- [ ] **E**stimable: the team understands it well enough to size it
- [ ] **S**mall: fits in one sprint (ideally 1–3 days)
- [ ] **T**estable: every AC can be verified pass/fail

</details>

<details>
<summary><b>Splitting patterns</b> (if it's too big)</summary>

| Pattern | Example |
|---|---|
| Workflow steps | Submit → Review → Approve as separate stories |
| Business rule variations | Domestic vs. international |
| Data variations | Single item vs. bulk upload |
| Interfaces | Web first, API second |
| Happy path first | Core flow, then edge cases |
| Defer performance | Make it work, then make it fast |

</details>
