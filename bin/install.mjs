#!/usr/bin/env node
// Installs skills from this repo into your Claude Code skills directory.
//
//   npx github:YashPatkar/skills            # install every skill
//   npx github:YashPatkar/skills impact-log # install just one
//   npx github:YashPatkar/skills --list     # list available skills
//
// Target dir: $CLAUDE_SKILLS_DIR, else ~/.claude/skills
// No dependencies — Node stdlib only.

import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

function findSkills() {
  return fs
    .readdirSync(repoRoot, { withFileTypes: true })
    .filter(
      (e) =>
        e.isDirectory() &&
        !e.name.startsWith(".") &&
        e.name !== "bin" &&
        e.name !== "node_modules" &&
        fs.existsSync(path.join(repoRoot, e.name, "SKILL.md"))
    )
    .map((e) => e.name);
}

function main() {
  const args = process.argv.slice(2);
  const available = findSkills();

  if (available.length === 0) {
    console.error("No skills found in this package (no folder contains a SKILL.md).");
    process.exit(1);
  }

  if (args.includes("--list") || args.includes("-l")) {
    console.log("Available skills:");
    for (const s of available) console.log(`  - ${s}`);
    return;
  }

  const requested = args.filter((a) => !a.startsWith("-"));
  const toInstall = requested.length ? requested : available;

  const unknown = toInstall.filter((s) => !available.includes(s));
  if (unknown.length) {
    console.error(`Unknown skill(s): ${unknown.join(", ")}`);
    console.error(`Available: ${available.join(", ")}`);
    process.exit(1);
  }

  const dest = process.env.CLAUDE_SKILLS_DIR || path.join(os.homedir(), ".claude", "skills");
  fs.mkdirSync(dest, { recursive: true });

  for (const skill of toInstall) {
    const from = path.join(repoRoot, skill);
    const to = path.join(dest, skill);
    fs.cpSync(from, to, {
      recursive: true,
      filter: (src) => !src.includes("__pycache__") && !src.endsWith(".pyc"),
    });
    console.log(`✓ installed ${skill}  ->  ${to}`);
  }

  console.log(`\nDone. ${toInstall.length} skill(s) installed to ${dest}`);
  console.log("Restart Claude Code (or start a new session), then type /<skill-name> — e.g. /impact-log");
}

main();
