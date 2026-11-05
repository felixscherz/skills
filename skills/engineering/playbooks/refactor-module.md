# Refactor a module

Make a module deeper: give callers a simpler interface and move into the module the complexity they carry today,
without changing the behavior they rely on. A module can be a package, class, function, or another unit with an
interface and an implementation.

## Applies when

The user asks to improve a module's interface, hide its implementation, make it deeper, or make it easier to use,
without changing what it does. For other structural changes, such as renames, moves, or removing duplication, use
Refactor (`refactor.md`).

## Who decides

- The user agrees the target interface, its boundary, the preserved behavior, and the scope before code changes.
- The user decides what happens to bugs and missing features found on the way, and to any break for consumers outside
  the codebase. The agent does not fix or add them in the refactor.
- The agent investigates, recommends a target, and decides the order of the moves and the commit split.

## Steps

1. Map how the module is used. Trace its callers and list the jobs they do, the interface they use, and the behavior
   they rely on, including errors and side effects. Find consumers outside the codebase too: callers of a package, and
   readers of any wire format such as a database schema or an HTTP payload (`../references/dont-break-production.md`).
2. Find the complexity callers carry that the module could own, and record the depth measures
   (`../references/deep-modules.md`).
3. Sketch at least two different target interfaces as caller code, with what stays internal and where the boundary
   sits. Propose one, with caller code before and after, the preserved behavior, and how outside consumers are
   protected, and wait for the user (`../references/deep-modules.md`, `../references/program-design.md`).
4. Pin the preserved behavior with tests that pass against the current code, at a level that survives the interface
   change, and commit them first on a branch (`../references/test-behavior.md`,
   `../references/keep-work-reviewable.md`).
5. Migrate in small commits that keep the pin green. Move callers to the new interface and delete the old one, unless
   outside consumers need it kept. Do not change a pinning test's assertions; write bugs and missing features down as
   follow-ups.
6. Check the result: take the depth measures again, compare caller code with the agreed target, and confirm the pin
   passes.
7. Follow Opening a PR (`opening-a-pr.md`) when authorized.

## Done

The module has the agreed interface and the pinned behavior is unchanged. The reply shows caller code before and after
with the depth measures, names the tests that pin the behavior and how outside consumers are handled, and lists
follow-ups.
