# Orchestrate

Run one task through subagents while the orchestrator keeps the scope, the decisions, and the conversation with the
user. The work itself, such as finding a cause, designing, implementing, and reviewing, happens in subagents, so the
orchestrator's context stays free for steering. The task runs in its own worktree, so other orchestrators can work on
other tasks in the same repository at the same time.

The orchestrator wraps another playbook; it does not replace it. The playbook that fits the task still decides the
steps and what waits for the user. The orchestrator splits those steps into phases, hands each phase to a subagent, and
checks what comes back against the agreed scope.

## Applies when

The user asks to orchestrate a task, to delegate it to subagents, or to work on it as an orchestrator. The task ends in
one branch or one PR. When it would take several PRs, propose the split and orchestrate each part as its own task.

## Who decides

- The user decides the scope at the start: what done means and what is out. Nothing is built before they agree.
- The user decides everything the wrapped playbook gives to the user, such as the design, accepting a diagnosis, or a
  larger fix. Subagents never decide these; they stop and return options with a recommendation, and the orchestrator
  brings them to the user.
- The user decides any growth of the scope, and whether to push, open a PR, and merge.
- The orchestrator decides the phases, what each subagent is told, whether a result meets the scope, and when to send
  work back.
- Subagents decide what the wrapped playbook leaves to the agent, within the scope they were given.

## Steps

1. Restate the task, pick the playbook that fits it from the index in `../SKILL.md`, and read that playbook. Write the
   scope in a few lines: the goal, done when, and out of scope. Wait for the user to agree.
2. Create the worktree and its branch (`../references/worktrees.md`).
3. Add a section for the task to `.worktrees/STATUS.md` in the primary checkout, creating the file when missing. The
   section is headed by the branch and holds the scope from step 1, the worktree path, the current phase, what the task
   waits on, the PR once there is one, and the follow-ups. Edit only your own section, since other orchestrators share
   the file. Keep it to the current state; it is not a log.
4. Split the playbook into phases. A phase ends where the playbook waits for the user or where a reviewable checkpoint
   exists, such as commits. Usually:
   - Make a change: design (its steps 1 to 4), build (5 to 8), review.
   - Find the cause, then Fix a bug: diagnose, fix, review.
   - Refactor, Refactor a module, Implement a spec: plan, build, review.

   Tell the user the phases in one line.
5. Run each phase as one subagent, one phase at a time. Give the subagent everything in its prompt, not in files:
   - that it works for an orchestrator, and which playbook file and steps it carries out;
   - the worktree's absolute path and branch, and that all work and commits happen there;
   - the agreed scope and every decision the user made so far, word for word;
   - that work outside the scope is reported as a follow-up, not done, and a decision the playbook gives to the user
     is returned as options with a recommendation, not made;
   - what to return, in a short reply: the outcome, the commits, how it was verified, the decisions needed, and the
     follow-ups.
6. Do not do phase work yourself. Do not read source code, diffs, logs, or test output; when you need to know something
   about the code, ask a subagent. Short orientation commands in the worktree, such as `git log --oneline` or `git
   status`, are fine.
7. After each phase, check the reply against the scope: does it meet the phase's part of done, does it name its commits
   and evidence, and did it stay inside the scope? Send work back when it does not. Bring each decision to the user
   with your recommendation and wait. Update the task's section in `STATUS.md`. Report to the user in a few lines: what
   finished, what is next, and what you need from them.
8. Review with a fresh subagent that took no part in the work, running Review code (`review-code.md`) on the branch
   against the agreed scope, and flagging any change outside it. Hand findings to a subagent running Address feedback
   (`address-feedback.md`). Review again with another fresh subagent when the changes go beyond the trivial.
9. Stop and ask the user before going on when the work grows: a prerequisite that was not in the scope, a second repair
   round on the same problem, a diff that outgrows the agreed design, or a subagent proposing extra work. Bring the
   evidence, the smallest way to stay in scope, and your recommendation (`../references/deliver-in-small-steps.md`).
10. When the user authorizes it, have a subagent run Opening a PR (`opening-a-pr.md`). Otherwise stop at the reviewed
    branch.
11. Mark the task done in `STATUS.md`. Leave the worktree in place (`../references/worktrees.md`).

## Done

A reviewed branch, or a PR when opening one is authorized, that meets the agreed scope. The reply states the outcome
against done when, the commits or the PR link, the decisions the user made along the way, how the work was verified
and reviewed, and the follow-ups. When the PR gets feedback, the next playbook is Address feedback, run the same way.
