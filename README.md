# PO Toolkit

**A tool-agnostic operating kit for Product Owners. It puts quality and flow efficiency first, and the automation checks them for you.**

Most PO templates are static documents that go stale in a wiki. This toolkit treats product ownership as a **system**, made of four parts:

1. **Standards.** Templates that define what "good" looks like (PRD, story, DoR, DoD).
2. **Gates.** Quality checkpoints at each stage of the lifecycle, so defects are caught at the story, not in UAT.
3. **Automation.** Scripts and workflows that enforce the gates, so humans don't have to police them.
4. **Feedback.** Flow and quality metrics that show whether the system is working.

It runs in any ecosystem: GitHub, Jira, Azure DevOps, Linear, or a spreadsheet. The standards are plain Markdown, and the automation reads plain CSV exports.

---

## Who this is for

- Product Owners and BSAs who want repeatable, auditable backlog quality
- Teams moving to SAFe / Scrum who need a starter operating model
- Hiring managers who want to see how I think about product ownership

## What's inside

| Area | What you get | Why it matters |
|---|---|---|
| [`docs/operating-model.md`](docs/operating-model.md) | Lifecycle from idea to value, with a quality gate at each stage | One shared definition of "how work flows here" |
| [`docs/adapting.md`](docs/adapting.md) | Field mapping for GitHub, Jira, Azure DevOps, Linear | Adopt in any tool in under an hour |
| [`docs/metrics.md`](docs/metrics.md) | Flow and quality metrics with formulas and targets | Manage the system, not the people |
| [`docs/automation-playbook.md`](docs/automation-playbook.md) | What to automate, in priority order, per tool | Put effort where it saves the most time |
| [`templates/`](templates) | PRD, user story, DoR, DoD, PI planning, retros, decision log, release notes | A consistent, reviewable standard |
| [`automation/`](automation) | `story_lint.py`, `backlog_health.py`, GitHub issue forms and Actions | Quality gates that run themselves |
| [`examples/`](examples) | Sample backlog export and a fully worked story | See it in action before adopting |

## Quick start (5 minutes)

```bash
git clone https://github.com/<you>/po-toolkit.git
cd po-toolkit

# 1. Lint a user story against the quality standard
python automation/scripts/story_lint.py examples/story-good.md
python automation/scripts/story_lint.py examples/story-weak.md

# 2. Run a health check on a backlog export (from Jira, ADO, GitHub, or any CSV)
python automation/scripts/backlog_health.py examples/sample-backlog.csv
```

No dependencies. Python 3.9+ standard library only.

To use it on GitHub, copy `.github/` into your repo. Every new story issue is then checked automatically, and the result is posted as a comment.

## Design principles

1. **Quality is built in, not inspected in.** Every gate sits as early as possible. A missing acceptance criterion costs minutes at refinement and days at UAT.
2. **Automate the checking, not the thinking.** Scripts catch structural gaps. Humans judge value and trade-offs.
3. **Tool-agnostic by default.** Standards live in Markdown, and data is exchanged as CSV. Nothing is locked to a vendor.
4. **Small batches, fast feedback.** Stories are sized to finish within a sprint, and metrics are reviewed every sprint.
5. **Everything is traceable.** Each story links to an objective, and each decision is logged with its rationale.

## Roadmap

- [x] Core templates and operating model
- [x] Story linter and backlog health report
- [x] GitHub issue forms and quality-gate workflow
- [ ] Jira Automation and Azure DevOps pipeline equivalents (exportable rules)
- [ ] Metrics dashboard (static HTML generated from CSV)
- [ ] WSJF/RICE scoring integration (see the companion repo, *feature-prioritization-calculator*)

## Author

**Jijoy Poulose**, Business Systems Analyst / Product Owner. SAFe Scrum Master, SAFe PI Planning, and SAFe Agile Software Delivery certified; CSPO in progress.
[jijoypoulose.com](https://jijoypoulose.com) · [LinkedIn](https://linkedin.com/in/jijoypoulose)

## License

MIT. Use it, fork it, adapt it to your team.
