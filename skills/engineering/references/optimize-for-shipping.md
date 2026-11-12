# Optimize for shipping

The goal of a change is to ship it: merged, deployed, and in use. Until then it
delivers nothing and keeps costing: it drifts from the default branch, holds
decisions open, and grows harder to review. The longer a change takes and the
more code it adds at once, the less likely it is to ship soon. Ten incremental
changes ship faster and with less risk than one change ten times the size,
because each one can be reviewed in one sitting, verified on its own, and
rolled back alone. Small steps are the means, not the goal: shipping decides
the scope of a change and how it is made safe.

- Scope by what can ship. Solve the immediate problem with the smallest change
  that can ship on its own. Small means no responsibilities or guarantees the
  request does not need, not compressed code or shortcuts. When a fuller
  design would be better, name it as a follow-up instead of building it.
- Decide how the change ships safely before building it. Know its blast
  radius: who and what sees the difference, and what breaks if it is wrong.
  Shrink it when it is large: put unfinished or risky behavior behind a
  feature flag or config switch so the code can merge before the behavior is
  on (`dont-break-production.md`), and say how you will verify it once it is
  deployed, not only in tests.
- Judge an edge case by its likelihood, consequences, and relevance to actual
  use. A rare security or data-loss risk can still be essential. A speculative
  failure with limited consequences usually does not justify substantial
  infrastructure.
- When a concern needs a new subsystem or a growing chain of prerequisites,
  revisit the approach before the next repair. Prefer removing machinery over
  making it handle every conceivable failure.
- When the work turns out much larger than the request suggested, tell the
  user what you found, the smallest alternative that ships, and your
  recommendation.
- Split larger work into steps that could each ship: working, verified, and
  leaving the default branch working if merged on its own. Commit each step
  before starting the next, so any step is a safe place to stop. Prefer
  several PRs that each merge soon over one long-lived branch
  (`keep-work-reviewable.md`). Opening a PR is a step toward shipping, not
  the end of it.
- Slice steps vertically. Each step delivers behavior a user or caller can
  observe, through every layer it needs. "Add the model", "add the
  repository", "add the endpoint" are commits inside a step, not steps.
