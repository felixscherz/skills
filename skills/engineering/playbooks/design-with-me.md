# Design with me

Design is done together with the user, never hands-off. The agent explores the code, lays out options, and
recommends; the user makes every design decision. The result is a design both sides agree is valid, and optionally a
spec that keeps it.

## Applies when

The user wants to work out how to build something before it is built: a new feature, a change that does not fit the
current model, or a question about where functionality lives, how components interact, or how something can be
tested. This covers both levels: inside one codebase (modules, types, dependency direction) and across components or
services (interactions, contracts, infrastructure).

## Who decides

- The user decides every design choice, including what is in scope.
- The agent settles facts on its own: what the code does today, whether an option works, what a library supports.
  When a decision hinges on a fact it can observe by reading code or running a throwaway experiment outside the
  repository, it checks before asking.
- No product code is written during this playbook. The only file it produces is the spec, in its last step.

## Steps

1. Restate the user's goal and the problem behind it in your own words, and let them correct it before going on.
2. Read the nearest `CONTEXT.md` and the code it points to for this area. Describe the current model in the domain's
   words, and name any drift between model and code (`../references/domain-driven-design.md`).
3. Separate requirements from suggestions and constraints, and write down what is unclear. Decide with the user how
   much to build now and what becomes a follow-up (`../references/deliver-in-small-steps.md`).
4. Decide the level, and read the references it calls for. In a codebase: `../references/program-design.md`,
   `../references/type-system.md`. Across components or services: bounded contexts in
   `../references/domain-driven-design.md`, `../references/dont-break-production.md`, and
   `../references/lifecycle-hygiene.md` for long-running services. A design that spans both takes both.
5. When the requirement does not fit the current model, design the model change first rather than a special case
   (`../references/redesign-from-first-principles.md`).
6. Work through the open decisions one at a time, the ones others depend on first, usually the domain model. For
   each, give two or three options with their tradeoffs and your recommendation, and wait for the user's choice.
7. Agree how the design will be verified: which behavior is tested, and through which API
   (`../references/test-driven-design.md`, `../references/test-behavior.md`).
8. Summarize the whole design in a few lines with each decision and its reason, and ask whether it is valid. When the
   user changes something, go back to the affected step.
9. Ask whether to keep the design. If yes, write it as a spec (`../references/spec.md`) with status `Draft`, ask the
   user which parts are `NORMATIVE` when that is not clear from the conversation, and set it to `Accepted` once they
   approve it.

## Done

The user confirmed the design. When they chose to keep it, an accepted spec exists and its path is in the reply. The
next playbook is usually Implement a spec, in this session or another.
