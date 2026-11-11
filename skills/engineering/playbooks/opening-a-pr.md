# Opening a PR

A change is not done until it is integrated. Opening a PR means getting it past every automated check and in front of
a reviewer with enough context to judge it quickly. The reviewer is usually the user, and their question is not only
"is this correct" but "is this what I want".

## Applies when

A change is done and needs to be pushed and integrated through a pull request or merge request, or an open PR's
description needs writing or updating. Build a feature ends here.

## Who decides

- The user decides whether to push, open a PR, and merge. Without their go-ahead, stop at a reviewable branch and
  report it (`../references/keep-work-reviewable.md`). Never merge unless the user asks.
- The agent decides the commit split, the description, and fixes for failing checks.

## Steps

1. Run the same checks CI runs: tests, linters, formatters, type checks, and pre-commit hooks. Find them in the CI
   config (`.github/workflows/`, `.gitlab-ci.yml`, ...), `Makefile`, `justfile`, or package scripts rather than
   guessing. Everything must pass. Never skip, weaken, or delete a check to get green. If a check fails for a reason
   unrelated to the change, confirm that by running it on the default branch, and say so in the PR.
2. Read your own diff as a reviewer would. Remove debug output, commented-out code, and unrelated changes. Split the
   commits so each is one reviewable unit, and propose stacked PRs when the change is too large for one review
   (`../references/keep-work-reviewable.md`).
3. Write the description (`../references/pull-request-description/pull-request-description.md`).
4. Push and open the PR with the platform's CLI: `gh pr create` for GitHub, `glab mr create` for GitLab. Pass the
   description through a file (`--body-file`) so formatting survives. Target the branch the repository integrates
   into, usually the default branch. Open it as a draft only when it still needs input before it is reviewable, and
   say what input.
5. Watch CI (`gh pr checks --watch`) and fix failures. A PR with red CI is not done.
6. When feedback or new commits change the scope, update the description so it still matches the diff.

## Done

The reply holds the PR link and its CI status, with CI green or each remaining failure explained, and names anything
the reviewer has to decide, such as a breaking change or a draft's missing input. The next playbook, once a reviewer
responds, is Address feedback (`address-feedback.md`).
