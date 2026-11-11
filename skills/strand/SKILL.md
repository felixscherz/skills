---
name: strand
description: Use when work spans several repositories and needs a short-lived home folder (a strand) instead of starting the agent in a parent directory, when the user asks to create, start, attach a repo to, resume, pick up, or close a strand, or names one. Not needed for ordinary work inside a strand folder, whose AGENTS.md explains everything; load it there only to attach a repo or close the strand.
argument-hint: "[new <name> | attach <repo> | close]"
---

# Strand

A strand is one folder for one piece of work that crosses repository boundaries. It lives for as long as the task
does, days rather than months, and is closed when the task is done. It holds git worktrees of the repositories the
work touches, plus a few files that let any agent started in the folder pick the work up: `AGENTS.md` explains the
strand, `STATUS.md` says where it stands, and `journal/` says what happened.

```
<strand>/                  # git repo of its own, for the strand's files only
├── AGENTS.md              # explains the strand to any agent started here
├── STATUS.md              # snapshot of the work, plus the repos table
├── journal/
│   └── YYYY-MM-DD-HHMM.md # one entry per session
└── repos/                 # excluded from the strand repo
    ├── <repo>/            # worktree or clone on branch strand/<name>
    └── ...
```

Folder names under `repos/` equal the source repositories' directory names, so relative paths between sibling repos
still resolve.

## Rules

- **Never touch the source checkout.** Work happens in `repos/<repo>`. The user's own clone, its branches other than
  `strand/<name>`, and its uncommitted changes stay as they are.
- **The user merges.** Never merge a PR or push to a base branch. Push `strand/<name>` and open PRs only when the user
  asks or `AGENTS.md` allows it.
- **Commit the strand's files in the strand repo.** `AGENTS.md`, `STATUS.md`, and `journal/` are committed in the
  strand folder itself. Code commits go into `repos/<repo>` and follow that repo's conventions.
- **Nothing is deleted on close without checks.** Uncommitted changes, unpushed commits, and unmerged branches are
  reported to the user before anything is removed.
- **No secrets** in strand files.
- **Fill templates, do not invent formats.** `templates/` has every file this skill writes. Replace each
  `{{placeholder}}`.

## New

1. Get from the user: a name (kebab-case, it becomes the branch `strand/<name>`), a one-line goal, and where the
   strand folder goes. There is no default location yet, so always ask; suggest the parent directory of the last
   strand they used if you know it. The folder must not exist or must be empty.
2. Create the folder, `git init` it, and add `repos/` to `.git/info/exclude`.
3. Write from the templates: `AGENTS.md` (name and goal filled in, permissions as the user states them, defaulting to
   "push and draft PRs only when asked") and `STATUS.md` with an empty repos table. Create `journal/` with an empty
   `.gitkeep`.
4. Attach each repository the user names (below).
5. Commit the strand's files, and tell the user the path to start agents in.

## Attach a repository

The source is a local clone path or a URL that `git clone` accepts. `<repo>` is the source's directory name, or the
URL's last path segment without `.git`. Stop and ask if `repos/<repo>` already exists.

**Local clone, as a worktree:**

1. Find the base. With an `origin` remote: `git -C <source> fetch origin`, then the default branch from
   `git -C <source> symbolic-ref --short refs/remotes/origin/HEAD` (for example `origin/main`). If that fails, ask.
   Without a remote: the local default branch (`main` or `master`), or ask. The user may name a different base.
2. If `strand/<name>` already exists in the source, stop and ask: it may belong to an earlier strand of that name.
3. `git -C <source> worktree add -b strand/<name> <strand>/repos/<repo> <base>`

**URL, as a clone:**

1. `git clone <url> <strand>/repos/<repo>`
2. Base is `origin/<default branch>`, found as above. `git -C repos/<repo> switch -c strand/<name> <base>`

Then add a row to the repos table in `STATUS.md`: repo, source (absolute path or URL), mode (`worktree` or `clone`),
branch, and base. The table is the manifest that closing reads, so keep it exact.

## Resume

An agent started in the strand reads `AGENTS.md`, which tells it to read `STATUS.md` and the latest journal entry.
When the user asks to pick up a strand by name and you are elsewhere, ask for its path, then do the same. Check that
each repo in the table still exists under `repos/`; a missing one is a question for the user, not something to
re-create silently.

## End of a session

`AGENTS.md` tells every agent to do this itself. When you work in a strand, do it too:

1. Write the session's journal entry from `templates/journal-entry.md`.
2. Rewrite `STATUS.md` as a snapshot of now. Keep the repos table.
3. Commit the strand's files in the strand repo.

## Close

When the task is done or abandoned:

1. For each repo in the table, check and report:
   - uncommitted changes: `git -C repos/<repo> status --porcelain`
   - commits not on the remote: `git -C repos/<repo> log --oneline @{u}..` when it has an upstream, else
     `git -C repos/<repo> log --oneline <base>..HEAD`
   - whether the branch is merged into the base, and any open PR for it (`gh pr list --head strand/<name>` when the
     remote is on GitHub).
2. Ask the user what to do with anything found. Do not continue past a repo with unsaved work until they decide.
3. Remove each repo:
   - worktree: `git -C <source> worktree remove <strand>/repos/<repo>`, without `--force`. Then delete the branch
     with `git -C <source> branch -d strand/<name>` only if it is merged or the user says so; otherwise leave it and
     say so.
   - clone: delete `repos/<repo>` only after step 1 showed nothing unsaved, and with the user's confirmation.
4. Write a last journal entry, set `Status: closed` in `STATUS.md`, and keep the repos table as a record of what the
   strand touched. Commit. The strand folder stays as an archive; the user may delete it.

If a source clone moved or is gone, `git worktree remove` fails. Remove the folder under `repos/` after the step 1
checks and run `git -C <source> worktree prune` once the source is found again.
