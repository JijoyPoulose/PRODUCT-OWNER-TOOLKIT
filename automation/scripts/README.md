# Automation scripts

Both scripts use only the Python 3.9+ standard library. Copy them anywhere.

## `story_lint.py`: Definition of Ready gate

Checks a story for the role, want, benefit, Given/When/Then coverage, error paths, vague language, leftover template placeholders, title length, estimate, size, and dependencies. It scores the story out of 100. **A story passes at 70 or above with no errors.**

```bash
python story_lint.py story.md                       # human-readable
python story_lint.py story.md --format markdown     # for bot comments
python story_lint.py story.md --format json         # for pipelines
python story_lint.py story.md --strict              # exit 1 if not ready (CI)
```

**Hook it into any tool:**

| Tool | How |
|---|---|
| GitHub | `.github/workflows/story-quality-gate.yml` (included) |
| Jira | Automation rule → *Send web request* to a small endpoint that runs the script, or use the no-code recipe in `docs/automation-playbook.md` |
| Azure DevOps | Service hook → Azure Function → PATCH the work item with tag and comment |
| Anywhere | Pre-refinement: `for f in stories/*.md; do python story_lint.py "$f"; done` |

**Tune it:** edit `VAGUE_TERMS`, `GENERIC_ROLES`, `SEVERITY_WEIGHT` and `PASS_THRESHOLD` at the top of the file to match your team's DoR.

## `backlog_health.py`: flow and quality report

```bash
python backlog_health.py export.csv > report.md
python backlog_health.py export.csv --format json
python backlog_health.py export.csv --stale-days 60 --col-estimate "Custom field (Story Points)"
```

The report scores Freshness, Acceptance criteria, Estimation, Lead time and Right-sizing, then lists recommended actions and the oldest and oversized items. Metric definitions are in `docs/metrics.md`.

### Getting a CSV from GitHub

```bash
gh issue list --state all --limit 1000 \
  --json number,title,state,createdAt,closedAt,body \
  --jq '(["Number","Title","State","CreatedAt","ClosedAt","Body"]),
        (.[] | [.number,.title,.state,.createdAt,.closedAt,.body]) | @csv' > export.csv
```
