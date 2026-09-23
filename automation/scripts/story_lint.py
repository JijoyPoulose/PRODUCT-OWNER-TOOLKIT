#!/usr/bin/env python3
"""
story_lint.py: check a user story against the Definition of Ready.

Tool-agnostic: it reads plain text or Markdown from a file, from stdin, or
from --text, so it works on stories from GitHub, Jira, Azure DevOps, Linear,
or a doc.

Usage:
    python story_lint.py story.md
    cat story.md | python story_lint.py -
    python story_lint.py --text "As a clerk I want..." --format json
    python story_lint.py story.md --format markdown --strict   # CI / bots

Exit codes: 0 = pass (or non-strict), 1 = fail in --strict mode, 2 = usage error.
Standard library only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict

# ---------------------------------------------------------------- rules ---

VAGUE_TERMS = [
    "fast", "quick", "quickly", "easy", "easily", "user-friendly", "user friendly",
    "intuitive", "etc", "and so on", "as appropriate", "as needed", "if possible",
    "should be able to", "seamless", "seamlessly", "robust", "efficient",
    "optimal", "flexible", "various", "appropriate", "properly", "tbd",
]
GENERIC_ROLES = {"user", "a user", "the user", "users", "someone", "person", "customer"}
PLACEHOLDER_RE = re.compile(r"\[(specific role|capability|measurable benefit|precondition|action|"
                            r"observable result|short, outcome-focused title)[^\]]*\]", re.I)

SEVERITY_WEIGHT = {"error": 20, "warning": 7, "info": 0}
PASS_THRESHOLD = 70


@dataclass
class Finding:
    rule: str
    severity: str  # error | warning | info
    message: str
    fix: str


@dataclass
class Result:
    score: int
    passed: bool
    title: str
    findings: list[Finding] = field(default_factory=list)
    stats: dict = field(default_factory=dict)


# -------------------------------------------------------------- helpers ---

def _strip_code_fences(text: str) -> str:
    """Keep fence content (Gherkin lives there) but drop the ``` markers."""
    return re.sub(r"^\s*```[a-zA-Z]*\s*$", "", text, flags=re.M)


def _title(text: str) -> str:
    for line in text.splitlines():
        s = line.strip()
        if s:
            return re.sub(r"^#+\s*", "", s)
    return ""


def _count(pattern: str, text: str) -> int:
    return len(re.findall(pattern, text, flags=re.I | re.M))


# ----------------------------------------------------------------- lint ---

