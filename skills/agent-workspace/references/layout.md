# Layout

The single place that defines where things live in a workspace and who may write them. File formats live in
`../templates/`.

## Tree

```
<workspace>/                 # git repo
├── .gitignore               # members/
├── AGENTS.md                # purpose, scope, done criteria, skills in use
├── CLAUDE.md -> AGENTS.md
├── workspace.toml           # name, purpose, status, members
├── members/                 # gitignored, one entry per member
│   ├── web-app/             # worktree or clone, writable
│   ├── design-system/       # worktree, read-only
│   └── brand-guide          # symlink, read-only
└── ...                      # other workspace files, added by the skills that own them
```

| Path | Purpose | Template |
| --- | --- | --- |
| `.gitignore` | Keeps `members/` out of the workspace repo | `gitignore` |
| `AGENTS.md` | What the workspace is for, scope, done criteria, and sections other skills add | `AGENTS.md` |
| `workspace.toml` | The manifest: metadata and members | `workspace.toml` |
| `members/<name>` | A member, built from its `workspace.toml` entry | - |

Paths other skills own, as an index:

| Path | Owner skill |
| --- | --- |
| `memory/` | `agent-memory` |
| `STATUS.md`, `plans/`, `tasks/` | `agent-teams` |

Anything not under `members/` is a workspace file and is versioned. Do not put files of your own into `members/`.

## Members

Each member has a `name`, exactly one source key, and `access`. The format and an example of each kind are in
`../templates/workspace.toml`.

| Source | Access | Built as |
| --- | --- | --- |
| `git`, local clone | write | worktree on `<branch_prefix>main` |
| `git`, local clone | read | detached worktree at `origin/<branch>` |
| `git`, URL | write | blobless clone (`--filter=blob:none`) on `<branch_prefix>main` |
| `git`, URL | read | shallow clone (`--depth 1`), detached |
| `path` | read | symlink to the absolute path |
| `path` | write | not allowed |

- `git` is a URL when it has a scheme (`https://`, `ssh://`, `file://`) or the form `user@host:path`. Anything else is
  a path to a local clone.
- `<branch>` is the entry's `branch`, or the remote's default branch when it has none.
- `branch_prefix` is required for writable git members and unused otherwise. `<branch_prefix>main` is the workspace's
  integration line in that repo, and every other branch the workspace creates there goes under the same prefix. The
  prefix keeps two workspaces apart in a shared clone and on a shared remote. Default it to `<workspace name>/`.
- Read-only git members get a worktree or clone of their own instead of a link to the user's checkout, which may be on
  a feature branch or have uncommitted changes.
- `path` members are read-only because files outside git have no diff, no undo, and no isolation. To let a workspace
  write them, make them a git repo first.

## Write permissions

A member's `access` binds every agent. Workspace files are written by the skill that owns them, under that skill's
rules; `AGENTS.md` and `workspace.toml` change only together with the user.

No agent commits the workspace repo. The user does.

## Names

- Workspace names and member names are kebab-case. Member names are unique within the workspace.
- `~` stays as written in `workspace.toml`; expand it to the home directory only when running a command.
