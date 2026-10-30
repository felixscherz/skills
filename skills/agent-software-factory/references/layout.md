# Layout

The single place that defines where things live in a factory and who may write them. File formats live in
`../templates/`.

## Tree

```
<factory>/                   # git repo
├── .gitignore               # members/, checkouts/, tasks/*/checkout/
├── AGENTS.md                # who you are, purpose, scope, permissions
├── factory.toml             # name, purpose, status, members
├── STATUS.md                # the factory agent's report on the current state
├── memory/
│   ├── README.md
│   ├── journal/
│   ├── notes/
│   └── inbox/
├── backlog/
│   └── NNNN-slug.md         # one file per item
├── members/                 # gitignored, one entry per member
│   ├── web-app/             # worktree or clone, writable
│   ├── design-system/       # worktree, read-only
│   └── brand-guide          # symlink, read-only
├── checkouts/               # gitignored
│   └── NNNN-slug/<member>/  # worktree for one backlog item, on its own branch
├── plans/                   # only when orchestrating, see working-as-an-agent-team
└── tasks/                   # only when orchestrating, see working-as-an-agent-team
```

| Path | Purpose | Template |
| --- | --- | --- |
| `.gitignore` | Keeps members and checkouts out of the factory repo | `gitignore` |
| `AGENTS.md` | Who you are, what the factory is for, scope, and permissions | `AGENTS.md` |
| `factory.toml` | The manifest: metadata and members | `factory.toml` |
| `STATUS.md` | A snapshot of the work, rewritten at the end of every session | `STATUS.md` |
| `memory/README.md` | What the memory is for, and an index of the notes | `memory-README.md` |
| `memory/journal/YYYY-MM-DD-HHMM.md` | What happened in one session | `memory.md` |
| `memory/notes/<topic>.md` | Durable knowledge, one topic per file | - |
| `memory/inbox/YYYY-MM-DDTHHMM-slug.md` | Raw input waiting for consolidation | `inbox-item.md` |
| `backlog/NNNN-slug.md` | One piece of work and its status | `backlog-item.md` |
| `members/<name>` | A member, built from its `factory.toml` entry | - |
| `checkouts/<item id>/<member>` | A worktree for one backlog item | - |

`plans/` and `tasks/` belong to the `working-as-an-agent-team` skill and exist only once it was used here.

Anything not under `members/` or `checkouts/` is a factory file and is versioned. Do not put files of your own into
`members/`.

## Embedded factory

An embedded factory has the same tree, rooted at `<repo root>/.factory/` in the repository it works on (the host):

- It is a git repo of its own, nested in the host's working tree. The host's local exclude file,
  `$(git rev-parse --git-common-dir)/info/exclude`, lists `.factory/`, so the host repo never sees it and its
  `.gitignore` stays untouched.
- The host is a writable git member like any other, with `git = ".."`, a path relative to the factory root. Its
  worktree, `members/<host name>`, is on `<branch_prefix>main`, so the factory never writes the user's own checkout.
- Find it from `git rev-parse --show-toplevel` of the session's directory, and check `<repo root>/.factory/factory.toml`
  directly. Tools that skip hidden or git-ignored paths can omit `.factory/` and everything in it, so a search from the
  host's root that finds nothing does not mean it is missing. To search the factory's files, point the tool at
  `.factory/` itself. Nothing in the host refers to it, so it takes effect only when this skill or
  `working-as-an-agent-team` is loaded.

## Members

Each member has a `name`, exactly one source key, and `access`. The format and an example of each kind are in
`../templates/factory.toml`.

| Source | Access | Built as |
| --- | --- | --- |
| `git`, local clone | write | worktree on `<branch_prefix>main` |
| `git`, local clone | read | detached worktree at `<base>` |
| `git`, URL | write | blobless clone (`--filter=blob:none`) on `<branch_prefix>main` |
| `git`, URL | read | shallow clone (`--depth 1`), detached |
| `path` | read | symlink to the absolute path |
| `path` | write | not allowed |

- `git` is a URL when it has a scheme (`https://`, `ssh://`, `file://`) or the form `user@host:path`. Anything else is
  a path to a local clone. A relative path resolves from the factory root, such as `..` for an embedded factory's
  host.
- `<branch>` is the entry's `branch`, or the remote's default branch when it has none. It is the member's base branch:
  backlog items branch from it and their PRs target it.
- `<base>` is the ref work starts from: `origin/<branch>`, or the local `<branch>` when the member is a local clone
  without a remote. A member without a remote needs `branch` in its entry, and hands over its work as branches instead
  of PRs (see "Work an item" in `backlog.md`). Skip every `fetch` for it.
- `branch_prefix` is required for writable git members and unused otherwise. `<branch_prefix>main` is the factory's
  integration line in that repo, and every other branch the factory creates there goes under the same prefix, such as
  `<branch_prefix><item id>` for a backlog item. The prefix keeps two factories apart in a shared clone and on a shared
  remote. Default it to `<factory name>/`.
- Read-only git members get a worktree or clone of their own instead of a link to the user's checkout, which may be on
  a feature branch or have uncommitted changes.
- `path` members are read-only because files outside git have no diff, no undo, and no isolation. To let a factory
  write them, make them a git repo first.

## Write permissions

| Path | Who writes it |
| --- | --- |
| `AGENTS.md`, `factory.toml` | The factory agent, only together with the user |
| `STATUS.md`, `backlog/`, `memory/` except `inbox/` | The factory agent |
| `memory/inbox/` | The factory agent and workers |
| `plans/`, `tasks/` | As `working-as-an-agent-team` says |
| Writable members and `checkouts/` | The factory agent, and workers where their brief allows |

A member's `access` binds every agent. No agent commits the factory repo. The user does.

## Names

- Factory names and member names are kebab-case. Member names are unique within the factory.
- `~` stays as written in `factory.toml`; expand it to the home directory only when running a command.
