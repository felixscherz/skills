# Code review

A review has two jobs:

1. Confirm that the reviewer understood the change the way the author meant it.
2. Find what stands between the change and merging it.

The first job is the one that usually gets skipped. Without a stated intent, a
reviewer can only check that code looks reasonable, not that it does what it
was supposed to do. So intent comes first, and a review restates the change in
the reviewer's own words so the author can catch a mismatch.

## Calibrate scrutiny

Not every line deserves the same depth. Assess each area of the change along
two axes and spend attention accordingly:

- **Blast radius** - how much breaks, and how badly, if this is wrong. Auth,
  payments, data migrations, shared libraries, public APIs and anything
  touching persistent data sit at the high end.
- **Longevity** - how long this code will live and how much will be built on
  it. A one-off script or a throwaway experiment sits at the low end. Core
  domain concepts sit at the high end.

Weight modelling over mechanics. A core domain concept deserves close
attention to whether its invariants hold, whether it is expressed in the right
terms, and whether the boundaries sit in the right place. A mistake there
spreads into everything built on top and is expensive to undo. An adapter at
the edge (a database adapter, an HTTP client, a serializer) still has to be
correct, but a clumsy one is cheap to replace later.

## Check the implementation against the intent

- Trace the main code paths end to end. Does the behavior match the stated
  goal, including edge cases, error paths, concurrency, and empty or invalid
  input?
- Do the invariants of the affected domain concepts still hold after the
  change, on every path that mutates them?
- Do the tests exercise the intended behavior, or only the happy path or the
  implementation details?
- Is there anything in the diff the intent does not explain? Unexplained
  changes are either scope creep or a sign the stated intent is incomplete.
  Ask about them.
- Is anything the intent implies missing from the diff?

## Naming

Names are how a codebase carries its model. Check every new or changed name
(types, functions, modules, fields, variables with a wide scope, config keys,
endpoints):

- Does it say what the thing is or does, without reading the implementation?
- Does it match the domain language used elsewhere in the codebase and by the
  people who own the domain?
- Is the same concept named the same way everywhere, and are different
  concepts named differently?
- Does it still fit after the change, or did the thing's meaning drift while
  the name stayed?

An unclear name, a better name that is clearly available, or a name that does
not align with the model is a **blocker**. Suggest the alternative.

## Changes to existing tests

New tests describe new behavior. A changed existing test means the behavior
it pinned down has changed, or the test was bent to make the build pass.
Either way it deserves extra attention, because it is where a regression
shows up in the diff while the rest of the change looks fine.

For every existing test whose assertions, inputs, expected values, fixtures,
snapshots, or golden files changed:

- Name the behavior the test pinned before and what it pins now.
- Check that the behavior change is part of the stated intent. A behavior
  change the description does not mention is an open question at least.
- Check who else relies on the old behavior: callers, users, other services,
  stored data (see `dont-break-production.md`). An intended change can still
  break someone.
- Confirm with the user that the behavior change is acceptable when it is
  observable outside the codebase.

A test that only moved, was renamed, or was rewritten against a new internal
API while asserting the same behavior is a refactor. Say so and move on.

## Removed or weakened verification

Treat any removal or weakening of verification as suspicious until justified.
Enumerate every instance explicitly, for example:

- deleted test files or test cases
- tests marked skip, xfail, only, or commented out
- loosened assertions, widened tolerances, updated snapshots or golden files
- mocks introduced where a real dependency was used before
- CI jobs or steps removed, made optional, or set to continue on error
- lowered coverage thresholds, disabled lint rules, added ignore comments
- changed timeouts or retry counts that could hide flakiness

For each one, find the justification in the description, the commits, or the
code itself (for example, the tested behavior was intentionally removed). The
question is whether the change to verification follows from the intended
change to behavior, or whether it was made to get a red build green. If no
justification exists, it is a **blocker**.

## Classify findings

- **Blocker** - must be resolved before merging. This includes: the change does
  not achieve its intent, broken invariants, correctness or security bugs,
  data loss risk, naming problems as defined above, an unexplained behavior
  change in an existing test, unjustified test or CI removal, and missing or
  unconfirmable intent.
- **Non-blocker** - worth raising, fine to merge without. Suggestions, style,
  small refactors, follow-up ideas, questions that do not affect correctness.

Weigh severity by the calibration above. The same flaw can be a blocker in
core domain code and a non-blocker in a throwaway script, except for the
categories named above as blockers.

Every finding needs a location (`path:line`), what is wrong, why it matters,
and a concrete suggestion. Drop findings you cannot back up with the code.
