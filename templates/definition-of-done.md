# Definition of Done (DoD)

**Done** means it's potentially shippable. It is not "dev complete" or "done except testing."

## Story level

- [ ] All acceptance criteria pass and are demonstrated to the PO
- [ ] Code peer-reviewed and merged to the main branch
- [ ] Automated tests written and passing (unit and, where relevant, integration)
- [ ] No new critical or high static-analysis or security findings
- [ ] Non-functional requirements verified (performance, security, accessibility)
- [ ] Documentation updated (user-facing, API, runbook, as relevant)
- [ ] Story linked to its PR or commits (traceability)
- [ ] PO accepted

## Sprint / increment level

- [ ] All committed stories meet story-level DoD
- [ ] Regression suite passing
- [ ] Increment deployed to a staging or test environment
- [ ] Release notes drafted

## Release level

- [ ] UAT sign-off (where required)
- [ ] No open Sev-1 or Sev-2 defects
- [ ] Rollback plan documented and tested
- [ ] Support, operations, and stakeholders briefed
- [ ] Monitoring and alerts in place for new functionality
- [ ] Audit or compliance evidence captured (regulated domains)

---

> ⚙️ The story-level list is also in `.github/PULL_REQUEST_TEMPLATE.md`, so it's checked at merge time.
