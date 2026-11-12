---
name: benchmarking-the-harness
description: Framework for testing how a change to an agent's environment (a skill, instruction file, settings) affects its behavior, by running Harbor tasks with opencode in containers and grading them blind. Use when the user wants to benchmark or compare skill variants, run an arena over their benchmark tasks, set up the opencode base image, or asks whether a skill change is actually better.
disable-model-invocation: true
metadata:
  opencode/autoinvoke: false
---

# Benchmarking the harness

A skill change affects every future session, so treat it as an experiment:
hold everything constant except the change, hide from the agents that they
are being measured, and grade the outcomes blind.

Benchmarks are [Harbor](https://harborframework.com) tasks and run with the
`harbor` CLI, so everything Harbor offers (jobs, retries, `harbor view`,
`harbor job regrade`, `harbor lint`) works on them. This skill adds the method,
an opencode base image every task builds on, an agent for it, and a judge.
The tasks themselves are captured from real work with `create-benchmark`.

## Primitives

Use these terms when designing, running, and reporting benchmarks.

- **Benchmark** - a piece of real engineering work, captured for reuse as a
  Harbor task directory (see "Benchmark contract").
- **Collection** - all benchmarks together, a directory of tasks that Harbor
  reads as a dataset: the work the environment should handle well.
- **Fixture** - the starting state a candidate works in, built by the task's
  `environment/Dockerfile`.
- **Task** - the prompt, worded exactly as a user would type it:
  `instruction.md`.
- **Checks** - deterministic tests the verifier runs on the result, e.g. the
  project's test suite. Optional.
- **Rubric** - 3-6 criteria in `tests/rubric.md`, graded by the judge.
- **Environment** - everything a candidate sees besides the task and fixture:
  skills, the global instruction file (AGENTS.md), opencode settings.
- **Layer** - a named snapshot of environment pieces:
  `layers/<name>/{skills/,AGENTS.md}`, e.g. `global` (the user's real setup)
  or `engineering-v2`.
- **Variant** - one environment under test: a job config with one agent entry
  that names its layer. The **control** is the baseline variant (current
  version, or nothing). Every arena has a control.
- **Constants** - what is identical for every variant: base image, agent,
  opencode version, model, attempts, timeouts, tasks.
- **Arena** - one experiment: benchmarks x variants x constants x attempts.
- **Trial** - one Harbor trial: one candidate run of one variant on one
  task, then the verifier. Run several per variant (`n_attempts`); a single
  run is an anecdote.
- **Candidate** - the agent executing a trial. It never knows it is in an
  arena.
- **Coordinator** - the agent running the arena.
- **Judge** - an LLM that grades one trial against the rubric from inside
  the verifier, seeing the diff, the final reply, and the redacted trace,
  never the variant.
- **Trace** - a trial's transcript, the ground truth for what the candidate
  did, as opposed to what it claims: `agent/trajectory.json` in the trial
  directory.
- **Verdict** - the judge's per-criterion scores and reasons:
  `verifier/verdict.json`. Harbor's reward (`verifier/reward.json`) holds one
  key per criterion and check, plus `reward`, their mean.
- **Leak** - any signal that reveals the evaluation, the variant, or other
  trials to a candidate, or the variant to the judge. A leak invalidates the
  trial.
- **Finding** - the coordinator's conclusion: promote, reject, or
  inconclusive.

## Setup

Once per machine, and again when the opencode version changes:

- `harbor` (`uv tool install harbor`) and a Docker-compatible engine. Podman
  works: Harbor builds task images with `docker compose build`, and needs
  `docker buildx` only for network allowlists.
- **The base image.** `scripts/build-base.sh [opencode-version]` builds
  `localhost/opencode-base:<version>`, also tagged `latest`, from
  `assets/base/Dockerfile`: Debian
  with git, python3, ripgrep and the opencode release binary. It builds for
  the engine's native architecture, arm64 on Apple silicon. Never pass
  `--platform linux/amd64`: emulation makes every trial several times
  slower. Task Dockerfiles start `FROM localhost/opencode-base`; the
  variant's `kwargs.version` pins the version, and a trial fails when the
  image has another one.
- **The agent.** Job configs use
  `import_path: harbor_agents.baked_opencode:BakedOpenCode`. Run Harbor with
  `PYTHONPATH=<this skill>/assets`. Harbor's built-in `opencode` agent targets
  opencode 1 and reinstalls it on every trial; `BakedOpenCode` checks the
  version baked into the image instead, and fails the trial on a mismatch
  rather than run another agent than the one under test.
- **Credentials.** The agent and the judge get the provider's API key from
  the environment (e.g. `DEEPSEEK_API_KEY`), never from the user's opencode
  login. Use a provider with an API key, and load it from an `.envrc` that
  stays out of every repository. Never print it.

## Where things live

Benchmarks from private code, and every arena record, live in the user's
private benchmarks directory (ask where; e.g. `~/workspaces/personal/benchmarking`):

```
<benchmarks>/
  .envrc                     # API keys, never committed
  tasks/<task>/              # the collection
  layers/<layer>/            # skills/, AGENTS.md
  arenas/<date>-<variable>/
    constants.yaml           # jobs_dir, n_attempts, tasks; no agents
    variants/<variant>.yaml  # job_name and the one agent entry
    jobs/<variant>/          # Harbor's output
    finding.md
```

Run commands from `<benchmarks>`; paths in the configs are relative to it.

## Environments start empty

The base image has no skills and no instruction file. A candidate gets only
what its variant names: `skills:` (Harbor copies them to
`~/.config/opencode/skills`) and `kwargs.instructions` (installed as
`~/.config/opencode/AGENTS.md`). For the user's global setup, snapshot it
with `scripts/global-layer.sh layers/global`. It resolves symlinks and strips
`benchmarking-the-harness`, `create-benchmark`, `benchmark-*` and `synced`
(Claude Code's eval tooling). Copy the snapshot to build another layer, and
edit the copy.

When a layer removes a skill, also remove instruction lines that point to it
(e.g. "load the `engineering` skill" in `AGENTS.md`), so the control is the
environment without that skill, not one with a dangling reference.

Never change a layer an arena has used; make a new one. Never use Harbor's
`extra_instructions` for a variant: it changes the task, not the
environment, and the candidate sees it.

Verify the variant from the first trial's trace: the skills it could list
and load, and the AGENTS.md lines it followed.

## Blinding

Candidates:

- None of these words appear in `instruction.md`, the fixture, or a layer,
  used in their meta sense: benchmark, eval, test, judge, experiment, rubric,
  score, compare, arena, trial, candidate, variant, control, harbor.
- The repository sits at a path a user might choose (`/root/<repo>`), never
  under a name that hints at the task.
- The task states the goal, not what is measured. Never ask a candidate to
  list which skills or rules it followed; grade that from the trace.
- Each trial runs in its own container. Candidates share no state.
- Harbor itself leaves `/logs/agent`, `/logs/verifier` and `/logs/artifacts`
  in the container. `tests/` and `solution/` only arrive after the candidate
  is done. This residual is the same for every variant, so it cannot favor
  one; flag a trace that explores it.

Judge:

- The judge runs in the verifier, which never sees the job config, so it is
  blind to the variant by construction. It may know it is judging.
- `assets/judge.py` drops every trace event that touches the environment
  (skill loads, reads of skill or instruction files) without a marker, since
  a count of markers reveals the variant, and replaces skill names in the
  candidate's prose. A task's `tests/redact.tsv` adds rewrites for other
  giveaway phrases.
- After the pilot, read a `verifier/trace.txt` and grep it for skill names,
  reference file names, and environment paths. Fix the redaction on any hit.

Each trial is graded alone, so scores are only comparable when the rubric's
anchors are concrete. Vague anchors drift between trials.

## Running an arena

1. **Frame.** Name the variable under test, the control, the constants, and
   `n_attempts`. State which result would promote the variant. To assess a
   variant across the collection, run every task in the same arena.
2. **Build.** Create the layers, `constants.yaml`, and one
   `variants/<name>.yaml` per variant. The agent entries differ only in
   `skills` and `kwargs.instructions`: compare
   `harbor run -c constants.yaml -c variants/<v>.yaml --print-config` across
   variants. Harbor appends `agents` lists across `-c` files, so the agent
   entry lives in the variant file only.
3. **Check for leaks.** Read every `instruction.md` and fixture against the
   blinding rules, and check the grep output of `global-layer.sh`.
4. **Pilot.** Run one attempt per variant per task (`-k 1`) before the full
   arena. It tests the setup, not the variant: images build, the variant
   reaches the candidate, candidates work to the end without stopping to
   ask, the judge follows the anchors. A pilot can also surface a real
   finding about the variant, e.g. a skill that makes the agent stop and ask
   where it should work; record it as a result, not only as a setup problem.
5. **Run** each variant:
   `PYTHONPATH=<this skill>/assets harbor run -c <arena>/constants.yaml -c <arena>/variants/<v>.yaml -y`.
   Rerun with a higher `n_attempts` to add trials; constants and layers stay
   unchanged.
6. **Verify outcomes yourself.** Before trusting a verdict, check results
   against the real system: build them from the trial's `artifacts/`, run the
   binary, reproduce against the real dependency. Passing tests are not
   enough; a candidate's unit test can confirm a fix the real tool rejects.
7. **Analyze.** Compare variants per reward key from each job's
   `result.json` (or `harbor view <arena>/jobs`). Read the verdicts where the
   variants differ. Check the task README's trace expectations against
   `agent/trajectory.json`. Where a verdict disagrees with your own
   verification, suspect the rubric first: fix the anchors, then rerun only
   the verifier on every job of the arena, which writes a new job and leaves
   the old one as it was:
   `PYTHONPATH=<this skill>/assets harbor job regrade <arena>/jobs/<v> -p tasks -o <arena>/jobs --job-name <v>-regrade -y`.
8. **Report** the finding in `finding.md`. Too few trials or a noisy spread
   is inconclusive, not a win.

## Running candidates

- A trial runs `opencode run --standalone --auto` inside its container, which
  approves every tool call there. The container confines the candidate's
  filesystem; it still has network access, so a public upstream repository
  is reachable. Flag a trace that fetches the answer.
- A candidate that asks a question or asks for confirmation ends the trial,
  because nobody answers. Write tasks that call for the whole job (see
  `create-benchmark`), and grade a trial that stopped to ask as a result, not
  a harness failure.
- An `AgentTimeoutError` is a result too: the work so far is still graded.
- opencode's exit code says little. Judge whether a trial finished from its
  final reply and diff.
- Toolchains a task needs (Go, Rust, a database) belong in the task's
  Dockerfile, pinned to the version the work used, never in the base image.

## Benchmark contract

A benchmark is a Harbor task directory that passes `harbor lint`:

```
<task>/
  task.toml            # separate verifier; artifacts = ["<repo dir>"]; judge env
  instruction.md       # the prompt as a user would type it
  README.md            # coordinator only: work, source, notes, trace expectations
  environment/
    Dockerfile         # FROM localhost/opencode-base; builds the fixture
  tests/
    test.sh            # checks on a copy of the repo, then judge.py
    judge.py           # copy of assets/judge.py
    rubric.md          # "## <id>: <title>" criteria with 0/1/2 anchors
    reference.patch    # the accepted change, judge only
  solution/
    solve.sh           # applies reference.patch, for `harbor run -a oracle`
    reference.patch
```

The verifier runs `separate`: in a fresh container from the same image, with
the candidate's repository copied back in from `artifacts`. The judge finds
the trace and the request in `/logs/artifacts/agent`, where `BakedOpenCode`
puts them. To create a new benchmark, use the `create-benchmark` skill.

## Report

Variable under test, control, constants, attempts per variant, rubric,
reward per key per variant, trace observations, your own reading where it
differs from the judge, finding. Across the collection, report per task: a
variant that improves some tasks and regresses others is not a plain win.
