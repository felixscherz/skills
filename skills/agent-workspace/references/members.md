# Members

Adding, refreshing, and removing members. What each kind of member is built as is in `layout.md`; the entry format is
in `../templates/workspace.toml`.

Use absolute paths for every target below. `<ws>` is the workspace root, `<member>` the member's name, `<git>` a local
clone from a `git` entry, and `<prefix>` the entry's `branch_prefix`.

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

### Git, local clone

Writable: the workspace works on its own branch. Git refuses to check out one branch in two worktrees, so the prefix
is what lets two workspaces work on the same repo.

```sh
git -C <git> worktree add -b <prefix>main <ws>/members/<member> origin/<branch>
```

If `<prefix>main` already exists, such as when recreating the workspace, check out the existing branch instead:

```sh
git -C <git> worktree add <ws>/members/<member> <prefix>main
```

Read-only: a detached worktree, so the workspace sees `<branch>` cleanly even when the user's checkout is on another
branch or has uncommitted changes.

```sh
git -C <git> worktree add --detach <ws>/members/<member> origin/<branch>
```

If `worktree add` fails, see `troubleshooting.md`.

### Git, URL

The workspace gets its own clone. Writable members get a blobless clone, which keeps the history needed to rebase and
push but downloads file contents only when needed:

```sh
git clone --filter=blob:none <git> <ws>/members/<member>
git -C <ws>/members/<member> switch -c <prefix>main origin/<branch>
```

If the remote already has `<prefix>main`, such as when recreating the workspace, use
`git -C <ws>/members/<member> switch <prefix>main` instead, which tracks it. If the server does not support filters,
git warns and makes a full clone, which works the same.

Read-only members get a shallow clone, detached:

```sh
git clone --depth 1 <git> <ws>/members/<member>                    # follows the default branch
git clone --depth 1 --branch <branch> <git> <ws>/members/<member>  # when the entry sets branch
git -C <ws>/members/<member> checkout --detach
```

### Path

A directory or a single file, used in place through a symlink. Path members are always read-only. If the workspace
needs to write them, ask the user to make them a git repo first.

```sh
test -e <absolute path> && ln -s <absolute path> <ws>/members/<member>
```

Expand `~` in the link target. Keep `~` in `workspace.toml`.

### Record it

Add a `[[members]]` entry to `workspace.toml` with `name`, the source key (`git` or `path`), `access`, and for writable
git members `branch_prefix`. Add `branch` only when the user names one.

## Refresh members

Run this at the start of a session, so the work starts from the latest state. For each entry in `workspace.toml`:

- **Writable git members:** rebase onto the latest `<branch>`.
  ```sh
  git -C <ws>/members/<member> fetch origin
  git -C <ws>/members/<member> rebase origin/<branch>
  ```
  Skip a member with uncommitted changes. If a rebase conflicts, run `git rebase --abort` and report the conflict
  instead of resolving it unasked.
- **Read-only git members:** move to the latest `<branch>`. A URL member is a shallow clone, so fetch it with
  `--depth 1` to keep it shallow.
  ```sh
  git -C <ws>/members/<member> fetch origin               # URL members: fetch --depth 1 origin
  git -C <ws>/members/<member> checkout --detach origin/<branch>
  ```
  If a read-only member has changes, something wrote to it. Report it; do not discard the changes.
- **Path members:** check that `<ws>/members/<member>` still resolves with `test -e`. Report a missing target.

A member that is missing altogether is built as in "Add a member".

## Remove a member

1. For a writable git member, check `git status` and for commits not on any remote
   (`git -C <ws>/members/<member> log --oneline --branches --not --remotes`). If there are any, ask the user before
   going on.
2. Remove it from `members/`:
   - Git, local clone: `git -C <git> worktree remove <ws>/members/<member>`. For a writable member, ask the user
     whether to delete the workspace's branches under `<prefix>` in the source clone.
   - Git, URL: delete the directory `<ws>/members/<member>`.
   - Path: `rm <ws>/members/<member>`, which removes only the link. Never pass `-r` or a trailing slash: that deletes
     the files the link points to.
3. Remove the `[[members]]` entry from `workspace.toml`.
