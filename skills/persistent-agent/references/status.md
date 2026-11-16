# STATUS.md

The snapshot of now, and the file a booting session relies on. A reader with only `ROLE.md` and `STATUS.md` must be
able to continue the work.

- **Rewritten, never appended.** Replace the whole file each time. History belongs in the journal.
- **About one screen.** If it grows, cut: finished items go, detail goes to where the work lives.
- **Four sections**, from `templates/STATUS.md`:
  - *Goal* - what you are working towards right now, one or two lines.
  - *In flight* - each open piece of work with its state and where it lives (strand, repository, branch, PR).
  - *Blockers* - what is stuck and on whom. "None" if none.
  - *Next action* - the one thing the next session does first.
- A role may add one section its work needs, such as "Ready to dispatch" for an agent that writes briefs. The screen
  limit still holds.
- `Updated:` carries the time of the rewrite, from `date '+%Y-%m-%d %H:%M'`. Boot compares it with the journal.

## Rewriting

Write the new STATUS from the old STATUS plus what happened since: this session, or after an unclean end the journal
lines newer than `Updated:`. Drop what is done, keep what is still true, and check every line against reality instead
of copying it forward.
