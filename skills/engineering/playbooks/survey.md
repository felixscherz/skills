# Survey a codebase

Go looking for friction on purpose, to find the work that would make a codebase easier to change. Day-to-day work runs
into friction by accident and raises it (When code resists in `../SKILL.md`). A survey goes to the places that matter
most and pushes on them the way real work would. It changes nothing, and ends in a ranked list of findings the user can
turn into tasks.

## Applies when

The user wants to apply forward pressure on a codebase: find what to improve or tasks to do, or asks where the codebase
is hard to work with, without naming a target. A question about how the code works is Investigate (`investigate.md`).
A request to improve a named module, or to act on a finding, is Refactor (`refactor.md`).

## Who decides

- The agent decides where to probe and how. It settles every finding by trying the work, not by reading the code for
  smells.
- The agent does not change product code, commit, or open a PR. Probes run in a throwaway worktree or scratch directory
  and are discarded (`../references/worktrees.md`).
- The agent asks only when the scope is too large to cover and neither `CONTEXT.md` nor the history points anywhere.
- The user decides which findings become work, in which order, and whether they go into the follow-up tracker.

## Steps

1. Read the nearest `CONTEXT.md` and name the core of the domain: the parts whose behavior matters most. From the
   history, find the files that change most often, and the commits that touched many files for a small change
   (`git log --stat`). Survey where the two overlap first.
2. For each of those wide commits, trace why every file had to change. A file that changed only because it knows
   something another file also knows is friction (`../references/friction.md`).
3. Probe each area by doing the work. Write a useful test of a key behavior through its public interface, as
   Refactor's test-led loop describes (`refactor.md`, `../references/test-behavior.md`), and try one or two changes the
   domain makes likely, such as a new case of an existing concept. Note every point where the work resists.
4. Write each friction down as `../references/friction.md` describes, and read the reference its signal points to.
5. Group the frictions by cause. Several signals with one cause are one finding. For each finding, name the cause and
   the shape that would remove it.
6. Rank the findings by what the friction costs against what removing it costs. Cost grows with how often the code
   changes, how many callers or people hit it, and how far its effect reaches. Note findings whose behavior has no
   tests to pin it, since a refactor has to write those first.
7. For each finding, name the next playbook: Refactor when the target shape is clear, Refactor with its test-led loop
   when it is not, Design when it needs a model change or reaches across services.

## Done

Nothing is committed. The reply opens with the top findings in a sentence each. Then, for each finding in rank order:
the cause, the evidence (the moments from step 3, files and lines, the commits from step 2), the shape that would remove
it, a rough size, and the next playbook. It ends with the areas surveyed and the ones left out. When the user picks a
finding, the next playbook is Refactor or Design. When the user asks, the findings go into the follow-up tracker.
