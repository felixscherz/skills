---
name: create-benchmark
description: Capture a piece of real engineering work (a finished task, merged PR, or agent session) as a new Harbor benchmark task for the benchmarking-the-harness framework, or convert an old benchmark-<slug> skill into one. Use when the user wants to create, write, or add a benchmark, or turn something they just worked on into one.
disable-model-invocation: true
metadata:
  opencode/autoinvoke: false
---

# Create a benchmark

A benchmark is a real task from day-to-day work, frozen so candidates can
redo it: the repository as it was before the work, the request as it was
made, and a rubric for what a good result looks like. It is a Harbor task
directory, and the benchmarks together form the collection: the work the
user wants their environment to handle well.

Read `../benchmarking-the-harness/SKILL.md` first: it defines the vocabulary,
the setup (base image, agent, credentials), the blinding rules, and the
contract this skill produces.

A benchmark does not need a special aspect or trap. Its value is that it is
real work. A benchmark where every variant does well still earns its place:
it catches a variant that makes ordinary work worse.

A good benchmark is:

- **Real** - taken from actual work, not invented.
- **Reproducible** - every trial starts from the identical state.
- **Gradeable** - the user knows what a good result looks like, because they
  did the work.
- **Neutral** - it rewards good outcomes, not compliance with one variant.

## 1. Pick the work

Good sources: a task the user just finished with an agent, a merged PR, a
closed issue. A good candidate:

- is completable in one session from the repository alone,
- has a result the user has judged (reviewed, merged, corrected),
- does not need live systems: production data, secrets, deployed services,
  or a human in the loop,
- runs in a Linux container, with every tool it needs installable at a
  pinned version.

Prefer work where a plausible fix passes the tests but fails in reality,
e.g. a unit test that checks a generated string while the real tool rejects
it. Such work separates good engineering from lucky guessing. Work where
every reasonable attempt produces the same working result rarely separates
variants.

Gather, before writing any file:

- **Repository and base commit** - the state right before the work started,
  including uncommitted work in progress if there was any.
- **Request** - the original prompt, or the issue or ticket it came from.
- **Reference outcome** - the change that was merged or accepted.
- **What mattered** - review comments, corrections the user made to an
  agent's work, things that went wrong. These become rubric criteria.

Name the task after the work: `<repo>-<short-task>`, e.g.
`invoice-sync-retry-backoff`.

## 2. Decide where it lives

Tasks go in `<benchmarks>/tasks/<task>/`, the user's private benchmarks
directory (ask where; see "Where things live" in `benchmarking-the-harness`).
Never commit benchmark content into the skills repo, which is public: not
code, requests, or reviews, even from public repositories.

Start from the template:

```sh
cp -R <this skill>/assets/task-template <benchmarks>/tasks/<task>
cp <benchmarking-the-harness>/assets/judge.py <benchmarks>/tasks/<task>/tests/
```

Replace every `REPO`, `BASE_COMMIT`, `START_TREE` and `TEST_COMMAND`
placeholder.

## 3. Build the fixture

The fixture is the repository at the starting state, built by
`environment/Dockerfile` on top of `localhost/opencode-base`.

- **Pin it.** Store the repository as a `git bundle` of the base commit in
  `environment/<repo>.bundle`, so the build is offline and immune to
  force-pushes. If the work started on uncommitted changes, add them as a
  tarball of the working tree and lay it over the clone (the
  `seer-dotted-session` task shows how).
- **Remove the future.** A candidate must not find the answer in the
  repository. Bundle only the base commit's history, remove the remote, and
  expire the reflog. Check `git log --all` in the built image.
- **Record the start tree.** The judge diffs against the starting state, not
  the base commit, so the user's work in progress is not graded as the
  candidate's. Write the start tree in the Dockerfile with
  `GIT_INDEX_FILE=<tmp> git add -A && git write-tree`, assert its id there,
  and pass it to `judge.py --base`. Without uncommitted work, it is the base
  commit's tree, and the commit works too.
- **Make it runnable.** Install every toolchain and tool the work used, at
  the version it used, in the task's Dockerfile, never in the base image. A
  distribution package often has another version than the one the work ran
  against; build from source or download a release when the behavior under
  test depends on it. Build and test the project in the Dockerfile, so a
  broken fixture fails the build.
- **Blind it.** Place the repository at `/root/<repo>`. Give copied files
  neutral names (`<repo>.bundle`, not `fixture.bundle`); the reflog and
  history keep the paths they were cloned from.
- **Make the behavior observable.** The fixture must be able to show the
  behavior the task changes. If two outcomes the rubric distinguishes look
  identical in the container (e.g. every view prints "nothing configured"),
  add the data or config that makes them differ.

## 4. Write the task

`instruction.md` holds the prompt exactly as the user would type it.

- Use the original prompt if there was one. If the work came from an issue
  or ticket, write the prompt the user would have typed, and include the
  issue text the way the user would have pasted it.
