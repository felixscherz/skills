# Implement a spec

Build what an accepted spec describes, and nothing else. The design decisions were made when the spec was written; this
playbook turns them into tested, reviewable commits and brings back to the user whatever the spec did not settle.

## Applies when

The user points to a spec (see `../references/spec.md`) or asks to implement a design that was written down. Without a
written design, the work is either small enough to need no playbook or belongs in Design with me first.

## Who decides

- The spec decides what is built. Parts marked `NORMATIVE` are built exactly as written. Unmarked parts are guidance
  the agent may adapt to what it finds in the code, and it records every adaptation and its reason.
- The user decides anything the spec does not: an ambiguity, a contradiction with the code, a normative part that
  cannot be built as written, or work beyond the spec's scope. The agent stops the affected work and brings each one
  to the user with its recommendation.
- The agent decides everything inside the spec's scope that the spec leaves open, such as names of internals, commit
  order, and test structure.

## Steps

1. Read the spec in full. If its status is not `Accepted`, ask the user before building from it.
2. Read the code the spec touches.
3. List the normative requirements, and every ambiguity, gap, or contradiction between the spec and the code. Bring
   the list to the user and settle it before planning the parts that depend on it.
4. Plan the steps from the spec (`../references/plan-from-a-spec.md`) and share the plan with the user. Every
   normative requirement has a step that delivers it and a check that proves it. Continue unless step 3 left
   something open.
5. Build each step of the plan, following Changing code in `../SKILL.md`. Read `../references/type-system.md` and
   `../references/program-design.md` for new types and modules.
6. When a normative part turns out wrong, or the code raises something the spec did not settle, pause the affected
   step and bring it to the user. If the spec changes, update it first (`../references/spec.md`).
7. Check every normative requirement against its passing check, and every adaptation against the spec's intent.
8. Set the spec's status to `Implemented` in the same change when it completes the spec.

## Done

A branch, or a PR when opening one is authorized, whose commits implement the spec. The reply maps each normative
requirement to the check that proves it, lists each adaptation of unmarked guidance with its reason, and names what
remains open or became a follow-up.
