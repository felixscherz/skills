# Memory

The memory is where the factory agent writes down what it learns, so a later session, starting with no context, can
pick up where the last one stopped and does not relearn what was already known. Raw input lands in the inbox and the
journal; consolidation distills it into notes.

```
memory/
├── README.md        # what this memory is for and an index of the notes
├── journal/         # what happened and why, one file per session: YYYY-MM-DD-HHMM.md
├── notes/           # durable knowledge, one topic per file
└── inbox/           # raw input waiting for consolidation, one file per item: YYYY-MM-DDTHHMM-slug.md
```

## Rules

- **Notes are the current truth, the journal is history.** Rewrite or delete a note when it stops being true. Never
  edit a journal entry; add a correction in a later one.
- **Write for a reader without your context.** Name files, branches, commits, backlog items, and task ids so entries
  can be traced. Record decisions with their reasons, not only actions.
- **Information over code.** Snippets and examples are fine; implementations belong in a repo, and the note points
  there.
- **Work is not knowledge.** Something to be done goes into the backlog, not into a note. A note may say what kind of
  work the user wants or rejects.

## Set up the memory

Create the layout above, with `README.md` from `../templates/memory-README.md` and an empty `.gitkeep` in each empty
directory.

## Notes

One topic per note, with a name that says what it is about, such as `focus-traps.md` or `review-preferences.md`.
Write the knowledge itself: what is true, why, and how to apply it. The story of how it was found belongs in the
journal. Keep the README's index current: every note with a one-line description.

What the user wants from the factory's work, such as which changes they welcome, which they reject, and how they like
PRs shaped, belongs in notes too. Finding work and writing PRs read them.

## Inbox items

Anything worth keeping that cannot be settled now, such as a finding outside the current work or an open question,
becomes one file in `inbox/` from `../templates/inbox-item.md`. Workers write their side findings here in the same
format.

## Journal entries

Name the file after the time the session started. If the session runs long, append to the same file rather than
starting a new one.

```markdown
# 2026-10-18 14:30

## Asked
Find small refactorings in web-app's checkout module.

## Done
Proposed 0004 to 0007. The user approved 0005 and 0006 and rejected 0004. Worked 0005 into a draft PR
(https://github.com/acme/web-app/pull/212).

## Decided
No refactors in billing/ until the payment migration lands (0004 rejected, see notes/scope.md).

## Open
Whether 0006 should wait for 0005's review, since both touch CartTotals.
```

## Consolidate

Consolidation turns the inbox and the journal into durable notes and backlog items, and keeps the notes small and
true. Run it when the user asks or before the factory closes. Do not consolidate unasked during other work.

### Resolve the inbox

Go through every file in `inbox/`, oldest first. Batch items about the same thing, such as all items from one task.
When an item has references, such as a task result or a journal entry, read them before deciding. Each item ends as
exactly one of:

- **New note.** The knowledge is durable and no note covers it yet.
- **Refined note.** An existing note covers the topic. Add, correct, or remove what the item changes.
- **Work.** The item asks for something to be done. Add it to the backlog as a proposed item (see `backlog.md`).
- **Nothing.** Not relevant, already known, or no longer true.

Then delete the item. Consolidation leaves the inbox empty.

### Review the notes

- Merge notes that cover the same topic. Delete notes that are no longer true or no longer matter.
- Read the journal files since the last consolidation for decisions and lessons that never made it into a note, and
  the `## Decision` sections of items rejected since then.

### Finish

1. Update the README's index of notes.
2. Write a journal entry: which inbox items became what, and which notes changed.
3. Promote what applies beyond this factory (below).

## Promote to a shared memory

Knowledge that holds beyond this factory, such as how a repo, tool, or service behaves, goes to a shared memory when
there is one, such as one the user keeps for a whole project. The factory agent does not own it, so write one inbox
item per piece of knowledge into its `inbox/`, with `from:` set to the absolute path of this memory and references
back to the notes or journal entries it came from. Only the shared memory's owner turns them into notes there.

When you own a shared memory, consolidate it the same way. Follow each item's references to read the source, never
write there, and keep only what holds outside the place it came from.
