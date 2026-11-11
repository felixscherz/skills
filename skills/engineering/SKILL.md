---
name: engineering
description: Use for any non-trivial code change - features, bug fixes, refactors, writing or changing tests, designing types, modules, or APIs, designing a solution with the user before it is built ("let's design", "design this with me"), implementing a spec, answering a question about a system without changing it ("how does this work", "is this feasible", "analyze", a feasibility check), building a prototype or proof of concept ("prototype", "POC", "spike", "just try it"), investigating a bug or production error to find its root cause, shipping the change through a pull request, reviewing a pull request or code changes ("review this PR", "code review", "review my branch", a PR number or URL), and addressing review feedback on a change (PR comments, bot findings, a reviewer agent's output). Also when the user asks to follow my engineering principles.
---

# Engineering

## What I care about

These hold in every task, whichever playbook applies. Each is one line; the
reference behind it holds the detail. Read that reference when you are about
to act on the line and need more than the line says.

1. Think in the model before the code. Name everything in the domain's words, one name per concept (`references/domain-driven-design.md`).
2. A requirement that does not fit the model gets a model change, not a special case (`references/redesign-from-first-principles.md`).
3. Solve the immediate problem with the smallest coherent solution, and name the fuller design as a follow-up (`references/deliver-in-small-steps.md`).
4. Say how you will verify the work before you build it. Write the test first and see it fail for the intended reason (`references/test-behavior.md`).
5. Test behavior through the public API, with fakes at real boundaries instead of mocks and patches (`references/test-behavior.md`).
6. Keep a pure core with side effects at the edges and dependencies passed in. Code that is awkward to test is awkward to use (`references/program-design.md`).
7. Make modules deep: a simple interface that hides a lot, judged from the caller's side (`references/deep-modules.md`).
8. Let types carry meaning. Make illegal states unrepresentable, and never pass a bare primitive for a domain value (`references/type-system.md`).
9. Names matter enough to block a change. A reader should understand a name without opening the implementation (`references/code-review.md`).
10. Fix a defect where the bad state is created, not where it shows up, and do not fix what you have not reproduced (`references/find-the-root-cause.md`).
11. Every mistake found should make its whole class harder to repeat, with the lightest check that catches it (`references/never-make-the-same-mistake-twice.md`).
12. Code is judged by how it is used. Changing behavior someone relies on needs sign-off, proof nobody uses it, or the old behavior kept available (`references/dont-break-production.md`).
13. Keep work reviewable while it happens: a branch before the first change, one purpose per commit, a commit after every verified step (`references/keep-work-reviewable.md`).
14. A change is done when its checks pass and it sits in front of a reviewer who can see what it is for (`playbooks/opening-a-pr.md`).
15. Scale the rigor to blast radius and longevity. Core domain code gets all of the above; a prototype or one-off script gets almost none of it (`playbooks/prototype.md`).

## Know when rules do not apply

These rules are my personal defaults, not my team's. Where a codebase has
established conventions, the conventions win. Where it has none, the rules
apply in full.

- Follow the patterns the codebase already uses, even where a rule here says
  otherwise. Personal preference is not a reason to impose a pattern on others.
- Look at how neighboring code solves the same problem before choosing an
  approach.
- Never make broad changes unprompted. Swapping a framework, a sweeping
  refactor, or a new architectural pattern needs the user's go-ahead.
- Pushing the boundary is sometimes right. When a convention causes a real
  problem for the task, propose the change with the reason and let the user
  decide.

## Start of a task

A codebase is a representation of a model, an abstraction of the real world.
The model does not have to mirror reality, it has to serve the problem. Think
in terms of the model first, then the code. Starting deep in the code risks
missing a wrong model, or chasing a local optimization when a global one is
available.

- In your first message on a task, restate the user's goal and the problem
  behind it in your own words, and, when the task changes code, the smallest
  change you expect to meet it. Go on without waiting for confirmation unless
  the playbook says otherwise. When what you find rules out the change the
  user asked for, show the evidence and stop.
- Before changing code, understand the problem, the domain, and how the parts
  you are about to touch work together.
- While reading code, check whether it still supports the model or has drifted
  from it. Name any drift you find. When code and model disagree, decide which
  one is wrong before fixing either.
- Read the nearest `CONTEXT.md` before exploring the code, and follow the
  links it gives for the task. When there is none, explore the code as usual
  and do not mention it.
- Keep plans, investigation notes, and other files that are not product code
  out of the repository. Use the task folder you were given, if any. A spec
  is the exception: it is committed with the project (see
  `references/spec.md`).

## Changing code

The playbooks that change product code share these steps and do not repeat
them. They do not apply to Prototype.

- Start a branch or worktree before the first change
  (`references/keep-work-reviewable.md`).
- For each step of the work, write the test first and see it fail for the
  intended reason (`references/test-behavior.md`). Implement until it passes,
  run the project's checks, and commit before the next step.
- Read the language index for the language you write in, and
  `references/dont-break-production.md` when the change alters behavior
  someone can observe.
- When the repository has a `CONTEXT.md` and the change adds, moves, renames,
  or removes a feature, a term, or a module, update it in the same change
  (`references/context.md`).
- Finish with Opening a PR (`playbooks/opening-a-pr.md`). Without the user's
  go-ahead to push, stop at a reviewable branch and report it.

## Playbooks

A playbook is the workflow for one kind of task. It says who decides what,
the steps to take, and which references to read at each step. Match the task
to a playbook below before anything else, and read it in full. A reference
named in a step is part of that step: open it and read it in full when you
reach the step, before doing what the step says. When you skip a step, say
which and why in your reply.

- **Make a change** (`playbooks/make-a-change.md`). The user asks for new or
  changed behavior, such as a feature, an endpoint, a field, or a ticket with
  clear scope, and there is no spec. The design is agreed in the conversation
  and built in the same session.
- **Design with me** (`playbooks/design-with-me.md`). The user wants to work
  out how to build something before it is built: a feature, a change that
  does not fit the current model, where functionality lives, how components
  or services interact, or how something can be tested. Ends in an agreed
  design, kept as a spec when the user wants.
- **Investigate** (`playbooks/investigate.md`). The user asks how a service,
  codebase, or library works, whether something is feasible or worth doing,
  or which of several options fits, and nothing has failed. Read-only. Ends
  in an answer backed by evidence, which may be "no".
- **Prototype** (`playbooks/prototype.md`). The user wants a proof of
  concept, a spike, or a throwaway project built fast to learn something.
  Production concerns are out and the agent decides how to build it.
- **Implement a spec** (`playbooks/implement-a-spec.md`). The user points to
  a spec or a written design and asks to build it.
- **Find the cause** (`playbooks/find-the-cause.md`). The user brings
  information about a bug in production, an error in a system, or a
  regression, and asks what is wrong or why it happened. Ends in a diagnosis
  backed by a reproduction, not a fix.
- **Fix a bug** (`playbooks/fix-a-bug.md`). The cause of a bug is known, from
  a diagnosis or because the user says what is wrong, and it needs fixing.
  Strictly a fix: no new behavior, no cleanup on the side.
- **Refactor** (`playbooks/refactor.md`). The user asks to restructure code
  without changing what it does: rename, move, split, or merge modules,
  change an internal API, reshape code toward a better model, or give a
  module a simpler interface that hides more.
- **Opening a PR** (`playbooks/opening-a-pr.md`). A change is done and needs
  to be pushed and integrated through a pull request, or a PR description
  needs writing or updating.
- **Review code** (`playbooks/review-code.md`). The user asks to review a
  pull request, a branch, or a set of code changes, their own or someone
  else's.
- **Address feedback** (`playbooks/address-feedback.md`). A change has
  received feedback, such as PR comments, bot findings, or a reviewer agent's
  output, and the user asks to address it.
- **Orchestrate** (`playbooks/orchestrate.md`). The user asks to orchestrate
  a task, delegate it to subagents, or work on it as an orchestrator. Wraps
  the playbook the task matches and runs its steps through subagents in a
  worktree.

When more than one seems to fit, pick by what the user wants at the end.
A bug report whose cause is unknown starts at Find the cause, even when the
user asks for a fix; Fix a bug follows once the user accepts the diagnosis.
A question about something that works is Investigate; a question about
something that failed is Find the cause. A refactor that would change
behavior is Make a change or Fix a bug, not Refactor. A request that names a
spec is Implement a spec, even when the change is small. A request to try
something out quickly is Prototype, even when it looks like a feature.

When no playbook fits, use the references below directly.

## References

The references hold the details. Each covers one topic, and the index says
when it applies. A playbook names the references for each of its steps; the
index is for work no playbook covers. Read a reference when you reach the
step that names it or when its trigger fires, and read it in full before
applying it. Do not read references for steps you have not reached. Do not
list the references you applied in your reply unless the user asks.

### Context

Documentation that points an agent to the right code or document without
searching.

- **Context** (`references/context.md`). The user asks to write or change a
  `CONTEXT.md` or its docs, one points to the wrong place, or a task adds,
  moves, renames, or removes a feature, a domain term, or a linked document in
  a repository that has one.

### Documents

The shape of documents that hand work from one person or agent to the next.

- **Spec** (`references/spec.md`). Writing, reading, or changing a spec that
  records an agreed design.
- **Pull request description**
  (`references/pull-request-description/pull-request-description.md`).
  Writing or updating a PR description.
- **Review output** (`references/review-output.md`). Writing a code review,
  or reading one to act on it.

### Principles

Rules that shape design and engineering decisions in any language.

- **Domain-driven design** (`references/domain-driven-design.md`). Naming or
  modelling domain concepts, adding a process that spans several services, or
  domain logic scattered across layers.
- **Redesign from first principles** (`references/redesign-from-first-principles.md`).
  Requirements change or are added, a drift is found, or you are about to add
  a special case for an edge case.
- **Deliver in small steps** (`references/deliver-in-small-steps.md`). Deciding
  how much to build for a request, before proposing an architecture or
  design, when a fix suggests a larger redesign, or planning work that spans
  several changes.
- **Keep work reviewable** (`references/keep-work-reviewable.md`). Before the
  first change of any task that ends in a commit or a review, at every
  commit, when uncommitted work grows beyond one purpose, or when splitting a
  diff or handing work over for review.
- **Worktrees** (`references/worktrees.md`). Creating, using, or removing a
  git worktree, or working in a repository other agents may be working in
  at the same time.
- **Program design** (`references/program-design.md`). Designing a new module,
  API, or model, deciding where code lives, or code that is hard to test.
- **Deep modules** (`references/deep-modules.md`). Designing or changing a
  module's interface, deciding what a module hides, or callers that repeat
  work, decisions, or knowledge the module could own.
- **Type system** (`references/type-system.md`). Designing types, signatures, or
  data shapes, or reaching for a plain string, dict, or bool that carries
  meaning.
- **Lifecycle hygiene** (`references/lifecycle-hygiene.md`). Writing or
  changing a long-running service or worker: startup, shutdown, background
  tasks, consumers, readiness probes, or dependencies that can go away.
- **Test behavior** (`references/test-behavior.md`). Before implementing a
  feature or fixing a bug, when writing, changing, naming, or keeping a test,
  or about to reach for a mock or patch.
- **Plan from a spec** (`references/plan-from-a-spec.md`). Turning a spec,
  requirements, or a ticket into an implementation plan, or planning work
  that spans several steps or agents.
- **Find the root cause** (`references/find-the-root-cause.md`). When debugging
  a failure or investigating a bug, before choosing a fix, and when several
  causes could explain a failure.
- **Code review** (`references/code-review.md`). Judging a code change, your
  own or someone else's: how closely to look, what makes a blocker, and
  changes to names, tests, and verification.
- **Never make the same mistake twice** (`references/never-make-the-same-mistake-twice.md`).
  After finding a bug, misusing a third-party API, or discovering a wrong
  assumption about an external service or constraint.
- **Don't break production** (`references/dont-break-production.md`). A
  change alters behavior that callers, users, or other systems can observe,
  including invisible semantics like durability, retries, ordering, or
  error handling where the interface stays the same.

### Language-specific

Guidance that builds on the principles for one language or framework.

- **Python** (`references/python/INDEX.md`). Writing or changing Python code.
  The index lists the Python references and when each applies; read only the
  ones the task needs.

## Maintaining this skill

These rules are a living draft, not a finished standard. Be critical of them.
When one gets in the way, leads to a worse result, misses a situation, or
contradicts another rule or the codebase, say so at the end of your reply. The
user decides when the skill changes: never edit it unprompted. Changes go
through the `reflect-on-engineering` skill
(`../reflect-on-engineering/SKILL.md`), which also holds the conventions for
editing this skill.
