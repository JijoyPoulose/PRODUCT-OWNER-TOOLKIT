# PI Planning Kit

Templates for a SAFe Program Increment (usually 8–12 weeks: 4–5 sprints plus an IP sprint). They work equally well for quarterly planning outside SAFe.

## 1. Pre-PI readiness checklist (2–3 weeks before)

- [ ] Top 10 features ranked by WSJF and shared with teams
- [ ] Each feature has a benefit hypothesis and acceptance criteria
- [ ] Team capacity calculated (see §4)
- [ ] Known dependencies and architectural runway reviewed
- [ ] Business context and vision briefing prepared
- [ ] Logistics set: agenda, board, rooms or remote tools

## 2. Feature brief (one per feature)

| Field | Content |
|---|---|
| Feature | |
| Benefit hypothesis | *We believe [feature] will result in [outcome]. We'll know when [metric].* |
| Acceptance criteria | |
| WSJF | BV __ + TC __ + RR/OE __ = CoD __ ÷ Size __ = **__** |
| Dependencies | |
| NFRs | |

## 3. Team PI objectives

| # | Objective (SMART) | Business value (1–10) | Committed / Uncommitted | Actual value (end of PI) |
|---|---|---|---|---|
| 1 | | | Committed | |
| 2 | | | Committed | |
| 3 | | | Uncommitted | |

**PI Predictability** = Σ actual ÷ Σ planned (committed only). Target: 80–100%.

## 4. Capacity worksheet

| Sprint | Team members | Days available | PTO / holidays | Normalized capacity (pts) | Load (pts) | Load % |
|---|---|---|---|---|---|---|
| S1 | | | | | | |
| S2 | | | | | | |
| S3 | | | | | | |
| S4 | | | | | | |
| IP | | | | *(innovation / planning)* | | |

Plan to **80% or less of capacity**. The buffer absorbs unplanned work.

## 5. Program board (text version)

| | S1 | S2 | S3 | S4 | IP |
|---|---|---|---|---|---|
| **Milestones** | | | | | |
| **Team A** | F-101 | F-101 → | F-104 | | |
| **Team B** | | F-102 🔗 A:S3 | | F-105 | |
| **Shared services** | | | | | |

🔗 = dependency: `F-xxx 🔗 Team:Sprint` means this feature depends on that team delivering in that sprint.

## 6. Risk board (ROAM)

| Risk | Owner | ROAM | Action |
|---|---|---|---|
| | | Resolved · Owned · Accepted · Mitigated | |

## 7. Confidence vote

On a scale of 1 to 5, each team votes, then the program votes. Anything below 3 triggers a re-plan of the concern before commitment.
