# skills

AI agent **Skills** for coding assistants like **Claude Code**, **Cursor**, and
**Codex** — reusable playbooks plus the scripts that power them.

## Install

Pick whichever you like — all install into your Claude Code skills directory
(`~/.claude/skills/`). Needs Node 16.7+.

```bash
# 1) From npm (shortest)
npx yashpatkar-skills                 # install every skill
npx yashpatkar-skills impact-log      # install one skill
npx yashpatkar-skills --list          # list available skills

# 2) From the skills.sh ecosystem
npx skills add YashPatkar/skills

# 3) From GitHub directly (no npm needed)
npx github:YashPatkar/skills

# 4) Manual — clone and copy the folder
git clone https://github.com/YashPatkar/skills.git
cp -r skills/impact-log ~/.claude/skills/
```

Then restart Claude Code (or open a new session) and type `/<skill-name>`
— e.g. `/impact-log`. Install elsewhere by setting `CLAUDE_SKILLS_DIR` first.

---

## What this is

A **Skill** is a folder containing a `SKILL.md` (natural-language instructions
your AI agent reads) plus any helper scripts. Drop it in `~/.claude/skills/` and
the agent gains a new `/command` — no plugins, no config. Each skill here is
self-contained and installs as a whole folder (instructions + scripts together).

## Available skills

| Skill | What it does |
|---|---|
| [impact-log](impact-log/) | Auto-capture your engineering accomplishments into a **local, searchable** career history — then export resume bullets, review notes, and interview stories. |

### Example: `impact-log` in action

After installing, you just finish some work and run the command — the AI reads
your session and git diff and drafts the entry for you:

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

Later, turn months of work into something useful:

```text
You ▸ /impact-log stats

  Total Entries: 37
  Categories:  Automation 12 · AI 8 · Bug Fixes 7 · Performance 6 · Deployment 4
  Estimated Time Saved: 143 hours
```

```text
You ▸ /impact-log export      # writes a resume-ready impact-report.md
```

See [impact-log/README.md](impact-log/) for full docs and privacy notes (all
data stays on your machine — nothing is ever uploaded).

---

## License

MIT — see [LICENSE](LICENSE).