- Resolve references the candidate cannot follow (internal links, chat
  threads) by inlining the content that mattered, or dropping it if it did
  not.
- Never add hints the original request did not contain, about the solution
  or about what the rubric looks at.
- A trial is one independent headless session: nobody answers questions,
  and a question or a confirmation request ends the trial without work.
  Adapt the prompt so it reads as a request to do the work start to finish.
  Drop invitations to stop and confirm ("Is it clear?", "Let me know before
  you start"). When the original session needed follow-up turns, fold the
  user's answers into the prompt, in the user's words, as if said up front.
  Keep genuine ambiguity in the request: the candidate should resolve it by
  stating an assumption and proceeding, which the rubric can grade.
- Record every change to the original prompt in `README.md` under Notes.

## 5. Write the verifier

Everything in `tests/` and `solution/` reaches only the verifier and the
oracle, never the candidate.

- **Checks.** `tests/test.sh` runs the project's own tests, and any check of
  the real behavior you can script, on a copy of the repository. Each check
  becomes a reward key through `judge.py --extra name=0|1`. A check that runs
  in place leaves build output in the diff the judge grades.
- **Reference.** Store the accepted change as `tests/reference.patch` and
  `solution/reference.patch`. It is one acceptable solution, not the only
  one; the rubric says so, so the judge does not penalize a different
  approach that also solves the problem.
- **Criteria.** 3-6 in `tests/rubric.md`, each a `## <id>: <title>` heading
  with a short kebab-case id, which becomes its reward key. Each must be
  gradeable from the trace, the diff, and the final reply. Cover:
  - whether the problem is actually solved, compared with the reference,
  - how the work was done: investigation before editing, verification
    before claiming done, questions asked or assumptions stated,
  - what mattered in the real review: scope, fit with the codebase's
    conventions, tests, the final report to the user,
  - anything that went wrong the first time.
- **Anchor every criterion** with what a full (2), partial (1), and failing
  (0) result looks like, concrete to this work: file names, the behavior, the
  specific mistakes seen in review. Each trial is graded alone, so vague
  anchors drift between trials and the judge scores on style.
- **Anchor on outcomes, not a list of solutions.** "Every target passed to
  the tool works for this input" holds for approaches you did not think of;
  a list of approved fixes marks down a valid one that is not on it.
- **Check anchors against the real system in the image.** Every claim an
  anchor makes about what works or fails (an API call, a CLI target, a
  config value) is checked once by running it inside the built image, and
  the check is noted in the rubric with the tool version. The judge follows
  anchors literally, so a wrong anchor scores a broken fix as full.
- **Cover every plausible reading.** When the prompt is ambiguous, write
  anchors for each reading a reasonable candidate could take, not only the
  one the user meant.
- **Variant-neutral.** Describe good outcomes, never "followed skill X". The
  benchmark must be able to show that a variant made things worse.
- **Trace expectations** (optional) are facts about the environment the
  coordinator checks in the trace, e.g. "loaded the engineering skill before
  editing code". They name skills or instruction files, which the judge must
  not see, so they go in `README.md`, never in `tests/`.

## 6. Write README.md and task.toml

`README.md` is for the coordinator. In this order:

1. **Work** - one paragraph on what the task is and what a good result
   achieves.
2. **Source** - repository, base commit, start tree, PR or session, date.
3. **Required layers** - e.g. `global`, or "none".
4. **Setup** - what the Dockerfile installs and why those versions, and how
   a candidate can reproduce the problem in the container.
5. **Notes** - changes to the original prompt, and what went wrong or
   needed correcting in the original work.
6. **Trace expectations** - if any.

In `task.toml`, `artifacts` names the repository directory, the verifier
stays `separate`, and `[verifier.env]` passes `JUDGE_MODEL` and the judge
provider's key from the coordinator's environment. Raise `agent.timeout_sec`
to what the original work took, with margin.

## 7. Validate

1. **Lint.** `harbor lint <benchmarks>/tasks/<task>` reports nothing.
2. **Leak check.** Build the image (`docker build -t <task> <task>/environment`)
   and look inside (`docker run --rm -it <task> bash`): no history after the
   base commit is reachable, no part of the reference is present. Grep the Dockerfile, the image's repository and
   `instruction.md` for the blinding words used in their meta sense.
3. **Oracle.** `harbor run -p <benchmarks>/tasks/<task> -a oracle` applies
   the reference and runs the verifier. The checks pass and the judge scores
   the diff-based criteria in line with the reference. Criteria graded from
   the trace score low, since the oracle has no trace.
4. **Dry run.** Run one trial per `benchmarking-the-harness` with the user's
   current environment (the `global` layer). The benchmark is ready when the
   candidate could work on the task without getting stuck on the fixture or
   stopping to ask the user, the variant reached it, and the judge's scores
   follow the rubric anchors. If the judge's scores disagree with your own
   reading, fix the anchors and `harbor job regrade` the run.

Record the dry run as an arena in `<benchmarks>/arenas/`. Remind the user to
commit the new task wherever it lives.
