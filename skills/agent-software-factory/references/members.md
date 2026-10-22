# Members

Adding, refreshing, and removing members. What each kind of member is built as is in `layout.md`; the entry format is
in `../templates/factory.toml`.

Use absolute paths for every target below. `<ws>` is the factory root, `<member>` the member's name, `<git>` a local
clone from a `git` entry, and `<prefix>` the entry's `branch_prefix`. Resolve a relative `git` path from `<ws>`, such
as `..` for an embedded factory's host, to an absolute path before running a command.

## Add a member

Create `<ws>/members/` if it does not exist yet. Then build the member by its kind, and record it.

### Git: find the branch

`<branch>` is the entry's `branch` if set, otherwise the remote's default branch. For a local clone, find the default
like this:

```sh
git -C <git> fetch origin
git -C <git> symbolic-ref --short refs/remotes/origin/HEAD   # prints origin/<default>
```

If there is no `origin/HEAD`, run `git -C <git> remote set-head origin --auto` and try again. If that fails too, ask the
user which branch is the base. For a URL, the clone below sets `origin/HEAD`; read it the same way inside the clone.

A local clone without a remote (`git -C <git> remote` prints nothing) has nothing to fetch, and its `<base>` is the
local `<branch>` (see `layout.md`). Set `branch` in its entry: the branch the user names, or by default the one the
clone has checked out, from `git -C <git> branch --show-current`. Tell the user that its work is handed over as
branches, since there is nowhere to push or open a PR.

### Git, local clone

Writable: the factory works on its own branch. Git refuses to check out one branch in two worktrees, so the prefix
is what lets two factories work on the same repo.

```sh
git -C <git> worktree add -b <prefix>main <ws>/members/<member> <base>
```

If `<prefix>main` already exists, such as when recreating the factory, check out the existing branch instead:

```sh
git -C <git> worktree add <ws>/members/<member> <prefix>main
```

Read-only: a detached worktree, so the factory sees `<branch>` cleanly even when the user's checkout is on another
branch or has uncommitted changes.

```sh
git -C <git> worktree add --detach <ws>/members/<member> <base>
```

If `worktree add` fails, see `troubleshooting.md`.

### Git, URL

The factory gets its own clone. Writable members get a blobless clone, which keeps the history needed to rebase and
push but downloads file contents only when needed:

```sh
git clone --filter=blob:none <git> <ws>/members/<member>
git -C <ws>/members/<member> switch -c <prefix>main origin/<branch>
```

If the remote already has `<prefix>main`, such as when recreating the factory, use
`git -C <ws>/members/<member> switch <prefix>main` instead, which tracks it. If the server does not support filters,
git warns and makes a full clone, which works the same.

Read-only members get a shallow clone, detached:

```sh
git clone --depth 1 <git> <ws>/members/<member>                    # follows the default branch
git clone --depth 1 --branch <branch> <git> <ws>/members/<member>  # when the entry sets branch
git -C <ws>/members/<member> checkout --detach
```

### Path

A directory or a single file, used in place through a symlink. Path members are always read-only. If the factory
needs to write them, ask the user to make them a git repo first.

```sh
test -e <absolute path> && ln -s <absolute path> <ws>/members/<member>
```

Expand `~` in the link target. Keep `~` in `factory.toml`.

### Record it

Add a `[[members]]` entry to `factory.toml` with `name`, the source key (`git` or `path`), `access`, and for writable
git members `branch_prefix`. Add `branch` only when the user names one.

## Refresh members

Run this at the start of a session, so the work starts from the latest state. For each entry in `factory.toml`:

- **Writable git members:** rebase onto the latest `<branch>`. Without a remote, skip the fetch: the local
  `<branch>` moves as the user commits to it.
  ```sh
  git -C <ws>/members/<member> fetch origin
  git -C <ws>/members/<member> rebase <base>
  ```
  Skip a member with uncommitted changes. If a rebase conflicts, run `git rebase --abort` and report the conflict
  instead of resolving it unasked.
- **Read-only git members:** move to the latest `<branch>`. A URL member is a shallow clone, so fetch it with
  `--depth 1` to keep it shallow.
  ```sh
  git -C <ws>/members/<member> fetch origin               # URL members: fetch --depth 1 origin; no remote: skip
  git -C <ws>/members/<member> checkout --detach <base>
  ```
  If a read-only member has changes, something wrote to it. Report it; do not discard the changes.
- **Path members:** check that `<ws>/members/<member>` still resolves with `test -e`. Report a missing target.

A member that is missing altogether is built as in "Add a member".

## Remove a member

1. For a writable git member, check `git status` and for commits not on any remote
   (`git -C <ws>/members/<member> log --oneline --branches --not --remotes`), or without a remote for branches not
   merged into the base (`git -C <git> branch --no-merged <branch> --list '<prefix>*'`), and for backlog items on it
   that are `in-progress` or `in-review`. If there are any, ask the user before going on. Remove the item checkouts
   under `<ws>/checkouts/` before the member itself.
2. Remove it from `members/`:
   - Git, local clone: `git -C <git> worktree remove <ws>/members/<member>`. For a writable member, ask the user
     whether to delete the factory's branches under `<prefix>` in the source clone.
   - Git, URL: delete the directory `<ws>/members/<member>`.
   - Path: `rm <ws>/members/<member>`, which removes only the link. Never pass `-r` or a trailing slash: that deletes
     the files the link points to.
3. Remove the `[[members]]` entry from `factory.toml`.
