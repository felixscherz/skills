# Troubleshooting

Fixes for the things that break around members. Report what you found and did to the user; when a fix could lose work,
ask first.

`<git>` below is a member's local clone, from its `git` entry in `factory.toml`. Members cloned from a URL and path
members have no separate clone, so the worktree sections do not apply to them.

## The factory or a source clone moved

Worktrees store absolute paths: the worktree's `.git` file points to the source clone, and the source clone records
where each worktree lives. Moving either breaks one side of the link.

- **The factory moved.** Git still works inside the worktrees, but the source clone lists them at their old path as
  prunable, and a `git worktree prune` would drop them. Run `git -C <git> worktree repair <new worktree path>` for
  each worktree. Clones of URL members and the symlinks of path members move without trouble.
- **A source clone moved.** Git commands in its worktrees fail with "not a git repository". Run
  `git -C <new git> worktree repair <worktree path>` for each worktree of that repo, and update `git` in each
  `factory.toml` that names it.

Check the result with `git -C <git> worktree list`.

## A worktree directory is missing

If `members/<member>` was deleted, the source clone still lists it. Run `git -C <git> worktree prune` to drop the
stale entry, then add the member again (see `members.md`). For a writable member, the factory's branch survives in
the source clone, so check it out instead of creating a new one:

```sh
git -C <git> worktree add <ws>/members/<member> <prefix>main
```

A missing clone of a URL member is cloned again. Commits on it that were never pushed are lost.

## A path member's target is missing

The symlink in `members/` survives, but `test -e members/<member>` fails: the directory or file was moved, renamed, or
deleted. Ask the user where it is now. If it moved, point the link at the new place and update `path` in
`factory.toml`:

```sh
ln -sfn <new absolute path> <ws>/members/<member>
```

If it is gone, remove the member (see `members.md`).

## The branch already exists

`worktree add -b` fails when `<prefix>main` already exists in the source clone. That usually means an earlier
factory of the same name, or a removed worktree, left it behind.

- Check what is on it: `git -C <git> log --oneline origin/<branch>..<prefix>main`.
- If it is this factory's work, check it out without `-b` (see `members.md`).
- Otherwise ask the user whether to delete it, or to pick another prefix.

## The branch is checked out elsewhere

`worktree add` refuses a branch that another worktree has checked out. Find it with `git -C <git> worktree list`.
Two factories must never share a branch; if this happens, the branch prefix in one `factory.toml` is wrong.

## The source has no remote

Without `origin`, there is nothing to fetch or rebase onto. Branch from the local default branch instead, or for a
read-only member detach at it, and tell the user that refreshing does not apply to this member.
