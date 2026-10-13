---
name: author-skill
description: How to author, edit, or move an Agent Skill (a SKILL.md) for broad agent compatibility. Use whenever creating or changing a skill, including fixing or updating an installed global skill under ~/.claude/skills or ~/.agents/skills, or when record-learnings decides a learning belongs in a skill. Covers where global and project-local skills live, the shared SKILL.md format, and harness-specific settings such as disabling auto-invocation.
---

# Authoring portable agent skills

Skills serve several harnesses (Claude Code, opencode, Codex, possibly more).
Two goals:

1. Every harness reads skills from the same place, so there is one copy.
2. Harness-level behavior (like auto-invocation) is configured for each
   harness's own convention, so all harnesses behave the same.

## Global or project-local

- **Global** - useful across repositories (personal workflow, general
  practices). The source of truth is the skills repo at
  `~/workspaces/personal/skills`. Author or edit a skill there, in
  `skills/<name>/SKILL.md`, or `skills/<group>/<name>/SKILL.md` for a group
  that already exists.
  - Never edit the installed copies in `~/.agents/skills/` or
    `~/.claude/skills/`. `npx skills` copies them from the repo, and the next
    update overwrites any change made there. When a task points you at an
    installed skill, edit the skill of the same name in the repo instead.
  - Skill names must be unique across the whole repo, groups included,
    because every skill is installed flat.
  - The change reaches the harnesses only after it is committed and pushed
    and the user runs `npx skills update -g`. A new skill needs the `npx
    skills add` command from the repo's README instead, since `update` does
    not pick up new skills. Tell the user which one to run.
- **Project-local** - specific to one repository's code, tooling, or
  conventions. Default to `.agents/skills/<name>/SKILL.md`, which most
  harnesses read. If the repo already keeps skills in `.claude/skills` or
  `.opencode/skills`, follow that instead. Do not move existing skills unless
  asked.

When unsure, ask which one the user wants.

## SKILL.md format

- One kebab-case directory per skill containing `SKILL.md`.
- Frontmatter core that every harness reads:
  - `name`: must match the directory name.
  - `description`: a single-line routing rule, not a summary. The model sees
    it before deciding to load the body, so state the concrete situations,
    phrases users would say, and boundaries.
- Body: portable markdown. Reference bundled files by relative path.
- Harnesses ignore unknown frontmatter fields, so harness-specific fields are
  safe to add.

## Harness conventions

When a skill must be user-invoked only, disable model invocation for every
harness:

```yaml
disable-model-invocation: true   # Claude Code
metadata:
  opencode/autoinvoke: false     # opencode
```

Codex does not read this from the frontmatter. It needs a separate `agents/openai.yaml` in the skill directory:

```yaml
policy:
  allow_implicit_invocation: false
```

Setting only some of them leaves the harnesses behaving differently. The same applies to
any other harness-level setting: check how each harness expresses it and set
all of them. `argument-hint` (Claude Code) shows a hint when the user passes
arguments.
