import sys
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "automation" / "scripts"))

import story_lint  # noqa: E402
import backlog_health  # noqa: E402


def rules(result):
    return {f.rule for f in result.findings}


class StoryLintTests(unittest.TestCase):
    def test_good_example_passes(self):
        r = story_lint.lint((ROOT / "examples/story-good.md").read_text())
        self.assertTrue(r.passed, r.findings)
        self.assertEqual(r.score, 100)

    def test_weak_example_fails_with_expected_rules(self):
        r = story_lint.lint((ROOT / "examples/story-weak.md").read_text())
        self.assertFalse(r.passed)
        self.assertTrue({"story.benefit", "ac.missing", "clarity.vague", "story.generic-role"} <= rules(r))

    def test_blank_template_is_not_ready(self):
        r = story_lint.lint((ROOT / "templates/user-story.md").read_text())
        self.assertIn("template.placeholder", rules(r))
        self.assertFalse(r.passed)

    def test_github_issue_form_body(self):
        body = (
            "# [Story] Export entry audit trail\n\n"
            "### Story\n\n**As a** compliance analyst\n**I want** to export the audit trail\n"
            "**So that** I can answer regulator requests in one day\n\n"
            "### Acceptance criteria\n\n```gherkin\nScenario: Export\n  Given an entry\n  When I export\n"
            "  Then a CSV downloads\n\nScenario: Error path\n  Given no entries\n  When I export\n"
            "  Then I see an error 'Nothing to export'\n```\n\n"
            "### Dependencies\n\nNone\n\n### Estimate (story points)\n\n13 (split me)\n"
        )
        r = story_lint.lint(body)
        self.assertIn("size.points", rules(r))
        self.assertNotIn("ready.estimate", rules(r))
        self.assertTrue(r.passed)

    def test_vague_terms_deduplicated(self):
        r = story_lint.lint("As a clerk I want X as appropriate so that Y")
        vague = next(f for f in r.findings if f.rule == "clarity.vague")
        self.assertIn("as appropriate", vague.message)
        self.assertNotIn("appropriate,", vague.message)


class BacklogHealthTests(unittest.TestCase):
    def test_parse_dates_across_tools(self):
        for raw in ["2026-01-05", "2026-01-05T10:00:00Z", "2026-01-05T10:00:00.123+00:00",
                    "05/Jan/26 10:00 AM", "01/05/2026"]:
            self.assertEqual(backlog_health.parse_date(raw), date(2026, 1, 5), raw)

    def test_column_autodetect(self):
        cols = backlog_health.resolve_columns(
            ["Work Item Id", "Title", "State", "Created Date", "Closed Date", "Effort"], {})
        self.assertEqual(cols["id"], "Work Item Id")
        self.assertEqual(cols["resolved"], "Closed Date")
        self.assertEqual(cols["estimate"], "Effort")

    def test_analyze_small_backlog(self):
        rows = [
            {"Key": "A-1", "Status": "Done", "Created": "2026-01-01", "Resolved": "2026-01-11",
             "Story Points": "3", "Description": "Given x When y Then z"},
            {"Key": "A-2", "Status": "Backlog", "Created": "2026-01-01", "Resolved": "",
             "Story Points": "", "Description": ""},
            {"Key": "A-3", "Status": "Ready", "Created": "2026-09-01", "Resolved": "",
             "Story Points": "13", "Description": "Given a When b Then c"},
        ]
        cols = backlog_health.resolve_columns(list(rows[0].keys()), {})
        m = backlog_health.analyze(rows, cols, date(2026, 9, 23), 90)
        self.assertEqual((m["open"], m["done"]), (2, 1))
        self.assertEqual(m["stale_count"], 1)
        self.assertEqual(m["ac_coverage_pct"], 50.0)
        self.assertEqual(m["lead_median"], 10)
        self.assertEqual(len(m["oversized"]), 1)
        self.assertTrue(m["actions"])


if __name__ == "__main__":
    unittest.main()
