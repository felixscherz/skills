# Refactor

Change the structure, keep the behavior. A refactor starts by agreeing with the user which behavior it preserves, pins
that behavior with tests, and then moves the code in steps that keep the tests green. It adds no features and fixes no
bugs: either one changes behavior and becomes its own change.

## Applies when

The user asks to restructure code without changing what it does: rename, move, split, or merge modules, change an
internal API, remove duplication, or reshape code toward a model that fits it better. It also covers making a module
deeper: giving callers a simpler interface and moving into the module the complexity they carry today. A module can be
a package, class, function, or another unit with an interface and an implementation.

## Who decides

- The user agrees which behavior is preserved, and which internal interfaces may change along the way.
- The user decides the target shape when the refactor is broad or changes a module's interface: it touches many
  modules, changes an interface other teams use, or introduces a new pattern to the codebase.
- When the refactor turns up a bug or a missing feature, or would break a consumer outside the codebase, the user
  decides what happens to it. The agent does not fix it in the refactor.
- The agent decides the order of the moves and the commit split.

## Steps

1. Set the expectations. List the behavior the refactor preserves, as callers observe it: the public API, outputs,
   errors, side effects such as events and writes, and invisible semantics such as ordering, retries, and durability
   (`../references/dont-break-production.md`). List the interfaces that may change, such as internal functions and
   their callers. For a module's interface, start from its callers: trace them, list the jobs they do and the behavior
   they rely on, and find consumers outside the codebase, such as callers of a package and readers of a wire format.
   Agree both lists with the user before touching code.
2. Pin the preserved behavior. Find the tests that cover it through the public API, at a level that survives the
   change (`../references/test-behavior.md`). Where it is not covered, write the missing tests against the current code
   and see them pass. Type checks and lint are not a pin.
3. Name the target shape: the concept the code is missing, or the drift it fixes, and what the modules and types look
   like after (`../references/redesign-from-first-principles.md`, `../references/program-design.md`,
   `../references/domain-driven-design.md`, `../references/type-system.md`). When the refactor is broad, propose it
   with the old and new shape side by side and wait for the user.
4. When the target is a module's interface, find the complexity callers carry that the module could own and record the
   depth measures (`../references/deep-modules.md`). Sketch at least two different interfaces as caller code, propose
   one with caller code before and after, and wait for the user.
5. Start a branch or worktree (`../references/keep-work-reviewable.md`) and commit the pinning tests first, on their
   own.
6. Move in small steps that keep the pin green, and commit each one. Keep mechanical commits, such as renames and
   moves, apart from reshaping commits. Migrate every caller of a changed internal interface and delete the old one in
   the same change, unless outside consumers need it kept. Check renames against strings, config, and docs that the
   type checker does not see.
7. Do not change the assertions of a test that pins preserved behavior. When a test has to change, it either pinned an
   internal detail or the behavior is changing. Say which in the commit message, and bring a behavior change to the
   user.
8. When you find a bug or a missing feature, write it down as a follow-up and keep its current behavior.
9. Check the result against step 1: every preserved behavior passes its pin, and only the listed interfaces changed.
   For a module's interface, take the depth measures again and compare caller code with the agreed target.
10. Finish as Changing code in `../SKILL.md` describes.

## Done

A branch, or a PR when opening one is authorized, whose commits change the structure and leave the pinned behavior
unchanged. The reply names the preserved behavior and the tests that pin it, the shape before and after, the
interfaces that changed, and the bugs and features found along the way as follow-ups. For a module's interface, it
shows caller code before and after with the depth measures, and how outside consumers are handled.
