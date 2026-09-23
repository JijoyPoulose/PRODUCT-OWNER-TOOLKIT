# Automation Playbook

Automate in order of **time saved × errors prevented ÷ effort**. Start at the top.

| # | Automation | Saves | Effort | GitHub | Jira | Azure DevOps |
|---|---|---|---|---|---|---|
| 1 | **Structured intake** (forms with required fields) | Triage back-and-forth | Low | Issue forms (`.github/ISSUE_TEMPLATE`) | Request types / required fields | Work item templates + required rules |
| 2 | **Story quality gate** (AC, format, size) | Refinement churn, UAT defects | Low | `story-quality-gate.yml` Action | Automation rule: on create → validate → comment | Service hook → Azure Function running `story_lint.py` |
| 3 | **Auto-labeling / routing** | Manual sorting | Low | Labeler Action or issue form labels | Automation: if component = X → assign | Rules on work item type |
| 4 | **Definition of Done checklist on PRs** | Missed steps before merge | Low | `PULL_REQUEST_TEMPLATE.md` | Checklist plugin / sub-tasks | PR templates + branch policies |
| 5 | **Stale item sweep** | Backlog bloat | Low | `actions/stale` | Scheduled rule: untouched 90 days → flag | Scheduled query + alert |
| 6 | **Status sync** (PR merged → story done) | Manual status updates | Medium | Closing keywords (`Fixes #12`) | Dev integration (smart commits) | `AB#123` in commits |
| 7 | **Release notes generation** | Hours per release | Medium | `gh release create --generate-notes` | Release hub / version report | Release pipeline task |
| 8 | **Sprint health report** | Manual metric pulls | Medium | Scheduled Action + `backlog_health.py` | Scheduled export + script | Analytics view + script |
| 9 | **Stakeholder digest** | Status meetings | Medium | Scheduled Action → email or Slack | Automation → Slack/email | Power Automate |

## Jira Automation: story quality gate (recipe)

```
Trigger:   Issue created (Issue type = Story)
Condition: Description does NOT contain "Given" OR does NOT contain "Then"
Action:    Add comment:
           "⚠️ This story is missing Given/When/Then acceptance criteria.
            It won't pass Definition of Ready. Template: <link>"
Action:    Add label: needs-refinement
```

## Azure DevOps: story quality gate (recipe)

1. Project settings → Service hooks → *Work item created* → Web Hook
2. Point the hook at an Azure Function (or any endpoint) that runs `story_lint.py` on the Acceptance Criteria field
3. The function PATCHes the work item: it adds tag `needs-refinement` and a discussion comment with the findings

## Guardrails

- **Automations comment and label. They don't block or close.** People keep the final decision.
- **Every automated message links to the standard** it enforces, so it teaches rather than nags.
- **Review automations quarterly.** Remove any that the team ignores.
