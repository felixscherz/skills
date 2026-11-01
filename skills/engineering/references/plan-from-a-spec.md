# Plan from a spec

A spec says what the result must do. A plan says how the work gets there, in steps that each end in a working state.
A plan written straight from a spec tends to copy its structure and to split work by layer or by file. Steps like
that cannot be verified on their own and multiply handoffs. Derive the steps from the behavior instead, and keep
them as large as one agent can carry.

- Before planning, separate the spec's requirements from its suggestions. Requirements are observable behavior and
  hard constraints. Suggested designs, data shapes, and task lists are input to weigh, not decisions already made.
- Write down every ambiguity, gap, and contradiction you find, and settle them with the user before you plan the
  steps that depend on them. Record assumptions you make as assumptions, never as requirements. When the requirements
  only exist in conversation, write them down as the plan's first section and confirm them.
- Map the spec onto the model before onto the code (see `domain-driven-design.md`). Name the concepts it adds or
  changes. When a requirement does not fit the current model, plan the model change first (see
  `redesign-from-first-principles.md`).
- Give every requirement a step that delivers it and a check that proves it, preferably a test written first (see
  `test-driven-design.md`). A requirement with no check is not planned yet. A step that serves no requirement is
  scope the spec did not ask for: drop it or name it as a follow-up.
- Slice steps vertically. Each step delivers behavior a user or caller can observe, through every layer it needs,
  and ends in a verified state. Plan the earliest end-to-end behavior as the first step where dependencies allow.
  "Add the model", "add the repository", "add the endpoint" are commits inside a step, not steps.
- Size a step by what one agent can finish and verify in one session, not by what one review can hold. Every step
  boundary costs a handoff, rebuilt context, and a review, and is a seam where details get lost. A step larger than
  one review hands over several commits or stacked PRs (see `keep-work-reviewable.md`) instead of becoming several
  steps.
- Split a step only for a reason: a review or decision must land before the next part can start, the parts can run
  independently in parallel, a part is different work such as an investigation or a migration with its own risk, or
  the step would exceed what one agent can hold. When none applies, keep it whole.
- For each step, state its outcome, the requirements it covers, its acceptance checks, what it depends on, and what
  must stay intact. Order the steps against the code, so each one can meet its checks from the state the earlier ones
  leave.
- End the plan with what remains open: unresolved questions, accepted limitations, and conditions that send the work
  back to the user. Keep the plan out of the repository unless the user asks for it there.
