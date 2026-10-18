---
name: agent-memory
description: Use when an agent keeps knowledge across sessions by writing it down - at the start and end of a session where AGENTS.md names a memory directory (such as memory/ in an agent workspace), when the user asks to remember something, to set up a memory, or to consolidate, reflect on, or clean up a memory, and when promoting knowledge into a shared memory. Not for workers following a BRIEF.md; their brief says where to write.
---

# Agent memory

A memory is a directory where one agent writes down what it learns, so a later session, starting with no context,
can pick up where the last one stopped and does not relearn what was already known. Raw input lands in the inbox and
the journal; consolidation distills it into notes.

## Layout

```
<memory>/
├── README.md        # what this memory is for, who owns it, and an index of the notes
├── journal/         # what happened and why, one file per session: YYYY-MM-DD-HHMM.md
├── notes/           # durable knowledge, one topic per file
└── inbox/           # raw input waiting for consolidation, one file per item: YYYY-MM-DDTHHMM-slug.md
```

The memory lives where the `AGENTS.md` of the directory you work in says; in an agent workspace it is `memory/`. Any
directory can hold one, and a memory can be shared by several workspaces or agents: the owner is whoever its README
names.

## Rules

- **Single owner.** Only the owner writes the README, the journal, and the notes. Everyone else, such as workers or
  other agents, writes only to the inbox.
- **Notes are the current truth, the journal is history.** Rewrite or delete a note when it stops being true. Never
  edit a journal entry; add a correction in a later one.
- **Write for a reader without your context.** Name files, branches, commits, and task ids so entries can be traced.
  Record decisions with their reasons, not only actions.
- **Information over code.** Snippets and examples are fine; implementations belong in a repo, and the note points
  there.
- **No secrets.** Credentials, tokens, and personal data never go into a memory.
- **Fill templates, do not invent formats.** The README and inbox item formats are in `templates/`.

## Start of a session

1. Read the README, then the latest journal file. Read older journal files only when the latest one points to them.
2. Read the notes the README lists as relevant to what the user wants to work on now.
3. Mention how many inbox items are waiting, if any. Do not consolidate unasked.

## During a session

- When the user states a preference, corrects you, or settles a decision that will matter again, write it into the
  matching note right away.
- Anything else worth keeping that you cannot settle now, such as an idea, a finding outside the current work, or an
  open question, goes into the inbox as an item from `templates/inbox-item.md`. Do not stop to consolidate.

## End of a session

When the user wraps up, or before you stop after a meaningful chunk of work, write the session's journal file,
named after the time the session started:

```markdown
# 2026-10-18 14:30

## Asked
Fix the modal focus trap in web-app.

## Done
Fixed it on frontend/main (a1b2c3d). Stacked dialogs each registered a global keydown handler. Regression test in
Modal.test.tsx.

## Decided
No focus manager in design-system for now: only web-app stacks dialogs.

## Open
Whether design-system should own focus handling once a second app stacks dialogs.
```

If the session runs long, append to the same file rather than starting a new one. Then tell the user what changed in
the memory, if it lives in a repo they commit.

## Set up a memory

1. Create the layout above, with `README.md` from `templates/README.md` and an empty `.gitkeep` in each empty
   directory.
2. Add `templates/AGENTS-section.md` to the `AGENTS.md` of the directory it serves, so the next session loads this
   skill.

## References

- **Consolidate** (`references/consolidate.md`). The user asks to consolidate, reflect on, or clean up a memory, a
  workspace is about to close, or knowledge should move into a shared memory.
