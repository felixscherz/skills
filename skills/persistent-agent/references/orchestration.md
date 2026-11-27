# Orchestrating work

A persistent coordinator is the user's point of contact,
not the default worker.
Discuss and shape work with the user,
keep track of decisions and progress,
and delegate substantive investigation, implementation, verification,
and review to task-scoped subagents.
This keeps the coordinator's context available for steering
and for the next conversation.
Brief reads to frame work or understand a report are fine;
do not turn them into a deep investigation
by the coordinator.

This is a way to carry out a coordinating role,
not a grant of authority or a requirement for every persistent agent.
The user's instructions, `ROLE.md`, project rules, and harness permissions
still govern delegation, scope, output budgets,
and approval gates.
A role that does not allow starting sessions
remains inbox-only;
follow its handoff rules instead.
If delegation is unavailable or capacity is full,
tell the user and queue or prioritize work
rather than silently taking it on yourself.
Do not start work just because a session was woken.

## Assign

- Split agreed work into bounded assignments
  with clear outcomes.
  Start a fresh task-scoped child per assignment;
  a closely related follow-up
  may continue the same child.
  Run independent assignments concurrently
  when supported and within the role's output budget.
  Use separate worktrees or explicit ownership
  when concurrent changes could conflict.
- Give each child a complete brief:
  desired outcome and acceptance criteria;
  scope, constraints, relevant decisions and paths;
  permitted actions and approval gates;
  when to stop and ask;
  the expected report;
  and an estimated token budget when useful.
  The brief does not authorize work
  beyond the user's agreed scope or applicable permissions.
- Let the child own execution
  and technical choices inside the brief.
  Do not micromanage or require routine progress reports.
  For an independent review,
  use a child that did not do the work being reviewed.

## Follow through

- Ask the child to return one consolidated report:
  outcome, changed paths or commits,
  verification, remaining risks, documentation updates, and follow-ups.
  For a genuine blocker,
  a decision outside its authority,
  or work likely to exceed the budget,
  it should stop the blocked work
  and return a partial report with options and a recommendation.
- Treat token budgets as estimates,
  not measured limits.
  Do not invent usage;
  if it is unavailable,
  use the estimate as an effort guide and escalate
  when the work appears larger than the brief.
- Check reports against the assignment,
  send incomplete work back when appropriate,
  synthesize the result,
  and bring decisions and permission requests to the user.
  The coordinator remains accountable for the outcome.
- Record active assignments,
  child session IDs
  when available, scope, budget, state, pending input,
  and next actions in `STATUS.md`, keeping it a concise snapshot.
  Reconcile outcomes and pending permissions at session boundaries
  before starting replacements.
  Do not interrupt active work or abandon pending user input
  to rotate sessions.

Task-scoped children are not persistent agents:
they follow their brief,
do not assume the coordinator's identity,
and do not maintain its state or inbox.
The coordinator absorbs their results
into its own state
and any authorized durable project documentation.
Handoffs to other persistent agents
still follow [inbox.md](inbox.md).
