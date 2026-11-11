# Strand: {{name}}

This folder is a strand: a short-lived home for one piece of work that spans several repositories. You do not need
any skill to work here; this file explains everything. Load the `strand` skill only to attach another repository or
to close the strand.

## Goal

{{goal}}

## Start here

1. Read `STATUS.md`: where the work stands, what is next, and the repos table.
2. Read the latest entry in `journal/` (the file names sort by time).
3. Then do what the user asks. If `STATUS.md` and the user disagree, the user wins; mention the difference.

## Layout

- `repos/<repo>/` - a git worktree or clone of each repository, on branch `strand/{{name}}`. All code changes happen
  here. Each repo's own `AGENTS.md` or `CLAUDE.md` applies inside it.
- `STATUS.md` - a snapshot of the work. The repos table at its end lists where each repo came from and its base
  branch.
- `journal/YYYY-MM-DD-HHMM.md` - one entry per session, what was asked, done, decided, and left open.
- The strand folder is a git repo of its own for these files only; `repos/` is excluded from it.

## Rules

- Commit code inside `repos/<repo>` with `git -C repos/<repo> ...`, following that repo's conventions. Commit the
  strand's own files (`AGENTS.md`, `STATUS.md`, `journal/`) in the strand folder itself, never inside `repos/`.
- Never work in the source checkouts listed in the repos table, only in `repos/`.
- Never merge a PR or push to a base branch.
- Push: {{e.g. "only when the user asks", or "the strand branch freely"}}
- Pull requests: {{e.g. "draft, only when the user asks"}}
- Out of scope: {{what this strand must not change | "nothing beyond the goal"}}
- If the work turns out to need a repository that is not under `repos/`, tell the user instead of editing it
  elsewhere.
- If other agents work in this strand at the same time, only the one the user named as lead rewrites `STATUS.md`.
  Everyone writes their own journal entry.

## Before you stop

After a meaningful chunk of work, or when the user wraps up:

1. Write a journal entry named after the current time, `journal/YYYY-MM-DD-HHMM.md`. If you already wrote one this
   session, append to it. Never edit another session's entry; correct it in a new one.

   ```markdown
   # YYYY-MM-DD HH:MM

   ## Asked
   ## Done
   ## Decided
   ## Open
   ```

   Name files, branches, commits, and PRs so a reader can trace them. Give decisions with their reasons.
2. Rewrite `STATUS.md` so it describes now, not history. Keep its sections and the repos table; write "None." under an
   empty section.
3. Commit the strand's files in the strand folder.
