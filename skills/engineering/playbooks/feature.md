# Build a feature

Build new or changed behavior from an agreed design. The design belongs to the user and reaches the agent one of two
ways: as a spec (see `../references/spec.md`), or in the conversation, where the agent proposes it in a few lines and
the user agrees or corrects it. Either way, this playbook turns the design into tested, reviewable commits and brings
back to the user whatever the design did not settle.

## Applies when

The user asks for new or changed behavior, such as a feature, an endpoint, a field, an option, or a ticket with clear
scope, or points to a spec or written design and asks to build it. Without a spec, the design must fit in one
conversation. When it spans several services, has many open decisions that depend on each other, or the user wants it
kept, it belongs in Design with me first.

## Who decides

- With a spec, the spec decides what is built. Parts marked `NORMATIVE` are built exactly as written. Unmarked parts
  are guidance the agent may adapt to what it finds in the code, and it records every adaptation and its reason.
- Without a spec, the user decides every design choice: the data shape, where the code lives, how it surfaces to
  callers, and what is in scope. The agent recommends. When the request leaves no design decision open, because the
  change follows a pattern the codebase already uses, the agent states its approach in one or two lines and goes on
  without waiting.
- The user decides anything the design does not settle: an ambiguity, a contradiction with the code, a part that
  cannot be built as agreed, or work beyond the agreed scope. The agent pauses the affected work and brings each one to
  the user with its recommendation.
- The agent settles facts on its own, such as what the code does today or whether a library supports something, and
  decides everything below the agreed design: names of internals, commit order, test structure.

## Steps

1. With a spec, read it in full. If its status is not `Accepted`, ask the user before building from it.
2. Read the code the change touches, and look at how neighboring code solves the same problem.
3. Settle the design before building:
   - With a spec, list the normative requirements, and every ambiguity, gap, or contradiction between the spec and the
     code. Bring the list to the user and settle it before planning the parts that depend on it.
   - Without a spec, check whether the request fits the current model. When it does not, the model change is part of
     the design, not a special case (`../references/redesign-from-first-principles.md`,
     `../references/domain-driven-design.md`). Decide how much to build now and what becomes a follow-up
     (`../references/deliver-in-small-steps.md`). Then propose the design in a few lines: the data shape and its
     types, where the code lives, how callers see the change, and how it will be verified
     (`../references/program-design.md`, `../references/type-system.md`, `../references/test-behavior.md`). For each
     open decision, give the options and your recommendation, and wait for the user's choice unless no decision is
     open. When the proposal grows past a few decisions or reaches across services, stop and suggest Design with me
     (`design-with-me.md`).
4. When the work spans several steps, plan them (`../references/plan-from-a-spec.md`) and share the plan with the
   user. With a spec, every normative requirement has a step that delivers it and a check that proves it. Continue
   unless step 3 left something open.
5. Build each step, following Changing code in `../SKILL.md`. Read `../references/type-system.md` and
   `../references/program-design.md` for new types and modules.
6. When the code shows the design does not work, or raises something the design did not settle, pause the affected
   step and bring it to the user with a recommendation. If a spec changes, update it first (`../references/spec.md`).
7. Check the result against the design: with a spec, every normative requirement against its passing check and every
   adaptation against the spec's intent; without one, the change against the agreed proposal.
8. When the change completes a spec, set its status to `Implemented` in the same change.

## Done

A branch, or a PR when opening one is authorized, that implements the agreed design. The reply states the design as
built in a few lines and says how it was verified. With a spec, it maps each normative requirement to the check that
proves it and lists each adaptation of unmarked guidance with its reason. Without one, it names any point where the
build departed from the proposal and why. It lists what remains open or became a follow-up. The next playbook is
usually Opening a PR (`opening-a-pr.md`).
