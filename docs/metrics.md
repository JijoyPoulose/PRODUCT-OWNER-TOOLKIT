# Flow & Quality Metrics

Measure the **system**, not individuals. Review these every sprint, and look at trends over three or more sprints before drawing conclusions.

## Flow (efficiency)

| Metric | Formula | Healthy signal | Warning sign |
|---|---|---|---|
| **Cycle time** | Resolved date − In Progress date | Stable or falling; 85th percentile < 1 sprint | Long tail of stories > 2 sprints |
| **Lead time** | Resolved date − Created date | Predictable | Grows every sprint |
| **Throughput** | Items done per sprint | Stable ±20% | Swings wildly |
| **WIP** | Items in progress at once | ≤ team size | > 1.5 × team size |
| **Backlog age** | Today − Created, for open items | Top 20 items < 90 days | Stale items crowding the top |
| **Flow efficiency** | Active time ÷ total cycle time | > 40% | < 15% (work is mostly waiting) |

## Quality

| Metric | Formula | Healthy signal | Warning sign |
|---|---|---|---|
| **Ready rate** | Stories passing DoR at refinement ÷ total | > 90% | < 70% |
| **AC coverage** | Stories with acceptance criteria ÷ total | 100% of sprint-committed stories | Anything below 100% |
| **Escaped defects** | Production defects per release | Falling | Rising |
| **Rework rate** | Stories reopened ÷ stories done | < 5% | > 15% |
| **Estimate coverage** | Estimated stories ÷ sprint-ready stories | 100% | Unestimated work in sprint |

## Predictability (SAFe)

| Metric | Formula | Target |
|---|---|---|
| **PI Predictability** | Actual business value ÷ planned business value | 80–100% |
| **Sprint goal hit rate** | Sprints meeting their goal ÷ total | > 80% |

## How `backlog_health.py` computes these

The script calculates these from a CSV export: backlog age, AC coverage, estimate coverage, lead time (median and 85th percentile), throughput by month, and the count of stale items. It then outputs a scored report with recommended actions. See `automation/scripts/README.md`.

## Anti-patterns

- **Velocity as a target.** It inflates estimates. Use it for forecasting only.
- **Per-person metrics.** They destroy collaboration. Keep everything at team level.
- **Metrics without actions.** Every metric in a retro should lead to a decision, even if the decision is "no change."
