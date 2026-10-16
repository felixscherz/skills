---
name: agent-home
description: Use whenever you need somewhere to put files while working on a task - a scratch workspace, a document for the user to read (summary, implementation plan, investigation notes, review), a handoff note for another agent, or a place shared with other agents on the same task. Also use when the user says "write it to a file", "put the plan somewhere", "hand this off", mentions `ah`, or gives you a task ID like `task-auth-fix-k3x9m2qp`.
---

# Agent home

`ah` resolves where agent state lives. When you need a location, ask `ah`; never compute or guess one yourself. All
path rules live in `ah`, so they can change without touching any skill.

`ah` is a hard dependency for the agent that creates or resolves a task. If `command -v ah` fails, stop and tell the
user to install it with `go install github.com/felixscherz/ah@latest`. Do not fall back to another location. An
agent that was handed a task folder path needs neither `ah` nor this skill: it works in the folder it was given.

## Concepts

- A **context** is a directory, usually next to the repos it covers and never inside one. `ah context` prints it.
  It holds `context.md` (shared knowledge about this context), `cos/` (the chief of staff's home), and `tasks/`.
- A **task** is a folder under `tasks/`, named by its ID, for example `task-auth-fix-k3x9m2qp`. Use one for anything
  you produce while working that is not product code: documents for the user, scratch files, handoff notes, and
  shared state when several agents work on the same piece of work. A one-off analysis is a task too.

When nothing else resolves, `ah` uses a per-user fallback context. That is fine to work in. If `ah context` prints a
context that looks wrong, run `ah debug context`, show the user the relevant part, and let them fix the setup. Run
`ah init` only when the user asks for a new context, and only in a directory next to the repos, not inside one.

## Find or create the task

1. If you were given a task folder path, work in that folder. Read its `README.md` first.
2. If the user gave you a task ID, resolve it with `ah task path <id>`. Any unambiguous part of the ID works, like a
   short commit hash. Read the folder's `README.md` first.
3. Otherwise create one with `dir=$(ah task new <slug>)`, where the slug is a short kebab-case description such as
   `auth-token-refresh`. It prints the new folder. Do not reuse a task that belongs to unrelated work.

`ah task list --status open` shows the open tasks, oldest first.

An older `.agents/tasks/...` path from the user is a plain folder: work in it as given and do not move it.

## What goes in a task folder

`ah` owns `task.toml`. Never edit `status`, `created`, or `closed` by hand. The agent that owns the task may add its
own keys, such as a branch or a PR.

Every task folder has a `README.md`, so any agent or human opening it understands the task. It states the goal and,
once work stops, the outcome. For example:

```markdown
# Refresh auth tokens before expiry

Users get logged out mid-session because access tokens expire without being refreshed. Add background refresh
in the API client and cover it with tests.

Outcome: merged in PR #412. Refresh runs 60s before expiry.
```

Put everything else in the folder as files with descriptive names. Only edit files you created, unless you are
updating the README to reflect the current state.

## Status

The agent that created or resolved the task owns its status and changes it with
`ah task status <id> <open|blocked|done>`. An agent it hands work to reports progress back instead of setting the
status itself.

- `blocked` when the work waits on something outside your control, with the reason in the README.
- `done` when work on the task stops, whether it succeeded or not. Record the outcome in the README first.

## Documents for the user

When the user asks for a summary, plan, or write-up, write it to the task folder and give them the absolute path.
Write for a reader without your context and keep the chat reply to a short summary.

## Handing off to another agent

Give a subagent the absolute path of the task folder, plus the file it should write its result to. The subagent
works in that folder without calling `ah`, and you keep ownership of the task and its status.

When handing off to a new session through the user, write a handoff document in the task folder so a fresh agent with no
context can continue: the goal, current state, decisions made, where the work lives (repository, branch, files), open
questions, and skills to load. Reference existing files, specs, commits, or PRs instead of duplicating them. Leave out
secrets. Give the user the task ID and the folder path so they can pass it on. Ownership of the task, and its status,
moves to the agent that picks it up.

## Worktrees

Inside a worktree, `ah` finds the context through the primary checkout. Move a worktree only with
`git worktree move`. If `ah context` inside a worktree prints an unexpected context, run `git worktree repair` and
check again.

## Keep agent state out of shared writing

Do not cite task IDs or local paths in commit messages, pull request descriptions, or anything else read by people
who cannot open the local files. Inline the relevant content instead.

## Pruning

Keep tasks after they are done. Remove them only when the user asks, in two steps:

1. Run `ah task prune --older-than <age>`, for example `30d`, and show the user the folders it lists.
2. Only after the user approves that list, run the same command with `--delete`.
