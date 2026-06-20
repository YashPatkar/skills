#!/usr/bin/env python3
"""impact-log driver — local-only structured career history.

All data stays on this machine. Nothing is ever sent anywhere.

Storage: $IMPACT_LOG_HOME (if set) else ~/.impact-log/logs.json

The AI (Claude) does the analysis and builds an entry; this script only
persists, searches, and reports. Commands:

  add        read a JSON entry (object) from stdin, assign id+date, save
  recent     show the last N entries (default 10)
  search     full-text search across all fields
  stats      totals, category breakdown, estimated time saved
  export     write a resume-ready impact-report.md
  path       print the storage file path

Run `python impact_log.py <command> -h` for per-command flags.
"""
import argparse
import json
import os
import sys
from datetime import date as _date
from pathlib import Path

CATEGORIES = [
    "automation", "ai", "performance", "deployment", "frontend",
    "backend", "security", "bugfix", "devops", "database",
    "architecture", "other",
]


def store_path() -> Path:
    home = os.environ.get("IMPACT_LOG_HOME")
    base = Path(home) if home else Path.home() / ".impact-log"
    return base / "logs.json"


def load() -> list:
    p = store_path()
    if not p.exists():
        return []
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.exit(f"error: {p} is corrupt JSON ({e}). Fix or remove it.")
    if not isinstance(data, list):
        sys.exit(f"error: {p} must contain a JSON array.")
    return data


def save(entries: list) -> None:
    p = store_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(entries, indent=2, ensure_ascii=False), encoding="utf-8")


def next_id(entries: list, day: str) -> str:
    n = sum(1 for e in entries if e.get("date") == day) + 1
    return f"{day}-{n:03d}"


def normalize_category(cat: str) -> str:
    c = (cat or "other").strip().lower()
    return c if c in CATEGORIES else "other"


def cmd_add(args) -> None:
    if args.file:
        # utf-8-sig tolerates a BOM (PowerShell's Out-File -Encoding utf8 adds one)
        raw = Path(args.file).read_text(encoding="utf-8-sig")
    else:
        raw = sys.stdin.read()
    if not raw.strip():
        sys.exit("error: no entry given. Use --file <path> (preferred) or pipe JSON on stdin.")
    try:
        entry = json.loads(raw)
    except json.JSONDecodeError as e:
        sys.exit(f"error: input is not valid JSON ({e}).")
    if not isinstance(entry, dict):
        sys.exit("error: entry must be a single JSON object.")

    if not entry.get("title"):
        sys.exit("error: entry needs a non-empty 'title'.")

    entries = load()
    day = entry.get("date") or _date.today().isoformat()
    entry["date"] = day
    entry["category"] = normalize_category(entry.get("category"))
    entry.setdefault("problem", "")
    entry.setdefault("solution", "")
    entry.setdefault("impact", "")
    entry.setdefault("tech", [])
    if not entry.get("id"):
        entry["id"] = next_id(entries, day)

    entries.append(entry)
    save(entries)
    print(f"saved {entry['id']}  \"{entry['title']}\"  [{entry['category']}]")


def _fmt(e: dict) -> str:
    tech = ", ".join(e.get("tech", []))
    conf = e.get("confidence")
    conf_s = f"  conf={conf}" if conf is not None else ""
    lines = [
        f"# {e.get('id','?')}  {e.get('date','?')}  [{e.get('category','?')}]{conf_s}",
        f"  {e.get('title','(untitled)')}",
    ]
    if e.get("problem"):
        lines.append(f"  Problem : {e['problem']}")
    if e.get("solution"):
        lines.append(f"  Solution: {e['solution']}")
    if e.get("impact"):
        lines.append(f"  Impact  : {e['impact']}")
    if tech:
        lines.append(f"  Tech    : {tech}")
    return "\n".join(lines)


def cmd_recent(args) -> None:
    entries = load()
    if not entries:
        print("No entries yet. Run an impact-log capture to create one.")
        return
    for e in entries[-args.count:]:
        print(_fmt(e))
        print()


def cmd_search(args) -> None:
    q = args.query.lower()
    entries = load()
    hits = []
    for e in entries:
        hay = " ".join([
            str(e.get("title", "")),
            str(e.get("problem", "")),
            str(e.get("solution", "")),
            str(e.get("impact", "")),
            str(e.get("category", "")),
            " ".join(e.get("tech", [])),
            " ".join(e.get("tags", [])),
        ]).lower()
        if q in hay:
            hits.append(e)
    if not hits:
        print(f"No entries match '{args.query}'.")
        return
    print(f"{len(hits)} match(es) for '{args.query}':\n")
    for e in hits:
        print(_fmt(e))
        print()


def cmd_stats(args) -> None:
    entries = load()
    if not entries:
        print("No entries yet.")
        return
    cats = {}
    hours = 0.0
    for e in entries:
        c = e.get("category", "other")
        cats[c] = cats.get(c, 0) + 1
        h = e.get("time_saved_hours")
        if isinstance(h, (int, float)):
            hours += h
    print(f"Total Entries: {len(entries)}\n")
    print("Categories:")
    for c, n in sorted(cats.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"  {c.capitalize()}: {n}")
    print()
    if hours > 0:
        print(f"Estimated Time Saved:\n  {hours:g} hours")
    else:
        print("Estimated Time Saved:\n  (no time_saved_hours recorded yet)")


def cmd_export(args) -> None:
    entries = load()
    if not entries:
        sys.exit("No entries to export.")
    out = Path(args.output)
    by_cat = {}
    for e in entries:
        by_cat.setdefault(e.get("category", "other"), []).append(e)

    md = ["# Impact Report", "", f"_{len(entries)} accomplishments captured._", ""]
    for cat in sorted(by_cat):
        md.append(f"## {cat.capitalize()}")
        md.append("")
        for e in by_cat[cat]:
            md.append(f"### {e.get('title','(untitled)')}  ({e.get('date','?')})")
            md.append("")
            if e.get("problem"):
                md.append(f"**Problem:** {e['problem']}")
                md.append("")
            if e.get("solution"):
                md.append(f"**Solution:** {e['solution']}")
                md.append("")
            if e.get("impact"):
                md.append(f"**Impact:** {e['impact']}")
                md.append("")
            if e.get("tech"):
                md.append(f"**Tech:** {', '.join(e['tech'])}")
                md.append("")
    out.write_text("\n".join(md), encoding="utf-8")
    print(f"wrote {out}  ({len(entries)} entries)")


def cmd_path(args) -> None:
    print(store_path())


def main() -> None:
    p = argparse.ArgumentParser(prog="impact_log", description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("add", help="save a JSON entry (from --file, preferred, or stdin)")
    sp.add_argument("-f", "--file", help="path to a JSON file holding the entry object")
    sp.set_defaults(func=cmd_add)

    sp = sub.add_parser("recent", help="show the last N entries")
    sp.add_argument("count", nargs="?", type=int, default=10)
    sp.set_defaults(func=cmd_recent)

    sp = sub.add_parser("search", help="full-text search")
    sp.add_argument("query")
    sp.set_defaults(func=cmd_search)

    sub.add_parser("stats", help="totals and time saved").set_defaults(func=cmd_stats)

    sp = sub.add_parser("export", help="write a resume-ready markdown report")
    sp.add_argument("-o", "--output", default="impact-report.md")
    sp.set_defaults(func=cmd_export)

    sub.add_parser("path", help="print the storage file path").set_defaults(func=cmd_path)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
