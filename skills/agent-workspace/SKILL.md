---
name: agent-workspace
description: Use when working inside an agent workspace (a directory with a workspace.toml, or a session started in one of its members/), when the user asks to create, set up, onboard, recreate, pause, or close a workspace, or to add, remove, or refresh a workspace member (git repo or file). Covers the layout, the workspace.toml manifest, members versus workspace files, and repairing broken members.
---

# Agent workspace

An agent workspace is a directory where agents make progress on one area of work, such as frontend bugs or a
refactoring, over many sessions. It is a git repo of its own and holds two kinds of content:

- **Members** are what the work is about: git repos and files from outside the workspace, each read-only or writable.
  `workspace.toml` lists them, and each one appears at `members/<name>`. Members are gitignored and built from the
  manifest on demand.
- **Workspace files** are everything else: `AGENTS.md`, `workspace.toml`, and whatever organizes the work and what is
  learned from it, such as a memory or task folders. They are versioned in the workspace repo.

So a workspace can be recreated from its repo alone: clone it and build the members from `workspace.toml`. What
cannot be rebuilt is uncommitted work inside members and anything outside git, so durable things belong in git repos.

Other skills add workspace files of their own: `agent-memory` keeps a memory in `memory/`, and `agent-teams` keeps
`STATUS.md`, `plans/`, and `tasks/`. This skill only defines where they go, not what is in them.

## Find your way in a workspace

1. Find the workspace root: the nearest directory at or above where you run that has a `workspace.toml`. A session
   started inside `members/<name>/` belongs to that workspace.
2. Read the root `AGENTS.md`: purpose, scope, done criteria, and which other skills the workspace uses.
3. Work on members through `members/<name>`, never through the source in `workspace.toml`. A member's `access`
   binds every agent.
4. If a member is missing or broken, see `references/troubleshooting.md` before anything else.

## Rules

- **Read-only means read-only.** Never write to a member with `access = "read"`, whatever its kind.
- **The user commits the workspace repo.** Never commit, stage, or push workspace files. Commits inside writable
  members are ordinary work and follow that repo's conventions.
- **Members stay out of the workspace repo.** Content the workspace should own, such as a copy of some documents, is a
  workspace file, not a member: import it once and version it.
- **Fill templates, do not invent formats.** Every file this skill defines has a template in `templates/`.

## References

Read a reference when its trigger fires, not before. Read it in full before acting on it.

- **Layout** (`references/layout.md`). You need to know where something lives, how members and workspace files are
  named, or who may write a path.
- **Lifecycle** (`references/lifecycle.md`). The user asks to create, onboard, recreate, pause, or close a workspace,
  or the workspace's `AGENTS.md` still has placeholders.
- **Members** (`references/members.md`). A member is added, removed, or refreshed, such as at the start of a session.
- **Troubleshooting** (`references/troubleshooting.md`). A member is missing or broken, the workspace or a source
  clone moved, a branch name collides, or a `git worktree` command fails.
