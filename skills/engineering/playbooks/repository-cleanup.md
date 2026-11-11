# Repository cleanup

Find the worktrees and local branches that past tasks left behind and remove the ones whose work is safe in the
default branch or no longer wanted. Agents start a branch or worktree for every task (`../references/worktrees.md`),
and nothing removes them once the work is merged, so they pile up. The risk runs one way: a stale branch left in
place costs nothing, a branch deleted with unpushed work loses it. When the evidence is unclear, keep the branch and
say why.

## Applies when

The user asks to clean up, prune, or tidy worktrees or branches, or asks which of them are stale. The scope is the
current repository unless the user names others. Remote branches are out of scope unless the user asks for them.

## Who decides

- The agent takes the inventory and classifies every worktree and branch on its own, read-only apart from fetching.
- The user approves the removal list before anything is removed. The approval covers that list only: an item found
  later goes back to the user.
- The agent never removes the primary checkout, the default branch, the branch checked out in the primary checkout,
  or a locked worktree, and never forces a removal of a worktree with uncommitted or untracked changes.
- Deleting a branch on the remote is outward-facing and needs the user's explicit request, separate from approving
  local cleanup.

## Steps

1. Update the view of the remote with `git fetch --prune`, so deleted remote branches show as gone. Find the default
   branch with `git symbolic-ref --short refs/remotes/origin/HEAD`, and compare everything against the remote's
   default branch, not the local one, which may be behind.
2. List the worktrees with `git worktree list --porcelain`. For each, note its branch or detached commit, whether it
   is locked or prunable, the output of `git -C <path> status --porcelain`, and the date of its last commit. Also list
   directories under `.worktrees/` that no worktree points to.
3. List the local branches with
   `git for-each-ref refs/heads --format='%(refname:short) %(upstream:short) %(upstream:track) %(committerdate:iso)'`.
4. Classify each branch by what its own commits are worth, using the first category that fits:
   - **Merged.** The tip is reachable from the default branch (`git merge-base --is-ancestor <branch>
     origin/<default>`), or the branch was squash- or rebase-merged: `git merge-tree --write-tree origin/<default>
     <branch>` prints the default branch's own tree (`git rev-parse origin/<default>^{tree}`), so merging adds
     nothing. A merged PR whose head commit equals the branch tip (`gh pr list --head <branch> --state merged --json
     headRefOid`) is the same evidence. A branch whose tip is an ancestor because it has no commits of its own is
     **Empty**, not Merged: it may be a task that just started.
   - **Gone.** It had an upstream and `%(upstream:track)` says `[gone]`, but it is not merged. The remote branch was
     deleted, which happens when a PR is closed without merging, so the commits may still matter. List them with
     `git log --oneline origin/<default>..<branch>`.
   - **Local only.** It never had an upstream. This is work that has not been pushed yet, not stale work. Keep it,
     however old it is.
   - **Active.** It tracks an existing remote branch. Keep it.
5. Classify each worktree by its branch. It is a candidate when its branch is Merged, when it is detached at a commit
   reachable from the default branch (a temporary verification worktree), or when git marks it prunable because its
   directory is gone. Any uncommitted or untracked change makes it Keep, whatever its branch: report the changes.
   A worktree with very recent activity may be in use by another agent: flag it. Leave unregistered directories under
   `.worktrees/` alone and report them.
6. Present the result as one table: the item, its category, the evidence, and the proposed action. Propose removal for
   Merged branches, their clean worktrees, and prunable worktrees. Propose nothing for Gone and Empty branches: show
   their commits and let the user choose. Wait for the user's approval.
7. Remove only what was approved. Record each branch's tip with `git rev-parse <branch>` first. Remove worktrees
   before their branches with `git worktree remove <path>`, then `git worktree prune`. Delete ancestor-merged branches
   with `git branch -d`. A squash-merged branch needs `git branch -D`; use it only for a branch proven merged in step 4
   or explicitly approved. When a command refuses, stop for that item and report why instead of forcing it.

## Done

The reply lists what was removed with each branch's last tip, so the user can restore one with
`git branch <name> <sha>`, what was kept and why, and anything that needs the user's decision, such as Gone branches
with unmerged commits, dirty worktrees, and unregistered directories. Nothing usually follows; a Gone branch the user
wants to keep may go on to Opening a PR (`opening-a-pr.md`).
