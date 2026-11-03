# The engineering skill

The `engineering` skill holds my philosophy for software engineering and the practices that follow from it. It is
large, and most of it is irrelevant to any single task. Its structure exists so that an agent reads the few parts that
apply and skips the rest.

## References and playbooks

The skill has two kinds of content.

- **References** (`references/`) say what good looks like: a principle or best practice on one topic, such as type
  design, testing behavior, or not breaking production. References also define the shape of the documents that hand
  work over, such as a spec or a PR description, so that several playbooks can share one definition.
- **Playbooks** (`playbooks/`) say what to do: a workflow or a responsibility, such as designing a feature,
  implementing a spec, or opening a PR. A playbook names the situation it applies in, who decides what, the steps to
  take, and the references to read at each step.

An agent routes to a playbook first, and the playbook routes to references. The playbook knows the context, so it can
pull in the right principles at the right step, which an index of principles alone cannot. Before playbooks existed,
`SKILL.md` indexed references directly, and each reference had to describe its own trigger well enough for the agent
to find it.

The idea is borrowed from Lauren Tan's [pstack](https://github.com/cursor/plugins/tree/main/pstack), whose
`poteto-mode` skill routes a task to one of its playbooks. The playbooks here differ in posture: pstack aims for full
autonomy, while these keep the user in the loop for design decisions and keep the agent inside the assigned scope.

## Anatomy of a playbook

Each playbook is one file in `playbooks/` with:

- **Applies when.** The situation, stated as what the user asks for or what the agent finds. This is what the index in
  `SKILL.md` repeats.
- **Who decides.** Where the user is in the loop: which decisions wait for them, and what the agent settles alone.
- **Steps.** Ordered, each with the references it pulls in. A step names its reference at the point it applies, not
  in a list at the top.
- **Done.** What the playbook hands back, what the final reply holds, and which playbook usually comes next. The reply
  is where I review the work, so each playbook says what it contains rather than leaving it to the agent.

When a playbook applies, the agent copies its steps word for word into its todo list before any task-specific items.
A step it skips stays in the list with a one-line reason, so a skipped step is a visible decision rather than a
forgotten one.

## Routing

`SKILL.md` loads on its own for any non-trivial engineering work, so no one has to invoke it. It lists the playbooks
first, then how they hand over to each other and how to pick one when several seem to fit. Below them it keeps the
index of references, as a fallback for work no playbook covers.

Rules that apply to every task, such as restating the goal in the first message, live in `SKILL.md` under "Start of a
task" instead of being repeated as the first step of each playbook.

## Design stays with the user

I stay in the loop for design. An agent does not come up with a design and implement it without my agreement. There
are two ways the design reaches me:

- **In the conversation.** For a change whose design fits in a few lines, Make a change proposes it, waits for my
  choice on each open decision, and builds it in the same session. No spec, no written plan.
- **As a spec.** For a larger design, Design with me ends, optionally, in a spec that records it; Implement a spec
  starts from such a spec. The spec is the hand-off, and it is where I review.

A spec holds the background, the reasoning, the alternatives considered, and the design. Parts marked `NORMATIVE` must
be built exactly as written; the rest is guidance the implementer may adapt and must report. Its shape is defined in
`references/spec.md`, so the playbook that writes a spec and the one that reads it share one definition.

## Playbooks

Written:

- **Make a change** (`make-a-change.md`). New or changed behavior without a spec: the design is agreed in the
  conversation and built in the same session. Moves to Design with me when the design outgrows the conversation.
- **Design with me** (`design-with-me.md`). Working out a solution together with the user, at the level of one
  codebase or across components and services. Ends in an agreed design, kept as a spec when the user wants.
- **Implement a spec** (`implement-a-spec.md`). Building from an accepted spec, inside its scope. Ends in Opening a PR.
- **Find the cause** (`find-the-cause.md`). The user has information about a bug, production error, or regression and
  wants it investigated. Reproducing it and explaining what caused it come first; fixing it is not the goal. Ends in a
  diagnosis.
- **Fix a bug** (`fix-a-bug.md`). The cause is known, from Find the cause or from the user. Strictly a fix: anything
  the fix does not need, such as new behavior, cleanup, or adjacent bugs, becomes a follow-up.
- **Refactor** (`refactor.md`). The structure changes and the behavior does not. Starts by agreeing with the user
  which behavior is preserved and pinning it with tests; bugs and missing features found on the way become follow-ups.
- **Opening a PR** (`opening-a-pr.md`). Getting a finished change past the checks and in front of a reviewer. The
  description's shape lives in `references/pull-request-description/`.
- **Review code** (`review-code.md`). Reviewing a PR or a set of changes, my own or someone else's. The principles
  live in `references/code-review.md` and the output shape in `references/review-output.md`, which Address feedback
  also reads.
- **Address feedback** (`address-feedback.md`). Working through review feedback, from PR comments, bots, or a reviewer
  agent. Each item is a claim checked against the code before anything changes.

Planned:

- **Orchestrate.** The agent acts as an orchestrator: it delegates work to subagents within one session and checks
  what they hand back. Work that has to outlive the session moves to the `working-as-an-agent-team` skill.

## Moving workflows out of references

Workflow references become playbooks, so `references/` holds only principles and document shapes.

- `ship-changes/` became Opening a PR, with the description guidance and template kept as a reference.
- `find-the-root-cause.md` became the Find the cause playbook for investigations. The reference stays for its
  principles, fix a defect where the bad state is first created and eliminate competing causes one by one, which also
  apply when debugging inside other work.
- `code-review.md` became the Review code playbook. The reference keeps the principles: calibrating scrutiny, naming
  as a blocker, changed tests, weakened verification, and classifying findings. The output template moved to
  `review-output.md`, a document shape.
- `plan-from-a-spec.md`, `test-driven-design.md`, and `find-the-root-cause.md` are listed under principles in
  `SKILL.md`, and the "Workflows" group of references is gone.
