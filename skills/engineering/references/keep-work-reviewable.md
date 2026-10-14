# Keep work reviewable

Work nobody can review cannot be trusted or shipped. A reviewer can judge a
change that does one thing and fits in one sitting. A large diff that mixes
purposes gets skimmed or sent back. Splitting work is easy while it happens and
hard once it has piled up, so checkpoint it for review as you go.

- Start on a feature branch, or in a separate worktree, before the first
  change, never on the default branch. Creating the branch only when it is
  time to commit means the work so far happened where it did not belong.
- Make each commit one reviewable unit: one purpose, a message that says why,
  and a state that builds and passes the tests. A reviewer should be able to
  read the commits in order and understand each one without the later ones.
- Separate mechanical changes from behavior changes. A rename, move,
  formatting pass, or preparatory refactor gets its own commit before the
  change that needs it, so the reviewer can skim it and focus on the risk.
- Commit at every verified checkpoint, not at the end. When uncommitted work
  starts to serve more than one purpose, commit what is done before going on.
- When work has accumulated anyway, split it before asking for review. Stage by
  file or hunk into commits that each stand on their own, and verify each
  commit, not only the last. Never hand over one large commit because
  splitting is tedious.
- Verify a commit in a clean checkout of it, such as a temporary worktree
  (`git worktree add <dir> <sha>`), not in a working tree that still holds
  later uncommitted changes. Those changes make the check pass or fail for
  reasons the commit does not contain. Report which commit the check ran on.
- When the whole change is too large for one review, ship it as stacked PRs.
  Each PR holds one reviewable unit, targets the branch of the PR below it,
  and leaves the default branch working if merged on its own. Each description
  names the stack's order and the PR's place in it. Rebase and retarget the
  stack as lower PRs merge.
- For work that will span several reviews, plan the split before building:
  say which commits or PRs the work becomes, and in which order.
- A checkpoint is not permission to ship. Committing, pushing, and opening PRs
  still follow the user's instructions. Where they are not authorized, stop at
  a reviewable state, report it, and do not pile more work on top unasked.
