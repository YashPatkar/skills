# impact-log

> Capture engineering accomplishments with almost zero effort and build a
> searchable, **100% local** career history — automatically.

## Install

```bash
# From npm (shortest)
npx yashpatkar-skills impact-log

# Or install the whole collection
npx yashpatkar-skills

# Or via the skills.sh ecosystem
npx skills add YashPatkar/skills

# Or straight from GitHub (no npm)
npx github:YashPatkar/skills

# Or manually — clone and copy the folder
git clone https://github.com/YashPatkar/skills.git
cp -r skills/impact-log ~/.claude/skills/        # macOS / Linux
```

Any of these copy the skill into `~/.claude/skills/impact-log/` (set
`CLAUDE_SKILLS_DIR` to install elsewhere). Needs **Node 16.7+** to install and
**Python 3.8+** on your `PATH` to run (standard library only — no `pip install`).
Then restart Claude Code (or start a new session) and type `/impact-log`. Other
install targets (Claude Desktop, Cursor, ChatGPT) are covered [below](#more-install-options).

---

## What it does

Instead of keeping a work journal by hand, you run `/impact-log` and let the AI
read your current coding session, git diff, and conversation to write a
structured accomplishment entry for you. It infers the **problem** you solved,
the **solution** you built, the **technologies** used, the **impact** (and time
saved, when it can estimate it), and the right **category** — then saves it to a
local file you own. It's AI-first: it only asks a question when it genuinely
can't infer something, never a form.

Later, turn months of entries into resume bullets, performance-review notes,
promotion docs, weekly reports, or interview stories.

**Privacy:** all data stays in `~/.impact-log/logs.json` on your machine.
Nothing is ever uploaded or transmitted.

## Example

You finish a feature, then:

```text
You ▸ /impact-log

impact-log ▸ I found an accomplishment in this session:

  Title    : Task Assignment Automation
  Category : automation
  Problem  : Manual task creation took 30+ minutes daily.
  Solution : Built JWT-authenticated API automation.
  Impact   : Daily effort dropped to under 5 minutes (~25 hrs/month saved).
  Tech     : Python, REST API, JWT

  Save this? [Y/n]  ▸ Y
  ✓ saved 2026-06-20-001
```

If it can't infer one field (say, time saved), it asks **only that one thing** —
not five form questions. Then, across all your entries:

```text
You ▸ /impact-log recent           # last 10 accomplishments
You ▸ /impact-log search jwt        # full-text search
You ▸ /impact-log stats

  Total Entries: 37
  Categories:  Automation 12 · AI 8 · Bug Fixes 7 · Performance 6 · Deployment 4
  Estimated Time Saved: 143 hours

You ▸ /impact-log export             # writes a resume-ready impact-report.md
```

## Commands

| Command | What it does |
|---|---|
| `/impact-log` | Analyze the session and save a new accomplishment (confirms before saving; only asks when unsure) |
| `/impact-log recent` | Show your last 10 entries |
| `/impact-log search <query>` | Full-text search across all entries |
| `/impact-log stats` | Totals, category breakdown, estimated time saved |
| `/impact-log export` | Generate a resume-ready `impact-report.md` |

## What's in this skill

```
impact-log/
  SKILL.md         # instructions the AI reads
  impact_log.py    # the engine: stores, searches, totals, exports (Python 3, no dependencies)
  README.md        # this file
```

The files work as a pair: the AI does the thinking (reading your session and
drafting the entry), and `impact_log.py` does the exact, repeatable work
(saving, searching, math, export). **Both install together** — a skill is a
folder, not a single file.

---

## More install options

### Claude Code — install location

`~/.claude/skills/impact-log/` makes it available in **every** project;
`<project>/.claude/skills/impact-log/` scopes it to one. On Windows the home
path is `C:\Users\<you>\.claude\skills\impact-log\`. PowerShell manual copy:

```powershell
git clone https://github.com/YashPatkar/skills.git
New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null
Copy-Item -Recurse skills\impact-log "$HOME\.claude\skills\"
```

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