def lint(raw: str) -> Result:
    text = _strip_code_fences(raw)
    # Ignore collapsible guidance blocks copied from the template
    text_body = re.sub(r"<details>.*?</details>", "", text, flags=re.S | re.I)
    lower = text_body.lower()
    findings: list[Finding] = []
    title = _title(text_body)

    # --- Story statement --------------------------------------------------
    role_m = re.search(r"\bas an?\*{0,2}\s+(.+?)(?:,|\n|\*{0,2}\s*i want)", text_body, re.I)
    if not role_m:
        findings.append(Finding("story.role", "error",
            "Missing 'As a <role>' statement.",
            "Start with who benefits: 'As a customs entry clerk…'."))
    else:
        role = re.sub(r"[\*\[\]_]", "", role_m.group(1)).strip().lower()
        if role in GENERIC_ROLES:
            findings.append(Finding("story.generic-role", "warning",
                f"Role '{role}' is too generic.",
                "Name the specific role or persona. It drives design and test decisions."))

    if not re.search(r"\bi want\b", lower):
        findings.append(Finding("story.want", "error",
            "Missing 'I want <capability>'.",
            "State the capability the role needs."))

    if not re.search(r"\bso that\b", lower):
        findings.append(Finding("story.benefit", "error",
            "Missing 'So that <benefit>'. The value is unstated.",
            "Add the outcome. If you can't, question whether the story is valuable."))

    # --- Acceptance criteria ---------------------------------------------
    givens = _count(r"^\s*(?:[-*]\s*)?(?:\*\*)?given\b", text_body)
    whens = _count(r"^\s*(?:[-*]\s*)?(?:\*\*)?when\b", text_body)
    thens = _count(r"^\s*(?:[-*]\s*)?(?:\*\*)?then\b", text_body)
    scenarios = _count(r"^\s*(?:[-*]\s*)?(?:\*\*)?scenario\b", text_body)
    ac_count = min(givens, whens, thens)

    if ac_count == 0:
        findings.append(Finding("ac.missing", "error",
            "No Given/When/Then acceptance criteria found.",
            "Add at least one scenario: Given <context>, When <action>, Then <result>."))
    else:
        if ac_count == 1:
            findings.append(Finding("ac.coverage", "warning",
                "Only one scenario. Edge cases and errors are probably missing.",
                "Add at least one edge-case and one error or validation scenario."))
        if not re.search(r"error|invalid|fail|reject|missing|exceed|denied|timeout", lower):
            findings.append(Finding("ac.negative", "warning",
                "No negative or error path described.",
                "Add a scenario for invalid input or failure, with the expected behaviour."))
        if scenarios > 8:
            findings.append(Finding("size.scenarios", "warning",
                f"{scenarios} scenarios. The story is likely too big.",
                "Split by workflow step, business rule, or data variation."))

    # --- Clarity ---------------------------------------------------------
    hits = sorted({t for t in VAGUE_TERMS
                   if re.search(rf"(?<![\w-]){re.escape(t)}(?![\w-])", lower)})
    hits = [h for h in hits if not any(h != o and h in o for o in hits)]  # keep longest phrase
    if hits:
        findings.append(Finding("clarity.vague", "warning",
            f"Vague terms: {', '.join(hits)}.",
            "Replace with measurable criteria (e.g. 'fast' → 'responds in < 2s at p95')."))

    if PLACEHOLDER_RE.search(text_body):
        findings.append(Finding("template.placeholder", "error",
            "Unfilled template placeholders remain.",
            "Replace every [bracketed] placeholder with real content."))

    if len(title) > 80:
        findings.append(Finding("title.length", "warning",
            f"Title is {len(title)} characters (max 80).",
            "Shorten it to the outcome; put the detail in the body."))

    # --- Readiness --------------------------------------------------------
    est_m = (re.search(r"(?:story\s*points?|estimate|points|effort)\s*[:=]\s*\*{0,2}\s*(\d+(?:\.\d+)?)", lower)
             # GitHub issue-form style: "### Estimate (story points)\n\n5"
             or re.search(r"^#+\s*estimate[^\n]*\n\s*\n?\s*(\d+(?:\.\d+)?)\b", lower, re.M))
    if not est_m:
        findings.append(Finding("ready.estimate", "warning",
            "No estimate found.",
            "Size it with the team (e.g. 'Story points: 3')."))
    elif float(est_m.group(1)) > 8:
        findings.append(Finding("size.points", "warning",
            f"Estimate of {est_m.group(1)} points is large for one sprint.",
            "Split it into stories of 5 points or less."))

    if not re.search(r"depend", lower):
        findings.append(Finding("ready.dependencies", "info",
            "Dependencies not mentioned.",
            "State 'Dependencies: none' explicitly, or list them with owners."))

    # --- Score ------------------------------------------------------------
    penalty = sum(SEVERITY_WEIGHT[f.severity] for f in findings)
    score = max(0, 100 - penalty)
    has_error = any(f.severity == "error" for f in findings)
    passed = score >= PASS_THRESHOLD and not has_error

    return Result(score=score, passed=passed, title=title, findings=findings,
                  stats={"scenarios": max(scenarios, ac_count), "given": givens,
                         "when": whens, "then": thens,
                         "estimate": est_m.group(1) if est_m else None})


# --------------------------------------------------------------- output ---

ICON = {"error": "❌", "warning": "⚠️", "info": "ℹ️"}


def render_text(r: Result) -> str:
    lines = [f"Story: {r.title or '(untitled)'}",
             f"Score: {r.score}/100  →  {'READY ✅' if r.passed else 'NOT READY ❌'}", ""]
    if not r.findings:
        lines.append("No issues found. Meets the automated Definition of Ready checks.")
    for f in r.findings:
        lines.append(f"{ICON[f.severity]} [{f.rule}] {f.message}\n     ↳ {f.fix}")
    return "\n".join(lines)


def render_markdown(r: Result, dor_link: str = "templates/definition-of-ready.md") -> str:
    status = "✅ **Ready**" if r.passed else "❌ **Not ready**"
    out = [f"### Story quality gate: {status} ({r.score}/100)", ""]
    if r.findings:
        out += ["| | Check | Finding | How to fix |", "|---|---|---|---|"]
        for f in r.findings:
            out.append(f"| {ICON[f.severity]} | `{f.rule}` | {f.message} | {f.fix} |")
    else:
        out.append("All automated Definition of Ready checks passed. 🎉")
    out += ["", f"<sub>Automated check against the [Definition of Ready]({dor_link}). "
                 "Human review still decides whether the story is ready.</sub>"]
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Lint a user story against the Definition of Ready.")
    p.add_argument("path", nargs="?", help="Story file, or '-' for stdin")
    p.add_argument("--text", help="Story text passed directly")
    p.add_argument("--format", choices=["text", "markdown", "json"], default="text")
    p.add_argument("--strict", action="store_true", help="Exit 1 when the story is not ready")
    p.add_argument("--dor-link", default="templates/definition-of-ready.md")
    a = p.parse_args(argv)

    if a.text is not None:
        raw = a.text
    elif a.path == "-":
        raw = sys.stdin.read()
    elif a.path:
        with open(a.path, encoding="utf-8") as fh:
            raw = fh.read()
    else:
        p.print_usage(sys.stderr)
        return 2

    r = lint(raw)
    if a.format == "json":
        print(json.dumps(asdict(r), indent=2, ensure_ascii=False))
    elif a.format == "markdown":
        print(render_markdown(r, a.dor_link))
    else:
        print(render_text(r))
    return 1 if (a.strict and not r.passed) else 0


if __name__ == "__main__":
    sys.exit(main())
