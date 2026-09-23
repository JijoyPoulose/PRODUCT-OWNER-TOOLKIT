# Adapting to Your Ecosystem

The toolkit depends on **concepts**, not on a vendor's tool. Map the concepts to your tool once, and every template and script works.

## Concept → tool mapping

| Toolkit concept | GitHub | Jira | Azure DevOps | Linear | Spreadsheet |
|---|---|---|---|---|---|
| Epic / Feature | Issue + `epic` label or parent issue | Epic | Feature / Epic | Project | Row with Type = Epic |
| Story | Issue (Story form) | Story | User Story / PBI | Issue | Row |
| Acceptance criteria | Issue body section | Description or custom field | Acceptance Criteria field | Description | Column |
| Estimate | Projects "Estimate" field | Story Points | Story Points / Effort | Estimate | Column |
| Status | Projects "Status" field | Workflow status | State | Status | Column |
| Sprint / Iteration | Projects "Iteration" field | Sprint | Iteration Path | Cycle | Column |
| PI / Quarter | Milestone | Fix Version or label | Area/Iteration | Initiative | Column |
| Quality gate automation | GitHub Actions | Jira Automation | Pipelines + Service Hooks | Webhooks + API | Formulas or macros |

## Getting data into the scripts

`backlog_health.py` reads any CSV. It recognizes common column names automatically, and you can override them with flags.

| Script field | Auto-detected headers |
|---|---|
| `id` | ID, Key, Issue key, Work Item Id, Number |
| `title` | Title, Summary, Name |
| `status` | Status, State |
| `type` | Type, Issue Type, Work Item Type |
| `created` | Created, Created Date, CreatedAt |
| `resolved` | Resolved, Closed Date, ClosedAt, Done Date |
| `estimate` | Story Points, Estimate, Effort, Points |
| `acceptance` | Acceptance Criteria, Description, Body |

**Exporting:**

- **Jira:** Filters → Export → CSV (all fields)
- **Azure DevOps:** Query → Open in Excel or Export to CSV
- **GitHub:** `gh issue list --json number,title,state,createdAt,closedAt,body,labels --limit 500`, converted to CSV (see `automation/scripts/README.md`)
- **Linear:** Settings → Import/Export → Export CSV

## Adoption path (recommended)

| Week | Step | Effort |
|---|---|---|
| 1 | Adopt the story template and DoR. Lint stories manually before refinement. | Low |
| 2 | Add the DoD to the PR or ticket-close checklist. | Low |
| 3 | Turn on the automated story gate (GitHub Action, Jira rule, or ADO hook). | Medium |
| 4 | Run the backlog health report every sprint and review it in the retro. | Low |
| 6+ | Add PRDs for epics, a decision log, and PI planning templates. | Medium |

Start with the gates that hurt most. For most teams, that is acceptance criteria quality.
