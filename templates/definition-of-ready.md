# Definition of Ready (DoR)

A story is **Ready** when the team can start it tomorrow without needing to ask the PO a blocking question.

> ⚙️ Items marked **[auto]** are checked by `automation/scripts/story_lint.py` and the story quality gate.

## Story

- [ ] **[auto]** Written in *As a / I want / So that* form, with a specific role
- [ ] **[auto]** Has a "so that" stating the benefit
- [ ] **[auto]** Title is concise (≤ 80 characters) and outcome-focused
- [ ] Linked to a parent epic or feature and an objective
- [ ] Passes the INVEST check

## Acceptance criteria

- [ ] **[auto]** At least one Given/When/Then scenario
- [ ] **[auto]** No vague words ("fast", "user-friendly", "etc.", "should be able to", "as appropriate")
- [ ] Covers the happy path, at least one edge case, and error handling
- [ ] Each criterion is testable pass/fail

## Readiness

- [ ] **[auto]** Estimated by the team
- [ ] Dependencies identified, with owners and dates
- [ ] UX or mockups attached if there is a UI change
- [ ] Test data needs identified
- [ ] Non-functional requirements stated (or explicitly "none")
- [ ] Reviewed by the Three Amigos (PO + Dev + QA) if rules or edge cases exist

## When a story isn't ready

It stays out of the sprint. It gets the label `needs-refinement` and goes on the next refinement agenda. **No exceptions for "urgent" work.** Urgent work gets a fast refinement, not skipped refinement.

---

*Tailor this list. Remove items your team never fails on, and add ones that caused your last three escaped defects.*
