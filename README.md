# skills

A collection of AI agent **Skills** I build — reusable playbooks (plus the
scripts that power them) for tools like Claude Code, Codex, and Cursor.

Each skill lives in its own folder with a `SKILL.md` (the agent instructions),
any supporting code, and a `README.md` explaining what it does and how to
install it.

## Skills

| Skill | What it does |
|---|---|
| [impact-log](impact-log/) | Auto-capture engineering accomplishments into a local, searchable career history (resume bullets, reviews, interview stories). |

## Install (one command)

Install every skill into your Claude Code skills directory (`~/.claude/skills/`)
with `npx` — no clone, no setup, Node 16.7+ only:

```bash
npx github:YashPatkar/skills
```

Install just one, or see what's available:

```bash
npx github:YashPatkar/skills impact-log   # install a single skill
npx github:YashPatkar/skills --list       # list available skills
```

Restart Claude Code (or open a new session), then type `/<skill-name>`
(e.g. `/impact-log`). To install somewhere other than `~/.claude/skills`, set
`CLAUDE_SKILLS_DIR` first.

### Manual install

A skill is a **folder**, not a single file — install the whole folder so its
scripts come along. Copy the skill folder into `~/.claude/skills/<skill-name>/`:

```bash
git clone https://github.com/YashPatkar/skills.git
cp -r skills/impact-log ~/.claude/skills/
```

## License

MIT — see [LICENSE](LICENSE).
