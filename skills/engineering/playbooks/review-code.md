# Review code

Review a change against what its author meant it to do. The agent first establishes the intent and states it back, then
checks the change against it, and hands the user a review they can read, correct, and decide to post. A review changes
no code.

## Applies when

The user asks to review a pull request, a branch, or a set of code changes, their own or someone else's: "review this
PR", "code review", "review my branch", a PR number or URL.

## Who decides

- The user decides whether the review, or any comment from it, is posted to GitHub or anywhere else. The agent offers
  to post it once the user has read it.
- The user confirms the intent when the change does not state it clearly. A review against an unconfirmed intent says
  so at the top.
- The user confirms that a behavior change observable outside the codebase is acceptable.
- The agent decides the calibration, the findings, and their classification. It does not change code, commit, or push
  in this playbook.

## Steps

1. Gather the material: the PR description, the full diff, the commit messages, linked issues or tickets, and CI
   status. For a GitHub PR, `gh pr view <n>`, `gh pr diff <n>`, `gh pr checks <n>`, and `gh pr view <n> --comments`
   cover most of it. For a local branch, diff against the merge base with the target branch. Read linked issues and
   their discussion, including maintainer comments, and read the code around the diff, not only the diff.
2. Establish the intent. Write down in one or two sentences what the change is trying to achieve and why. Do not reject
   a description for following the project's own format. When the motivation is missing or too vague to review against,
   stop and ask the user whether the PR is theirs. For their own PR, ask for the motivation and offer to update the
   description with it. For someone else's, ask what they know, and offer to infer the intent from commits, issues,
   branch name, and code, marked as inferred and confirmed by the user before relying on it, and to draft questions for
   the author.
3. Calibrate scrutiny by blast radius and longevity, and state the calibration (`../references/code-review.md`).
4. Check the implementation against the intent: trace the main paths, check the invariants, and look for changes the
   intent does not explain and things it implies that are missing (`../references/code-review.md`). Read the principle
   references for what the change touches: `../references/domain-driven-design.md` and `../references/type-system.md`
   for the model, `../references/test-behavior.md` for the tests, `../references/dont-break-production.md` when
   observable behavior changes, and the language index for the language it is written in.
5. Check every new or changed name (`../references/code-review.md`).
6. Check every changed existing test, and every removal or weakening of verification
   (`../references/code-review.md`).
7. Classify each finding as blocker or non-blocker, with its location, what is wrong, why it matters, and a suggestion.
   Drop findings the code does not back up (`../references/code-review.md`).
8. Write the review (`../references/review-output.md`) and offer to post it.

## Done

The review in the reply, in the shape of `../references/review-output.md`, with an unconfirmed intent marked at the
top. Nothing is posted without the user's go-ahead. When the author or an agent acts on the review, the next playbook is
Address feedback.
