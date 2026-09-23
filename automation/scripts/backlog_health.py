#!/usr/bin/env python3
"""
backlog_health.py: a flow and quality health report from any backlog CSV export.

Works with exports from Jira, Azure DevOps, GitHub, Linear, or a spreadsheet.
Column names are auto-detected (see docs/adapting.md) and can be overridden.

Usage:
    python backlog_health.py export.csv
    python backlog_health.py export.csv --format json
    python backlog_health.py export.csv --col-estimate "Custom field (Story Points)"
    python backlog_health.py export.csv --today 2026-09-23 --stale-days 60

Standard library only.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import statistics
import sys
from collections import Counter
from datetime import date, datetime

ALIASES = {
    "id": ["id", "key", "issue key", "work item id", "number", "issue id"],
    "title": ["title", "summary", "name"],
    "status": ["status", "state"],
    "type": ["type", "issue type", "work item type", "issuetype"],
    "created": ["created", "created date", "createdat", "created at", "date created"],
    "resolved": ["resolved", "closed date", "closedat", "closed at", "done date",
                 "resolved date", "completed at", "completed"],
    "estimate": ["story points", "estimate", "effort", "points", "story point estimate",
                 "custom field (story points)"],
    "acceptance": ["acceptance criteria", "description", "body", "microsoft.vsts.common.acceptancecriteria"],
}
DONE_STATES = {"done", "closed", "resolved", "completed", "released", "accepted", "removed"}
DATE_FORMATS = ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d %H:%M",
                "%Y-%m-%d %H:%M:%S", "%d/%b/%y %I:%M %p", "%d/%b/%y", "%m/%d/%Y",
                "%m/%d/%Y %I:%M:%S %p", "%m/%d/%Y %H:%M", "%d/%m/%Y"]


# -------------------------------------------------------------- parsing ---

def parse_date(value: str) -> date | None:
    v = (value or "").strip()
    if not v:
        return None
    v = re.sub(r"\.\d+", "", v)                 # drop fractional seconds
    v = re.sub(r"([+-]\d{2}):?(\d{2})$", "", v)  # drop tz offset
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(v, fmt).date()
        except ValueError:
            continue
    return None


def resolve_columns(headers: list[str], overrides: dict) -> dict:
    norm = {h.strip().lower(): h for h in headers}
    cols = {}
    for key, names in ALIASES.items():
        if overrides.get(key):
            cols[key] = overrides[key]
            continue
        cols[key] = next((norm[n] for n in names if n in norm), None)
    return cols


def pct(n: int, d: int) -> float:
    return round(100 * n / d, 1) if d else 0.0


def percentile(values: list[float], p: float) -> float | None:
    if not values:
        return None
    s = sorted(values)
    k = (len(s) - 1) * p
    lo, hi = int(k), min(int(k) + 1, len(s) - 1)
    return round(s[lo] + (s[hi] - s[lo]) * (k - lo), 1)


# -------------------------------------------------------------- analysis ---

def analyze(rows: list[dict], cols: dict, today: date, stale_days: int) -> dict:
    def get(row, key):
        c = cols.get(key)
        return (row.get(c) or "").strip() if c else ""

    items = []
    for r in rows:
        status = get(r, "status")
        resolved = parse_date(get(r, "resolved"))
        is_done = status.lower() in DONE_STATES or resolved is not None
        items.append({
            "id": get(r, "id"), "title": get(r, "title"), "status": status,
            "type": get(r, "type") or "Item", "created": parse_date(get(r, "created")),
            "resolved": resolved, "done": is_done,
            "estimate": get(r, "estimate"), "ac": get(r, "acceptance"),
        })

    open_items = [i for i in items if not i["done"]]
    done_items = [i for i in items if i["done"]]

    ages = [(today - i["created"]).days for i in open_items if i["created"]]
    stale = sorted([i for i in open_items if i["created"] and (today - i["created"]).days > stale_days],
                   key=lambda i: i["created"])
    lead = [(i["resolved"] - i["created"]).days for i in done_items
            if i["created"] and i["resolved"] and i["resolved"] >= i["created"]]

    has_ac = lambda i: bool(re.search(r"\bgiven\b.*\bthen\b", i["ac"], re.I | re.S))
    has_est = lambda i: bool(re.match(r"^\d+(\.\d+)?$", i["estimate"])) and float(i["estimate"]) > 0
    ac_ok = sum(has_ac(i) for i in open_items)
    est_ok = sum(has_est(i) for i in open_items)
    oversized = [i for i in open_items if has_est(i) and float(i["estimate"]) > 8]

    throughput = Counter(i["resolved"].strftime("%Y-%m") for i in done_items if i["resolved"])

    m = {
        "total": len(items), "open": len(open_items), "done": len(done_items),
        "by_status": dict(Counter(i["status"] or "(blank)" for i in open_items).most_common()),
        "by_type": dict(Counter(i["type"] for i in open_items).most_common()),
        "age_median": round(statistics.median(ages), 1) if ages else None,
        "age_p85": percentile(ages, 0.85),
        "stale_count": len(stale), "stale_pct": pct(len(stale), len(open_items)),
        "stale_top": [{"id": i["id"], "title": i["title"], "age": (today - i["created"]).days}
                      for i in stale[:10]],
        "ac_coverage_pct": pct(ac_ok, len(open_items)) if cols.get("acceptance") else None,
        "estimate_coverage_pct": pct(est_ok, len(open_items)) if cols.get("estimate") else None,
        "oversized": [{"id": i["id"], "title": i["title"], "estimate": i["estimate"]} for i in oversized],
        "lead_median": round(statistics.median(lead), 1) if lead else None,
        "lead_p85": percentile(lead, 0.85),
        "throughput_by_month": dict(sorted(throughput.items())),
    }
    m["health"] = score(m)
    m["actions"] = recommend(m, stale_days)
    return m


def score(m: dict) -> dict:
    """0–100 per dimension, averaged over the dimensions we have data for."""
    dims = {}
    if m["open"]:
        dims["Freshness"] = max(0, round(100 - m["stale_pct"] * 2))
    if m["ac_coverage_pct"] is not None:
        dims["Acceptance criteria"] = round(m["ac_coverage_pct"])
    if m["estimate_coverage_pct"] is not None:
        dims["Estimation"] = round(m["estimate_coverage_pct"])
    if m["lead_p85"] is not None:
        # 14 days or less at p85 = 100; fall off linearly to 0 at 90 days
        dims["Lead time"] = max(0, min(100, round(100 - (m["lead_p85"] - 14) * 100 / 76)))
    if m["open"]:
        dims["Right-sizing"] = max(0, round(100 - pct(len(m["oversized"]), m["open"]) * 3))
    overall = round(sum(dims.values()) / len(dims)) if dims else 0
    grade = "A" if overall >= 85 else "B" if overall >= 70 else "C" if overall >= 55 else "D"
    return {"overall": overall, "grade": grade, "dimensions": dims}


def recommend(m: dict, stale_days: int) -> list[str]:
    acts = []
    if m["ac_coverage_pct"] is not None and m["ac_coverage_pct"] < 90:
        acts.append(f"Acceptance criteria coverage is {m['ac_coverage_pct']}%. Run story_lint.py on the "
                    "top of the backlog, and turn on the automated story gate.")
    if m["stale_count"]:
        acts.append(f"{m['stale_count']} items are older than {stale_days} days. Hold a 30-minute "
                    "backlog purge: close, merge, or re-validate each one.")
    if m["estimate_coverage_pct"] is not None and m["estimate_coverage_pct"] < 80:
        acts.append(f"Only {m['estimate_coverage_pct']}% of open items are estimated. Add estimation "
                    "to the refinement agenda for the next two sprints' worth of work.")
    if m["oversized"]:
        acts.append(f"{len(m['oversized'])} items are estimated above 8 points. Split them using the "
                    "patterns in templates/user-story.md.")
    if m["lead_p85"] and m["lead_p85"] > 30:
        acts.append(f"85th-percentile lead time is {m['lead_p85']} days. Run a Flow Retro "
                    "(templates/retro-formats.md) to find where work waits.")
    if not acts:
        acts.append("The backlog is healthy. Keep the current cadence and review trends next sprint.")
    return acts


# --------------------------------------------------------------- output ---

def bar(v: float, width: int = 20) -> str:
    n = round(v / 100 * width)
    return "█" * n + "░" * (width - n)


def render_markdown(m: dict, source: str, today: date) -> str:
    h = m["health"]
    fmt = lambda v, s="": "n/a" if v is None else f"{v}{s}"
    out = [f"# Backlog Health Report",
           f"*Source: `{source}` · Generated {today.isoformat()}*", "",
           f"## Overall: **{h['overall']}/100 (Grade {h['grade']})**", "",
           "| Dimension | Score | |", "|---|---|---|"]
    for k, v in h["dimensions"].items():
        out.append(f"| {k} | {v} | `{bar(v)}` |")
    out += ["", "## Snapshot", "",
            "| Metric | Value |", "|---|---|",
            f"| Items (open / done) | {m['open']} / {m['done']} |",
            f"| Backlog age: median / p85 | {fmt(m['age_median'], ' d')} / {fmt(m['age_p85'], ' d')} |",
            f"| Stale items | {m['stale_count']} ({m['stale_pct']}%) |",
            f"| AC coverage (open) | {fmt(m['ac_coverage_pct'], '%')} |",
            f"| Estimate coverage (open) | {fmt(m['estimate_coverage_pct'], '%')} |",
            f"| Lead time: median / p85 | {fmt(m['lead_median'], ' d')} / {fmt(m['lead_p85'], ' d')} |",
            ""]
    if m["throughput_by_month"]:
        out += ["## Throughput by month", "", "| Month | Done |", "|---|---|"]
        out += [f"| {k} | {v} |" for k, v in m["throughput_by_month"].items()] + [""]
    out += ["## Recommended actions", ""] + [f"{n}. {a}" for n, a in enumerate(m["actions"], 1)] + [""]
    if m["stale_top"]:
        out += ["## Oldest open items", "", "| ID | Title | Age (days) |", "|---|---|---|"]
        out += [f"| {i['id']} | {i['title']} | {i['age']} |" for i in m["stale_top"]] + [""]
    if m["oversized"]:
        out += ["## Oversized items (> 8 pts)", "", "| ID | Title | Estimate |", "|---|---|---|"]
        out += [f"| {i['id']} | {i['title']} | {i['estimate']} |" for i in m["oversized"]] + [""]
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Backlog flow and quality health report from a CSV export.")
    p.add_argument("csv", help="Path to a CSV export")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p.add_argument("--today", help="Report date YYYY-MM-DD (default: today)")
    p.add_argument("--stale-days", type=int, default=90)
    for k in ALIASES:
        p.add_argument(f"--col-{k}", help=f"Column name to use for '{k}'")
    a = p.parse_args(argv)

    today = datetime.strptime(a.today, "%Y-%m-%d").date() if a.today else date.today()
    with open(a.csv, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        headers = reader.fieldnames or []

    cols = resolve_columns(headers, {k: getattr(a, f"col_{k}") for k in ALIASES})
    missing = [k for k in ("status", "created") if not cols.get(k)]
    if missing:
        print(f"Could not find column(s) for: {', '.join(missing)}. "
              f"Headers seen: {headers}. Use --col-<field> to map them.", file=sys.stderr)
        return 2

    m = analyze(rows, cols, today, a.stale_days)
    if a.format == "json":
        print(json.dumps({"columns": cols, **m}, indent=2, default=str))
    else:
        print(render_markdown(m, a.csv, today))
    return 0


if __name__ == "__main__":
    sys.exit(main())
