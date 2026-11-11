# Fix a bug

Make the code do what it was supposed to do, and nothing more. A fix restores the expected behavior at the place where
the bad state is created. It does not add features, clean up the surrounding code, or fix the other bugs found on the
way. Those become follow-ups.

## Applies when

The cause of a bug is known: a Find the cause diagnosis exists, or the user says what is wrong and what needs fixing.
When the cause is not known yet, run Find the cause (`find-the-cause.md`) first.

## Who decides

- The expected behavior is the one the code was meant to have. When it is unclear, or the fix would change behavior
  that callers rely on beyond restoring it, the user decides.
- The user decides when the right fix is larger than a fix: a model change, a redesign, or a change to a contract. The
  agent brings it with the smallest safe fix next to it and a recommendation.
- The user decides between a mitigation and a fix at the root, when the two differ.
- The agent decides how to reproduce, where the fix goes within the cause it was given, and how to commit it.

## Steps

1. State the bug in one line each: what should happen, what happens, and the cause. When the cause comes from the user,
   check it against the code before building on it. When the code says otherwise, bring it back to the user.
2. Write the failing test first, or take over the reproduction from Find the cause. Run it and confirm it fails for the
   stated cause (`../references/test-behavior.md`).
3. Fix the invariant where the bad state is created or owned, not where it becomes visible
   (`../references/find-the-root-cause.md`). A guard that only silences the symptom is not a fix. When the fix needs a
   preparatory refactor, it goes in its own commit before the fix.
4. Check the other producers and consumers of the same state for the same defect
   (`../references/find-the-root-cause.md`). Fix the instances that share this cause, and report the rest.
5. Run the test and the project's checks. Commit the test with the fix, and keep the output of the test failing without
   the fix for the PR.
6. When the fix changes behavior someone could rely on, even wrong behavior, apply
   `../references/dont-break-production.md`.
7. Ask whether the whole class of mistake can be caught automatically
   (`../references/never-make-the-same-mistake-twice.md`). Add the check when it is light, and propose it when it needs
   new tooling or CI setup.
8. Finish as Changing code in `../SKILL.md` describes.

## Done

A branch, or a PR when opening one is authorized, with the fix and its test. The reply states the bug, the cause, the
fix and where it sits, the test output before and after the fix, and the follow-ups: other instances found, adjacent
bugs, and the proposed check against the class of mistake.
