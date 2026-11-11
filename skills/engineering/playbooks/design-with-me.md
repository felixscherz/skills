# Design with me

The agent designs on its own. It clears up the requirements at the start when they are unclear, then investigates the
code and works out a design without checking in on each decision. Each choice follows the tenets in `../SKILL.md` and
the patterns the codebase already uses. The user reviews the finished design, and the result is a design both sides
agree is valid, and optionally a spec that keeps it.

## Applies when

The user wants to work out how to build something before it is built: a new feature, a change that does not fit the
current model, or a question about where functionality lives, how components interact, or how something can be
tested. This covers both levels: inside one codebase (modules, types, dependency direction) and across components or
services (interactions, contracts, infrastructure).

## Who decides

- The user decides the requirements and the scope. The agent asks about them once, at the start, and only when the
  request leaves them open in a way the code cannot settle.
- The agent makes the design decisions: the model, where code lives, interfaces, types, and how the design is
  verified. It settles facts on its own by reading code or running a throwaway experiment outside the repository, and
  does not ask the user what it can observe.
- The user accepts or rejects the finished design. A design that needs a broad change, such as a new framework, a new
  architectural pattern, or a change to behavior others rely on, names that choice for the user to approve instead of
  assuming it.
- No product code is written during this playbook. The only file it produces is the spec, in its last step.

## Steps

1. Separate requirements from suggestions and constraints. When a requirement is unclear or two readings would lead
   to different designs, and reading the code cannot settle it, ask all such questions in one message and wait for the
   answers. Otherwise go on without waiting.
2. Read the nearest `CONTEXT.md` and the code it points to for this area. Describe the current model in the domain's
   words, and name any drift between model and code (`../references/domain-driven-design.md`).
3. Find how neighboring code solves similar problems: its structure, naming, error handling, and tests. Where the
   codebase has a convention, the design follows it, even where a tenet says otherwise.
4. Decide how much to build now and what becomes a follow-up (`../references/deliver-in-small-steps.md`).
5. Decide the level, and read the references it calls for. In a codebase: `../references/program-design.md`,
   `../references/deep-modules.md`, `../references/type-system.md`. Across components or services: bounded contexts in
   `../references/domain-driven-design.md`, `../references/dont-break-production.md`, and
   `../references/lifecycle-hygiene.md` for long-running services. A design that spans both takes both.
6. When the requirement does not fit the current model, design the model change first rather than a special case
   (`../references/redesign-from-first-principles.md`).
7. Work through the open decisions, the ones others depend on first, usually the domain model. For each, weigh the
   realistic options against the tenets and the codebase's patterns, and pick one. When reading cannot settle whether
   an option works, run the smallest experiment that can, outside the repository.
8. Decide how the design will be verified: which behavior is tested, and through which API
   (`../references/test-behavior.md`).
9. Present the design: the model, then each decision with its reason and the main alternative it beat. Name any choice
   that needs the user's approval, and ask whether the design is valid. When the user changes something, go back to
   the affected step and rework what depends on it.
10. Ask whether to keep the design. If yes, write it as a spec (`../references/spec.md`) with status `Draft`, ask the
    user which parts are `NORMATIVE` when that is not clear from the conversation, and set it to `Accepted` once they
    approve it.

## Done

The user confirmed the design. The reply summarizes it in a few lines with each decision and its reason, and lists
what became a follow-up. When the user chose to keep it, an accepted spec exists and its path is in the reply. The next
playbook is usually Build a feature, in this session or another.
