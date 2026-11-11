# Make a change

Design and build a change in one session, without a spec or a written plan. The design still belongs to the user: the
agent proposes it in a few lines in the conversation, the user agrees or corrects it, and then the agent builds it. This
is the playbook for most feature work whose design fits in one conversation.

## Applies when

The user asks for new or changed behavior, such as a feature, an endpoint, a field, an option, or a ticket with clear
scope, and there is no spec for it. When the change spans several services, has many open decisions that depend on each
other, or the user wants the design kept, it belongs in Design with me first.

## Who decides

- The user decides every design choice: the data shape, where the code lives, how it surfaces to callers, and what is
  in scope. The agent recommends.
- When the request leaves no design decision open, because the change follows a pattern the codebase already uses, the
  agent states its approach in one or two lines and goes on without waiting.
- The agent settles facts on its own, such as what the code does today or whether a library supports something, and
  decides everything below the agreed design: names of internals, commit order, test structure.

## Steps

1. Read the code the change touches, and look at how neighboring code solves the same problem.
2. Check whether the request fits the current model. When it does not, the model change is part of the design, not a
   special case (`../references/redesign-from-first-principles.md`, `../references/domain-driven-design.md`).
3. Decide how much to build now and what becomes a follow-up (`../references/deliver-in-small-steps.md`).
4. Propose the design in a few lines: the data shape and its types, where the code lives, how callers see the change,
   and how it will be verified (`../references/program-design.md`, `../references/type-system.md`,
   `../references/test-behavior.md`). For each open decision, give the options and your recommendation. Wait for the
   user's choice unless no decision is open. When the proposal grows past a few decisions or reaches across services,
   stop and suggest Design with me (`design-with-me.md`).
5. Build it, following Changing code in `../SKILL.md`. When the code shows the design does not work, pause and bring it
   to the user with a recommendation.

## Done

A branch, or a PR when opening one is authorized, that implements the agreed design. The reply states the design as
built in a few lines, names any point where the build departed from the proposal and why, says how the change was
verified, and lists the follow-ups.
