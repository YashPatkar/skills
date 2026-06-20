---
name: impact-log
description: Capture an engineering accomplishment from the current session and save it to a local, searchable career history. Use when the user says /impact-log, "log this", "track this accomplishment", "record what I did", "impact log", "add to my worklog", or asks to see recent logs, search logs, show impact stats, or export a resume/impact report.
---

# impact-log

Turn the work in the current Claude Code session into a structured, **local-only**
accomplishment record — then search it, total it up, and export it for resumes,
reviews, and interviews. Nothing is ever sent anywhere; all data lives in a JSON
file on this machine.

The skill is AI-first: **you** analyze the session and write the entry. The driver
([impact_log.py](impact_log.py), Python 3, stdlib only) just persists, searches, and
reports. Do not make the user fill out a form.

Storage: `~/.impact-log/logs.json` (override with the `IMPACT_LOG_HOME` env var).
All commands below are run from this skill's directory; `impact_log.py` is here.

## Capture a new accomplishment — `/impact-log` (the default)

This is the main flow. Do NOT interrogate the user. Instead:

1. **Gather evidence** from what's already available, in this order:
   - the current conversation (code written, bugs fixed, decisions made — you
     already have this context)
   - `git diff`, `git status`, `git log --oneline -15` if this is a git repo
   - files recently changed in the session
2. **Infer** the fields: `title`, `category`, `problem`, `solution`, `impact`,
   `tech` (list), and — when you can estimate it — `time_saved_hours`. Set a
   `confidence` between 0 and 1.
3. **Decide based on confidence:**
   - **≥ 0.8** — present the drafted entry and ask only `Save? [Y/n]`.
   - **< 0.8** — ask ONLY for the specific missing piece (usually impact /
     time saved). One question, not five. Then save.
4. **Write the entry to a temp JSON file and save it** (see below).

`category` must be one of: `automation`, `ai`, `performance`, `deployment`,
`frontend`, `backend`, `security`, `bugfix`, `devops`, `database`,
`architecture`, `other` (anything unrecognized is stored as `other`).

### Saving an entry (file-based — works on every shell)

Write the entry JSON to a temp file, then call `add --file`. **Do not pipe JSON
via stdin on Windows** — PowerShell re-encodes it (UTF-16/BOM) and the parse fails.

PowerShell (the user's default shell):

```powershell
$tmp = "$env:TEMP\impact-entry.json"
@'
{"title":"Task Assignment Automation","category":"automation","problem":"Manual task creation took 30+ min daily.","solution":"Built JWT-authenticated API automation.","impact":"Daily effort dropped to under 5 minutes.","tech":["Python","REST API","JWT"],"time_saved_hours":25,"confidence":0.94}
'@ | Out-File -FilePath $tmp -Encoding utf8
python impact_log.py add --file $tmp
Remove-Item $tmp
```

Bash:

```bash
cat > /tmp/impact-entry.json <<'EOF'
{"title":"Task Assignment Automation","category":"automation","problem":"Manual task creation took 30+ min daily.","solution":"Built JWT-authenticated API automation.","impact":"Daily effort dropped to under 5 minutes.","tech":["Python","REST API","JWT"],"time_saved_hours":25,"confidence":0.94}
EOF
python impact_log.py add --file /tmp/impact-entry.json
```

`id` and `date` are assigned automatically (`id` is `YYYY-MM-DD-NNN`, sequential
per day). On success it prints `saved <id>  "<title>"  [<category>]`.

## Other commands

| User says | Run | Does |
|---|---|---|
| `/impact-log recent` | `python impact_log.py recent` | last 10 entries (pass a number for more) |
| `/impact-log search <q>` | `python impact_log.py search <q>` | full-text search across all fields |
| `/impact-log stats` | `python impact_log.py stats` | totals, category breakdown, time saved |
| `/impact-log export` | `python impact_log.py export` | writes `impact-report.md` (use `-o` for a path) |
| — | `python impact_log.py path` | print the storage file location |

After running a command, relay the output to the user in a readable way — don't
just dump it.

## Entry schema

```json
{
  "id": "2026-06-20-001",        // auto-assigned
  "date": "2026-06-20",          // auto-assigned (today) if omitted
  "title": "Task Assignment Automation",
  "category": "automation",
  "problem": "Manual task creation took 30+ min daily.",
  "solution": "Built JWT-authenticated API automation.",
  "impact": "Daily effort dropped to under 5 minutes.",
  "tech": ["Python", "REST API", "JWT"],
  "time_saved_hours": 25,        // optional; only this feeds the stats total
  "confidence": 0.94             // optional
}
```

Only `title` is required. `time_saved_hours` is the only field that feeds the
"Estimated Time Saved" total — include it whenever you can defensibly estimate it,
otherwise leave it out (stats will say none is recorded rather than inventing one).

## Gotchas

- **Never pipe JSON to `add` via stdin on Windows.** PowerShell pipes encode as
  UTF-16, so Python reads garbage. Always write a temp file and use `--file`.
  The driver reads files as `utf-8-sig`, so a BOM from `Out-File -Encoding utf8`
  is fine.
- **Privacy is the selling point.** Data only ever touches `~/.impact-log/`
  (or `IMPACT_LOG_HOME`). Don't add any step that uploads or transmits entries.
- **Don't fabricate impact.** If you can't estimate time saved or business
  impact, ask one question or leave the field empty — don't make up numbers.

## Troubleshooting

- **`error: input is not valid JSON`** — the temp file isn't valid JSON (often a
  stray trailing comma, or you piped via stdin on PowerShell). Re-write the file
  and use `--file`.
- **`error: ... logs.json is corrupt JSON`** — the store was hand-edited into an
  invalid state. Open `python impact_log.py path` to find it and fix/remove it.
- **`python` not found** — try `python3 impact_log.py ...`.
