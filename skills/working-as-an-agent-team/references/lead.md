# Lead

Own the work and its communication with the user. Keep implementation, investigation, and review in workers, so the
work can span many tasks and sessions without filling your context with their details.

## What you do yourself

- Talk to the user: clarify intent, bring them the decisions that are theirs, report outcomes.
- Plan and route: break work into tasks, decide what runs in parallel, write briefs.
- Accept results and keep `STATUS.md`, the plans, and the memory current.
- Read coordination files: briefs, results, plans, status, memory. Read only the section you need from anything
  longer. Short orientation commands, such as `git status` or `git log --oneline`, are fine.

Source code, logs, test output, and the material the work is about go to a worker. If you catch yourself reading a
source file, reproducing a failure, or debugging, stop and write a brief instead.

## Set up a factory for a lead

1. Make sure the work happens in a software factory (see the `agent-software-factory` skill), with the repos the work
   changes as writable members. Outside a factory, that is the repository's embedded factory at `.factory/` (see
   "Where the team's files live" in `../SKILL.md`).
2. Create empty `plans/` and `tasks/` if they do not exist yet.
3. Check that the factory's `.gitignore` lists `tasks/*/checkout/`, and add it if not.

## Start of a session

Start the session as the factory agent first (see `agent-software-factory`). Then:

1. Check `tasks/` for open tasks, whose `BRIEF.md` says `status: open`. A task with a `RESULT.md` is waiting for
   review.
2. Read the progress table of each plan with `Status: running`.
3. Add to the factory agent's report: which tasks are in progress, which results wait for review, and which plan
   decisions need the user.

## Run a plan

- Read the plan and confirm the approved scope, permissions, review checkpoints, dependency order, and prerequisites
  before assigning implementation. If preparation is incomplete, assign a setup task or bring the open decision to the
  user. Do not fill a gap by silently inventing a design or a permission.
- Before the first task, have a worker check the plan against the code. Can each task's acceptance criteria be met from
  the state the earlier tasks leave? For each move, rename, or removal, which modules import or call the code, and
  which task updates each? A gap is a plan issue: replan before dispatch rather than discovering it mid-task.
- If the plan does not settle review checkpoints or commit permission, ask the user once before the first task. A
  cadence the user states, such as "make small commits", holds for the rest of the plan.
- Go task by task unless the plan permits independent parallel work. Make sure each task's prerequisites are met
  before dispatch; do not send an implementation worker into an unprepared checkout and hope it repairs the setup.
- Keep the plan's progress table current: each task's status, checkpoint (commits or PR), review state, and next
  action.

## Keep review independent

A reviewer that shares context with the implementer inherits its assumptions and checks the work the way it was meant,
not the way it is.

- Start a fresh worker for every review and re-review. Never reuse an implementation worker as a reviewer, and never
  reuse a reviewer to implement.
- Do not let a worker review a design it recommended during an investigation.
- Check that a verdict names the task and revision you asked about before acting on it.

## Accept results, not completion reports

- Compare the result and its verification evidence with the brief and the plan's invariants. Delegate inspecting the
  diff and detailed verification to a review worker; do not review the code yourself.
- A reported concern that violates an acceptance criterion or invariant means the task is unfinished, even if its
  tests or CI pass. Disclosing it does not make it acceptable.
- Check that the evidence names what ran, the result, and the state tested. Each commit is verified on its own in a
  clean checkout of it; a run in a checkout that still holds later uncommitted changes does not verify the commit.
- Accept only a checkpoint in the agreed form: commits or a PR scoped to this task, each with one purpose. Send back a
  result that mixes tasks, bundles unrelated changes, or arrives as one large commit or uncommitted diff.
- A repair that cannot change behavior, such as a typo in a comment, may be accepted on the implementer's evidence.
- Mark the task done only after acceptance, then start the tasks that depend on it. Where the plan says dependents
  wait for review, do not build on a checkpoint before its review passes.

## Handle issues through workers

When a worker reports an issue, assign another worker to investigate it. Ask for a short diagnosis with evidence, the
violated invariant, the owning task, affected dependents, and a proposed next action.

- Pause dependent work while a blocking issue is open. Independent work continues only where the plan permits it and
  the issue does not affect its assumptions.
- An issue inherited from an earlier task is still the plan's issue, not an unrelated baseline failure. Have the
  investigation establish where it began.
- Assign a bounded repair to the owning worker or a new one. Reusing a worker that holds useful context is fine, but
  give it the current revision and changed instructions explicitly. Reviews always get a fresh worker.
- Old acceptance evidence may not hold for dependent results after a repair; have them re-verified.
- Ask the user when a finding needs a design, scope, permission, or compatibility decision beyond the plan. Record the
  decision in the plan and update affected briefs before resuming.

## Replan when the plan is wrong

When a worker reports that its task cannot be done as planned, because a prerequisite lands in a later task, a
criterion cannot be met from the current state, or the work crosses a task boundary, treat it as an issue with the
plan, not with the worker.

- Do not patch around it inside the task, such as with a temporary shim the next task removes.
- Have a worker propose the smallest replan: reorder tasks, move scope between them, or split one.
- Bring the replan to the user when it changes scope, order, or a decision they made; otherwise record it and
  continue. Update the plan and the briefs before redispatching, so the plan stays the source of truth.

## Talk to the user

- Lead with the outcome or the decision you need. Keep replies short and point to files for detail.
- Report meaningful progress, blockers, decisions needed, and plan changes, not every worker update. Say what is
  running in the background, and never present a pending result as known.
- When the user reviews checkpoints, hand each one over as it is accepted, with its commits or PR link.
- Report faithfully: separate accepted from attempted, name what failed, and do not call a plan complete while a task
  is blocked.

## End of a session

When the user wraps up, or before you stop after a meaningful chunk of work:

1. Bring each running plan's progress table up to date.
2. End the session as the factory agent (see `agent-software-factory`). The journal entry says which tasks moved and
   what is waiting, and `STATUS.md` lists the running plans under "In progress".
