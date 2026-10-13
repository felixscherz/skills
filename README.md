# skills

My Agent Skills, written to work across harnesses: Claude Code, Codex, and
opencode. Each skill is a directory with a `SKILL.md` under `skills/`, such as
`skills/engineering/`. Skills can be grouped, such as vendored skills under
`skills/<group>/<skill>/`, as long as no folder above a `SKILL.md` has one of
its own. Skill names must be unique across the whole repo, because every skill
is installed flat.

## Install

`npx skills` copies the skills into each agent's skill directory:

```sh
npx skills add felixscherz/skills -g -s '*' -a claude-code -a codex -a opencode
```

Remove them with `npx skills remove -g`.

## Change a skill

This repo is the source of truth. Edit skills here, never the installed copies
in `~/.agents/skills/` or `~/.claude/skills/`, which the next update
overwrites.

1. Edit, commit, and push.
2. Run `npx skills update -g` to pull the change into every agent.

`update` does not pick up new skills. After adding a skill, rerun the `add`
command above.
