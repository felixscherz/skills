---
name: agent-software-factory
description: Use when working in a software factory (a directory with a factory.toml, a session started in one of its members/, or a repository's embedded factory at .factory/ when the user asks to work in it) - at the start and end of every session there, when the user asks to create (also inside a repository), onboard, recreate, pause, or close a factory, to add, remove, or refresh a member, to find work, to add, approve, reject, or work a backlog item, to follow up on its pull request or review branch, to remember something, or to consolidate the memory. Not for workers following a BRIEF.md.
---

# Agent software factory

A software factory is a directory where one agent improves codebases over many sessions. It finds work, keeps it in a
backlog, works approved items into pull requests, and learns from how they are received. That agent, the factory
agent, is the user's only contact point and owns everything in the factory. It may delegate work to workers when the
work calls for it (see "Orchestrate larger work").

The factory is a git repo of its own and holds two kinds of content:

- **Members** are what the work is about: git repos and files from outside the factory, each read-only or writable.
  `factory.toml` lists them, and each one appears at `members/<name>`. Members are gitignored and built from the
  manifest on demand.
- **Factory files** are everything else: `AGENTS.md`, `factory.toml`, `STATUS.md`, the memory, and the backlog. They
  are versioned in the factory repo.

So a factory can be recreated from its repo alone: clone it and build the members from `factory.toml`. What cannot be
rebuilt is uncommitted work inside members and anything outside git, so durable things belong in git repos.

A factory usually lives in a directory of its own. An **embedded factory** lives at `<repo root>/.factory/` inside the
one repository it works on, as a separate git repo that the repository's local exclude file keeps out of it. It is
for working on a repository without setting up a factory elsewhere. Nothing in the repository points to it, so only an
agent that loads this skill or `working-as-an-agent-team` uses it. See "Embedded factory" in `references/layout.md`.

```
<factory>/
├── AGENTS.md        # who you are, purpose, scope, permissions
├── factory.toml     # the manifest: metadata and members
├── STATUS.md        # the factory agent's report on the current state
├── memory/          # knowledge: what is true, what the user wants, what happened
├── backlog/         # work: one file per item, with its status
├── members/         # gitignored, one entry per member
└── checkouts/       # gitignored, one worktree per backlog item being worked
```

The memory and the backlog are kept apart on purpose. The memory holds knowledge, which is rewritten when it stops
being true. The backlog holds work, which moves through statuses and links to branches and PRs.

## Rules

- **The user approves work.** Work only on backlog items the user approved. Finding and proposing work is always
  fine; starting it is not. Approval covers the described outcome and approach, not every prerequisite later
  discovered. Reassess cumulative scope when new information materially increases the work, even inside the same
  repository with no product behavior change. Bring that decision back to the user before continuing affected work.
- **The user merges.** Never merge a PR, merge into a member's base branch, or push to it. Push and open PRs only as
  the permissions in `AGENTS.md` allow.
- **Read-only means read-only.** Never write to a member with `access = "read"`, whatever its kind.
- **The user commits the factory repo.** Never commit, stage, or push factory files. Commits inside writable members
  are ordinary work and follow that repo's conventions.
- **One owner.** Only the factory agent writes `STATUS.md`, the backlog, and the memory's README, journal, and notes.
  Workers write only to the memory's inbox and the paths their brief allows.
- **Members stay out of the factory repo.** Content the factory should own, such as a copy of some documents, is a
  factory file, not a member: import it once and version it.
- **No secrets.** Credentials, tokens, and personal data never go into a factory file.
- **Fill templates, do not invent formats.** Every file this skill defines has a template in `templates/`.

## Start of a session

1. Find the factory root: the nearest directory at or above where you run that has a `factory.toml`. A session started
   inside `members/<name>/` belongs to that factory. In a repository with no factory above it, the factory root is
   `<repo root>/.factory/` if it has a `factory.toml`. Unless the user mentioned the factory or asked for team work
   (see `working-as-an-agent-team`), confirm with them that they mean to work in it.
2. Read `AGENTS.md` and `STATUS.md`.
3. Read the memory's README and latest journal entry, and the notes relevant to what the user wants now.
4. Refresh the members (see `references/members.md`). If one is missing or broken, see
   `references/troubleshooting.md` before anything else.
5. Follow up on items in review (see "Follow up on reviews" in `references/backlog.md`).
6. If `tasks/` holds open tasks or a plan is running, load the `working-as-an-agent-team` skill and follow its lead's
   start of a session as well.
7. Give the user a short report: what happened to items in review, what is in progress, which proposed items wait for
   their decision, how many inbox items wait, and problems with members.

If `AGENTS.md` still has placeholders, onboard the factory first (see `references/lifecycle.md`).

## During a session

- When the user states a preference, corrects you, or settles a decision that will matter again, write it into the
  matching note right away.
- Work you or the user notice goes into the backlog as a proposed item. Anything else worth keeping that you cannot
  settle now, such as a finding or an open question, goes into the memory's inbox. Do not stop to consolidate.

## End of a session

When the user wraps up, or before you stop after a meaningful chunk of work:

1. Write the session's journal entry (see `references/memory.md`).
2. Rewrite `STATUS.md` from `templates/STATUS.md`. It is a snapshot, not a log: keep the sections fixed, write "None."
   under an empty one, and keep it short enough to read in a minute.
3. Tell the user what changed in the factory, so they can commit it.

## Orchestrate larger work

Work an item yourself when it fits one reviewable PR. When an item is larger than one agent should carry, or the user
wants several items worked in parallel, load the `working-as-an-agent-team` skill. It plans the work for delegation and
runs it through workers, in `plans/` and `tasks/` of this factory. The backlog item links to its plan.

## References

Read a reference when its trigger fires, not before. Read it in full before acting on it.

- **Layout** (`references/layout.md`). You need to know where something lives, how members and factory files are
  named, or who may write a path.
- **Lifecycle** (`references/lifecycle.md`). The user asks to create, onboard, recreate, pause, or close a factory, or
  `AGENTS.md` still has placeholders.
- **Members** (`references/members.md`). A member is added, removed, or refreshed, such as at the start of a session.
- **Troubleshooting** (`references/troubleshooting.md`). A member is missing or broken, the factory or a source clone
  moved, a branch name collides, or a `git worktree` command fails.
- **Memory** (`references/memory.md`). Writing a note, an inbox item, or a journal entry, setting up the memory, or
  consolidating it, such as when the user asks or the factory is about to close.
- **Backlog** (`references/backlog.md`). Finding work, adding, approving, rejecting, or working a backlog item, and
  following up on its review.
