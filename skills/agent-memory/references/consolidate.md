# Consolidate

Consolidation turns the inbox and the journal into durable notes, and keeps the notes small and true. The owner runs
it, when the user asks or before the workspace it serves closes.

## Resolve the inbox

Go through every file in `inbox/`, oldest first. Batch items about the same thing, such as all items from one task.
When an item has references, such as a task result or a journal entry, read them before deciding. Each item ends as
exactly one of:

- **New note.** The knowledge is durable and no note covers it yet.
- **Refined note.** An existing note covers the topic. Add, correct, or remove what the item changes.
- **Work.** The item asks for something to be done. Hand it to whatever tracks work here, such as the "Next" section
  of a `STATUS.md`, or to the user.
- **Nothing.** Not relevant, already known, or no longer true.

Then delete the item. Consolidation leaves the inbox empty.

## Review the notes

- One topic per note, with a name that says what it is about, such as `focus-traps.md`.
- Write the knowledge itself: what is true, why, and how to apply it. The story of how it was found belongs in the
  journal.
- Merge notes that cover the same topic. Delete notes that are no longer true or no longer matter.
- Read the journal files since the last consolidation for decisions and lessons that never made it into a note.

## Finish

1. Update the README's index of notes: every note with a one-line description.
2. Write a journal entry: which items became what, and which notes changed.
3. Promote what applies beyond this memory (below).

## Promote to a shared memory

Knowledge that holds beyond the work this memory serves, such as how a repo, tool, or service behaves, goes to a shared
memory when there is one, such as one the user keeps for a whole project. You do not own it, so write one inbox item
per piece of knowledge into its `inbox/`, with `from:` set to the absolute path of this memory and references back to
the notes or journal entries it came from. Only the shared memory's owner turns them into notes there.

When you own a shared memory, consolidate it the same way. Follow each item's references to read the source, never
write there, and keep only what holds outside the place it came from.
