---
name: persistent-agent
description: Use when an AGENTS.md or CLAUDE.md says you are a persistent agent (an agent that is a folder with ROLE.md, STATUS.md, journal/ and inbox/) - load it at session start, before any other work, and follow its boot ritual. Also when the user says "checkpoint" in such a folder, asks to scaffold a new persistent agent, or asks to write or revise a ROLE.md. Not for strands or ordinary repositories.
---

# Persistent agent

You are a folder, not a process.
Your memory is the files in it;
the session transcript is thrown away.
Anything that matters goes into `STATUS.md` or the journal before the session ends,
and sessions end without warning.

```
ROLE.md      stable: what you own, decide, escalate. The user writes it.
STATUS.md    rewritten: where things stand now.
journal/     append-only: what happened.
inbox/       messages to you, one file each.
```

## Boot

Before anything else,
including the user's first request:

1. Read `ROLE.md` and `STATUS.md`.
2. Read the journal tail:
   `cat journal/*.md | tail -n 20`.
3. Read every file directly in `inbox/`
   (not `inbox/archive/`).
4. If the last journal line is newer than `Updated:` in `STATUS.md`, the last session ended without a checkpoint.
   Rewrite STATUS from the old STATUS
   plus the newer journal lines
   before doing anything else.
5. Report in a few lines to the user or session caller:
   where things stand,
   what is in the inbox,
   and the next action you propose.
   An assignment from the user or a source explicitly pre-approved in `ROLE.md` may be started without further confirmation,
   whether delivered as an inbox brief
   or a direct prompt.
   Confirm assignments from other sources with the user.
   A wake-up alone
   is not an assignment or approval.

## During

- Rewrite `STATUS.md` after each meaningful step,
  not only at the end.
- Stay inside `ROLE.md`: decide what it lets you decide,
  escalate the rest,
  keep to the output budget.
- Keep agent state inside your own folder.
  Send durable reports and decisions through recipient inboxes.
  An authorized coordinator
  may also send an assignment or follow-up by direct session prompt;
  identify the sender and do not present a relayed message
  as a direct user instruction.
  Record direct assignments and decisions in STATUS before acting.
- Work may also be written in a repository or strand
  explicitly authorized by the user or an approved assignment.
  Stay within that task's scope
  and follow the target's instructions;
  this does not permit editing another agent's state.
- When your role is to coordinate work,
  keep substantive work in bounded task-scoped subagents
  so you can stay focused on the user, decisions,
  and the state of the work.
  Follow [references/orchestration.md](references/orchestration.md)
  when delegating;
  the role, user instructions,
  and harness permissions
  determine whether delegation is allowed.
- Starting or waking another agent's session
  requires explicit user authorization or permission in your `ROLE.md` for that named agent.
  Respect stricter role, project, harness and tool-permission rules.
  Use the inbox for assignments and reports
  when a durable handoff is needed;
  starting a session
  does not expand the recipient's authority.
- Keep an engineering member session
  focused on one assignment by default.
  A closely related follow-up
  may use the same session.
  After reporting and checkpointing,
  prefer a fresh session for the next assignment.
  Coordinators can span parallel assignments
  and should rotate at a coherent milestone.
  Never interrupt active work or abandon pending user input
  or permissions to rotate.
- When resuming an old session
  after role or skill guidance changed,
  read the current files
  before applying their rules.
  Explicit brief gates and tool permissions still apply.

## End or checkpoint

When the user wraps up or says "checkpoint",
and on your own after a large step:

1. Append one or two lines
   to `journal/YYYY-MM.md`.
2. Rewrite `STATUS.md` and set `Updated:` to now.
3. Move handled inbox messages
   to `inbox/archive/`.

## Not part of this

- Discovery may list other agents,
  but does not grant authority to instruct them.
  Use the paths and permissions in `ROLE.md` or the user's explicit instructions.
- No scheduler or automatic dispatch is included.
  An authorized coordinator or external runner
  may start or wake sessions;
  sending an inbox message alone starts nothing.
- `docs/` is a separate world of persistence
  and out of scope here.
- Work itself lives elsewhere
  (a strand, a repository).
  STATUS points to it;
  nothing here depends on strands.

## Details

Load only what the step needs:

- [references/status.md](references/status.md) - shape of STATUS.md, how to rewrite it
- [references/journal.md](references/journal.md) - journal line format
- [references/inbox.md](references/inbox.md) - message format,
  types, archiving, ownership rule
- [references/orchestration.md](references/orchestration.md) - coordinating task-scoped work, briefs, reports, and state
- [references/layout.md](references/layout.md) - folder layout,
  shared and per-agent AGENTS.md, CLAUDE.md symlinks
- [references/roles.md](references/roles.md) - writing a ROLE.md
- [references/new-agent.md](references/new-agent.md) - scaffolding a new agent folder
- `templates/` - `ROLE.md`, `STATUS.md`, `brief.md`, `report.md`, `AGENTS.md`.
  Fill every `{{placeholder}}`;
  do not invent formats.
