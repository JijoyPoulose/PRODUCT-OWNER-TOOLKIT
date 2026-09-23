# Backlog Health Report
*Source: `examples/sample-backlog.csv` · Generated 2026-09-23*

## Overall: **56/100 (Grade C)**

| Dimension | Score | |
|---|---|---|
| Freshness | 0 | `░░░░░░░░░░░░░░░░░░░░` |
| Acceptance criteria | 68 | `██████████████░░░░░░` |
| Estimation | 76 | `███████████████░░░░░` |
| Lead time | 61 | `████████████░░░░░░░░` |
| Right-sizing | 76 | `███████████████░░░░░` |

## Snapshot

| Metric | Value |
|---|---|
| Items (open / done) | 37 / 23 |
| Backlog age: median / p85 | 138 d / 223.0 d |
| Stale items | 25 (67.6%) |
| AC coverage (open) | 67.6% |
| Estimate coverage (open) | 75.7% |
| Lead time: median / p85 | 30 d / 43.9 d |

## Throughput by month

| Month | Done |
|---|---|
| 2026-01 | 1 |
| 2026-02 | 3 |
| 2026-03 | 1 |
| 2026-04 | 4 |
| 2026-05 | 3 |
| 2026-06 | 1 |
| 2026-07 | 2 |
| 2026-08 | 4 |
| 2026-09 | 4 |

## Recommended actions

1. Acceptance criteria coverage is 67.6%. Run story_lint.py on the top of the backlog, and turn on the automated story gate.
2. 25 items are older than 90 days. Hold a 30-minute backlog purge: close, merge, or re-validate each one.
3. Only 75.7% of open items are estimated. Add estimation to the refinement agenda for the next two sprints' worth of work.
4. 3 items are estimated above 8 points. Split them using the patterns in templates/user-story.md.
5. 85th-percentile lead time is 43.9 days. Run a Flow Retro (templates/retro-formats.md) to find where work waits.

## Oldest open items

| ID | Title | Age (days) |
|---|---|---|
| CUS-108 | Retry failed EDI transmissions | 257 |
| CUS-151 | Improve search (phase 2) | 250 |
| CUS-129 | Broker workload balancing | 248 |
| CUS-143 | Low-value shipment fast lane (phase 2) | 245 |
| CUS-140 | Role-based access for clerks (phase 2) | 225 |
| CUS-119 | Importer self-service portal | 223 |
| CUS-160 | Filing cutoff calendar (phase 2) | 223 |
| CUS-148 | Multi-currency duty calc (phase 2) | 218 |
| CUS-122 | Fix report | 217 |
| CUS-141 | Search entries by container number (phase 2) | 208 |

## Oversized items (> 8 pts)

| ID | Title | Estimate |
|---|---|---|
| CUS-133 | Duty estimate on quote screen (phase 2) | 13 |
| CUS-139 | Reconcile duties with invoicing (phase 2) | 13 |
| CUS-149 | Importer self-service portal (phase 2) | 13 |

