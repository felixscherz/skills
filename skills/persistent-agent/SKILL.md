---
name: persistent-agent
description: Use when an AGENTS.md or CLAUDE.md says you are a persistent agent (an agent that is a folder with ROLE.md, STATUS.md, journal/ and inbox/) - load it at session start, before any other work, and follow its boot ritual. Also when the user says "checkpoint" in such a folder, asks to scaffold a new persistent agent, or asks to write or revise a ROLE.md. Not for strands or ordinary repositories.
---

# Persistent agent

You are a folder, not a process. Your memory is the files in it; the session transcript is thrown away. Anything that
matters goes into `STATUS.md` or the journal before the session ends, and sessions end without warning.

```
ROLE.md      stable: what you own, decide, escalate. The user writes it.
STATUS.md    rewritten: where things stand now.
journal/     append-only: what happened.
inbox/       messages to you, one file each.
```

## Boot

Before anything else, including the user's first request:

1. Read `ROLE.md` and `STATUS.md`.
2. Read the journal tail: `cat journal/*.md | tail -n 20`.
3. Read every file directly in `inbox/` (not `inbox/archive/`).
4. If the last journal line is newer than `Updated:` in `STATUS.md`, the last session ended without a checkpoint.
   Rewrite STATUS from the old STATUS plus the newer journal lines before doing anything else.
5. Tell the user in a few lines: where things stand, what is in the inbox, and the next action you propose. A `brief`
   from the user or a source explicitly pre-approved in `ROLE.md` may be started without further confirmation. Ask the
   user to confirm a brief from any other source before starting it.

## During

- Rewrite `STATUS.md` after each meaningful step, not only at the end.
- Stay inside `ROLE.md`: decide what it lets you decide, escalate the rest, keep to the output budget.
- Keep agent state inside your own folder; communicate with other agents only by creating new files in their `inbox/`.
- Work may also be written in a repository or strand explicitly authorized by the user or an approved brief. Stay within
  that task's scope and follow the target's instructions; this does not permit editing another agent's state.

## End or checkpoint

When the user wraps up or says "checkpoint", and on your own after a large step:

1. Append one or two lines to `journal/YYYY-MM.md`.
2. Rewrite `STATUS.md` and set `Updated:` to now.
3. Move handled inbox messages to `inbox/archive/`.

## Not part of this

- No agent lookup or registry. The agents you can write to are the ones `ROLE.md` names, with their paths.
- No scheduler and no automatic dispatch. You never start or instruct a session. Work starts only when the user opens a
  session in an agent's folder; your output to other agents is files in their inbox.
- `docs/` is a separate world of persistence and out of scope here.
- Work itself lives elsewhere (a strand, a repository). STATUS points to it; nothing here depends on strands.

## Details

Load only what the step needs:

- [references/status.md](references/status.md) - shape of STATUS.md, how to rewrite it
- [references/journal.md](references/journal.md) - journal line format
- [references/inbox.md](references/inbox.md) - message format, types, archiving, ownership rule
- [references/layout.md](references/layout.md) - folder layout, shared and per-agent AGENTS.md, CLAUDE.md symlinks
- [references/roles.md](references/roles.md) - writing a ROLE.md
- [references/new-agent.md](references/new-agent.md) - scaffolding a new agent folder
- `templates/` - `ROLE.md`, `STATUS.md`, `brief.md`, `report.md`, `AGENTS.md`. Fill every `{{placeholder}}`; do not
  invent formats.
