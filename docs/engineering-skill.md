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

An agent that skips a step says which and why in its reply. An earlier version had the agent copy the steps into its
todo list; no session did, so the rule is gone.

## Routing

`SKILL.md` loads on its own for any non-trivial engineering work, so no one has to invoke it. It lists the playbooks
first, then how they hand over to each other and how to pick one when several seem to fit. Below them it keeps the
index of references, as a fallback for work no playbook covers.

Rules that apply to every task, such as restating the goal in the first message, live in `SKILL.md` under "Start of a
task" instead of being repeated as the first step of each playbook. The steps every code-changing playbook shares
(branch, test first, commit per step, update `CONTEXT.md`, open a PR) live there too, under "Changing code".

## Tenets

`SKILL.md` opens with "What I care about": about fifteen one-line tenets, each naming the reference that holds the
detail. They exist because agents read the playbook and stopped there. In the first week of playbooks, six sessions
opened a playbook and none opened a reference its steps named, so the principles never reached the work. The tenets
load with the skill and carry the principles into every session; the references stay as depth.

## Design stays with the user

I stay in the loop for design. An agent does not come up with a design and implement it without my agreement. There
are two ways the design reaches me:

- **In the conversation.** For a change whose design fits in a few lines, Build a feature proposes it, waits for my
  choice on each open decision, and builds it in the same session. No spec, no written plan.
- **As a spec.** For a larger design, Design with me ends, optionally, in a spec that records it; Build a feature
  starts from such a spec. The spec is the hand-off, and it is where I review.

A spec holds the background, the reasoning, the alternatives considered, and the design. Parts marked `NORMATIVE` must
be built exactly as written; the rest is guidance the implementer may adapt and must report. Its shape is defined in
`references/spec.md`, so the playbook that writes a spec and the one that reads it share one definition.

## Playbooks

The list of playbooks, with when each applies, is the index in `SKILL.md`. Two of them take a different posture from
the rest:

- **Investigate** is read-only and autonomous: the agent settles every fact itself and comes back with an answer,
  which may be "no".
- **Prototype** suspends the production rules and the design gate: the agent decides how to build and the user
  reacts to results.

**Orchestrate** replaces the `agent-software-factory` and `working-as-an-agent-team` skills. It is frozen until a real
session has used it.

## Moving workflows out of references

Workflow references become playbooks, so `references/` holds only principles and document shapes.

- `ship-changes/` became Opening a PR, with the description guidance and template kept as a reference.
- `find-the-root-cause.md` became the Find the cause playbook for investigations. The reference stays for its
  principles, fix a defect where the bad state is first created and eliminate competing causes one by one, which also
  apply when debugging inside other work.
- `code-review.md` became the Review code playbook. The reference keeps the principles: calibrating scrutiny, naming
  as a blocker, changed tests, weakened verification, and classifying findings. The output template moved to
  `review-output.md`, a document shape.
- `plan-from-a-spec.md` and `find-the-root-cause.md` are listed under principles in `SKILL.md`, and the "Workflows"
  group of references is gone. `test-driven-design.md` was merged into `test-behavior.md`.
