# UAT Plan & Traceability Matrix: [Release / Feature]

**Owner:** [PO] · **UAT window:** YYYY-MM-DD → YYYY-MM-DD · **Environment:** [UAT / staging URL]

> In regulated domains (customs, finance, health), *"How do you know it works, and who agreed?"* needs an answer that holds up in an audit. This template gives you one.

---

## Part A: Traceability matrix

Every requirement traces **forward** to what delivers it and what proves it. Every test traces **back** to a requirement.

| Req ID | Requirement (source) | Story / PR | Test case(s) | Test result | Defects | Sign-off |
|---|---|---|---|---|---|---|
| FR-01 | Flag shipments missing invoice 4h before cutoff (PRD §4) | STORY-123 / PR #45 | TC-01, TC-02 | ✅ Pass | — | J. Smith, 2026-10-02 |
| FR-02 | Remove from queue when invoice attached (PRD §4) | STORY-124 / PR #47 | TC-03 | ❌ Fail | BUG-88 | Pending |
| NFR-01 | Notification within 5 min (PRD §4 NFR) | STORY-123 | TC-04 (perf) | ✅ Pass | — | |
| REG-01 | Audit trail retained 7 years (regulation ref.) | STORY-130 | TC-09 | ⏳ Not run | — | |

### Coverage check (fill in before the UAT exit meeting)

| Check | Result |
|---|---|
| Requirements with ≥ 1 story | __ / __ |
| Requirements with ≥ 1 test case | __ / __ |
| Test cases linked to a requirement (no orphan tests) | __ / __ |
| Regulatory requirements passed | __ / __ (**must be 100%**) |

---

## Part B: UAT plan

### 1. Scope

| In scope | Out of scope |
|---|---|
| | |

### 2. Entry criteria (UAT does not start until these are met)

- [ ] All in-scope stories meet the Definition of Done
- [ ] System and regression tests passed; no open Sev-1 or Sev-2 defects
- [ ] UAT environment deployed with realistic, anonymized test data
- [ ] Testers trained and their access confirmed
- [ ] Test cases reviewed and approved by business owners

### 3. Participants

| Name | Role / business area | Scenarios assigned | Availability |
|---|---|---|---|
| | | | |

### 4. Test cases

| TC ID | Req ID | Scenario (business language) | Steps | Test data | Expected result | Actual | Pass/Fail | Tester | Date |
|---|---|---|---|---|---|---|---|---|---|
| TC-01 | FR-01 | Shipment with no invoice is flagged before cutoff | 1. Load shipment ETA < 24h, no invoice 2. Advance clock to cutoff − 4h | SHP-TEST-001 | Appears in "Missing documents" queue | | | | |

*Tip:* convert each story's Given/When/Then into a test case one-to-one. The acceptance criteria are already the test design.

### 5. Defect severity & handling

| Severity | Definition | Blocks go-live? | Response |
|---|---|---|---|
| Sev-1 Critical | Data loss, compliance breach, no workaround | Yes | Fix before exit |
| Sev-2 High | Core flow broken; a workaround exists but isn't sustainable | Yes (unless the PO formally accepts it) | Fix before exit |
| Sev-3 Medium | Non-core issue with an acceptable workaround | No | Next release |
| Sev-4 Low | Cosmetic | No | Backlog |

### 6. Exit criteria

- [ ] 100% of test cases executed
- [ ] ≥ 95% passed, and **100% of regulatory and Sev-1 scenarios passed**
- [ ] No open Sev-1 or Sev-2 defects (or formal risk acceptance logged in `decision-log.md`)
- [ ] Traceability coverage check complete
- [ ] Business sign-off recorded below

### 7. Sign-off

| Role | Name | Decision | Conditions / notes | Date |
|---|---|---|---|---|
| Business owner | | Approve · Approve with conditions · Reject | | |
| Compliance (if applicable) | | | | |
| Product Owner | | | | |
