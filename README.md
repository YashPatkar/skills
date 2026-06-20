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

## Installing a skill

A skill is a **folder**, not a single file — install the whole folder so its
scripts come along. See each skill's own README for exact steps. For Claude
Code, the short version is: copy the skill folder into
`~/.claude/skills/<skill-name>/`.

```bash
git clone https://github.com/YashPatkar/skills.git
```

## License

MIT — see [LICENSE](LICENSE).
