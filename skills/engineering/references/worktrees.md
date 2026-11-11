# Worktrees

A worktree is a second checkout of the same repository on its own branch. It lets a task run in isolation from the
user's checkout and from other agents working in the same repository at the same time. Isolation only holds while every
agent stays in its own worktree and leaves the shared checkout alone.

- Put worktrees at `.worktrees/<dir>` in the primary checkout, where `<dir>` is the branch name with `/` replaced by
  `-`, unless the repository has a convention of its own. Find the primary checkout from anywhere with
  `dirname "$(git rev-parse --path-format=absolute --git-common-dir)"`. `.worktrees/` is globally git-ignored; check
  with `git check-ignore -q .worktrees/`, and when it is not, add it to `.git/info/exclude`, never to a committed
  `.gitignore`.
- One task, one branch, one worktree. Start it from the current default branch of the remote, not from whatever the
  primary checkout has checked out:

  ```sh
  git fetch origin
  git worktree add -b <branch> .worktrees/<dir> origin/<default branch>
  ```

  Run `git worktree list` first. A branch or directory that already exists belongs to someone else's task: pick
  another name rather than reuse it.
- Work only inside your own worktree. Never switch branches, stash, reset, or commit in the primary checkout or in a
  worktree you did not create: the user or another agent may be using it. Use the worktree's absolute path for every
  command (`git -C <path>`, or `cd <path>` in the same command), and give that path to every subagent.
- A new worktree holds only tracked files. Install dependencies and build inside it with the project's own setup
  (`uv sync`, `npm ci`, ...). When it needs untracked local files such as `.env`, copy them from the primary checkout
  and say which ones you copied.
- Parallel worktrees share the machine. When a task runs services, containers, or a local database, pick ports and
  names that do not collide with other tasks, or say that the task cannot run alongside them.
- Use plain `git worktree` commands rather than a harness's own worktree feature, so the layout is the same in every
  harness and visible to every agent.
- Leave a task's worktree in place until the user asks to remove it. Then run `git worktree remove <path>`. It refuses
  when the worktree has uncommitted changes; report them instead of forcing. Delete the branch only when it is merged. To
  clean up the worktrees and branches that past tasks left behind, follow `../playbooks/repository-cleanup.md`.
- A temporary worktree you create for one check, such as verifying a commit (`git worktree add --detach
  .worktrees/verify-<sha> <sha>`), is yours to remove as soon as the check is done.
