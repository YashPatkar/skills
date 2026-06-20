# impact-log

> Capture engineering accomplishments with almost zero effort and build a
> searchable, **100% local** career history — automatically.

`impact-log` is an AI agent **Skill**. Instead of keeping a work journal by hand,
you run `/impact-log` and let the AI analyze your current coding session, git
changes, and conversation to write a structured accomplishment entry for you.

It figures out:

- the **problem** you solved
- the **solution** you built
- the **technologies** used
- the **impact** (and time saved, when it can estimate it)
- the right **category**

Entries are saved to a local JSON file you own. Later, turn them into resume
bullets, performance-review notes, promotion docs, or interview stories.

**Privacy:** all data stays in `~/.impact-log/logs.json` on your machine.
Nothing is ever uploaded or transmitted.

---

## Commands

| Command | What it does |
|---|---|
| `/impact-log` | Analyze the session and save a new accomplishment (asks to confirm; only asks questions when unsure) |
| `/impact-log recent` | Show your last 10 entries |
| `/impact-log search <query>` | Full-text search across all entries |
| `/impact-log stats` | Totals, category breakdown, estimated time saved |
| `/impact-log export` | Generate a resume-ready `impact-report.md` |

---

## What's in this skill

```
impact-log/
  SKILL.md         # instructions the AI reads
  impact_log.py    # the engine: stores, searches, totals, exports (Python 3, no dependencies)
  README.md        # this file
```

The two files work as a pair: the AI does the thinking (reading your session and
drafting the entry), and `impact_log.py` does the exact, repeatable work
(saving, searching, math, export). **Both files install together** — a skill is
a folder, not a single file.

**Requirement:** Python 3.8+ on your `PATH` (`python` or `python3`). No `pip
install` needed — it uses only the standard library.

---

## Install

### Quickest: one `npx` command (Claude Code)

```bash
npx yashpatkar-skills impact-log
```

This copies the skill into `~/.claude/skills/impact-log/` (override with the
`CLAUDE_SKILLS_DIR` env var). Needs Node 16.7+. Restart Claude Code and type
`/impact-log`. Run `npx yashpatkar-skills` with no arguments to install
every skill in the collection.

### Via the skills.sh CLI

```bash
npx skills add YashPatkar/skills
```

### Manual: copy the folder (Claude Code)

Copy the `impact-log` folder into a skills directory Claude Code discovers:

- **For all projects:** `~/.claude/skills/impact-log/`
  (Windows: `C:\Users\<you>\.claude\skills\impact-log\`)
- **For one project:** `<project>/.claude/skills/impact-log/`

Then `/impact-log` is available. Example (clone this repo, copy the folder):

```bash
git clone https://github.com/YashPatkar/skills.git
# macOS / Linux
mkdir -p ~/.claude/skills && cp -r skills/impact-log ~/.claude/skills/
```

```powershell
# Windows PowerShell
git clone https://github.com/YashPatkar/skills.git
New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null
Copy-Item -Recurse skills\impact-log "$HOME\.claude\skills\"
```

Restart Claude Code (or start a new session) and type `/impact-log`.

### Claude.ai / Claude Desktop (Skills)

In the app, open **Settings → Capabilities → Skills** and add a skill by
uploading the `impact-log` folder (zip it first if upload expects an archive).
Claude reads `SKILL.md` automatically.

> Note: the bundled `impact_log.py` runs only in environments that can execute
> code (Claude Code, the code-execution sandbox). In a plain chat without code
> execution, Claude can still follow the SKILL.md playbook but can't persist to
> a local file.

### Codex CLI, Cursor, and other agents that run shell commands

Any coding agent that can run terminal commands can use this skill — it's just
a markdown playbook plus a Python script. Point the agent at
`impact-log/SKILL.md` (or copy its contents into your `AGENTS.md` / rules file)
and make sure `impact_log.py` sits in the same folder. The agent calls
`python impact_log.py ...` exactly as described in SKILL.md.

### ChatGPT (no local execution)

A standard ChatGPT chat or Custom GPT can't run Python on your machine, so it
can't maintain the local JSON store. You can still paste `SKILL.md` into a
Custom GPT's instructions to get the *capture playbook* (it'll draft entries in
the conversation), but for the full save/search/stats/export experience use an
agent that executes code (Claude Code, Codex, Cursor).

---

## Storage & data format

Default location: `~/.impact-log/logs.json` — override with the
`IMPACT_LOG_HOME` environment variable. Each entry looks like:

```json
{
  "id": "2026-06-20-001",
  "date": "2026-06-20",
  "title": "Task Assignment Automation",
  "category": "automation",
  "problem": "Manual task creation took 30+ min daily.",
  "solution": "Built JWT-authenticated API automation.",
  "impact": "Daily effort dropped to under 5 minutes.",
  "tech": ["Python", "REST API", "JWT"],
  "time_saved_hours": 25,
  "confidence": 0.94
}
```

Categories: `automation`, `ai`, `performance`, `deployment`, `frontend`,
`backend`, `security`, `bugfix`, `devops`, `database`, `architecture`, `other`.

---

## Run it directly (without an AI)

The engine works on its own, too:

```bash
python impact_log.py recent
python impact_log.py search automation
python impact_log.py stats
python impact_log.py export -o impact-report.md
python impact_log.py path        # where your data lives
```

To add an entry manually, write a JSON file and pass it with `--file`:

```bash
python impact_log.py add --file my-entry.json
```

---

## License

MIT — see [LICENSE](../LICENSE).
