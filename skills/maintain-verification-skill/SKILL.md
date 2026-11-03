---
name: maintain-verification-skill
description: Audit a project's verify-<app> skill in .agents/skills/ against CONTEXT.md, the source, and the running app, and ship the proven corrections in one PR. Use when the user runs /maintain-verification-skill, asks to "audit", "update", or "refresh the verify skill", or a verify-<app> skill failed because the app changed. Not for creating one (use create-verification-skill).
disable-model-invocation: true
metadata:
  opencode/autoinvoke: false
---

# Maintain a verification skill

A verify skill goes stale as soon as the app changes: a button is renamed, a command gains a flag, a feature appears
that the map does not cover. This skill is the pass that brings a skill made by `create-verification-skill` back in
line with the app. It covers every feature twice, once from the source and once live, and ends in one of three
outcomes:

- **Clean** - every feature was covered and nothing needed fixing. No branch, no PR.
- **Changed** - one PR with the proven corrections.
- **Blocked** - coverage could not finish, or a fix could not ship safely. Say exactly what blocked it.

## Scope

Edit only the skill's own directory: `SKILL.md`, `features/`, and its `scripts/`. Never change product code in this
pass. When the app no longer does what a feature file describes, decide which it is:

- **Drift** - the app changed on purpose, and the map is out of date. Fix the map.
- **Product bug** - the app is broken. Report it, and leave the map describing the intended behavior.

`CONTEXT.md` is the other exception: when an entry the pass relies on is wrong, such as a feature listed under an old
name or a link to the wrong place, fix the entry in its own commit (see `../engineering/references/context.md`).

## Steps

1. **Find the skill.** Look for `.agents/skills/verify-*/`. When there are several, ask which one. When there is none,
   stop and point to `/create-verification-skill`.
2. **Read the context map.** Read the root `CONTEXT.md`, its "Read when" links that cover the features, and the
   skill's `SKILL.md`. Compare the features in `CONTEXT.md` with the files in `features/` and the skill's feature list:
   - a feature in `CONTEXT.md` without a file is a gap,
   - a file without a feature in `CONTEXT.md` was renamed or removed, or `CONTEXT.md` is stale. Check the code to tell
     which,
   - fix links in the skill's feature list that point to missing files.

   Also look at what changed recently (`git log` since the skill last changed) for user-facing surfaces that neither
   lists. Name a gap only with the code path that shows the feature exists.
3. **Read the source per feature.** For each feature file, read the code `CONTEXT.md` points to and answer: how does a
   user reach and use this feature today, and where does the feature file disagree? Cite the file for each
   disagreement. When the harness supports subagents, give each feature to its own read-only subagent in parallel.
   They read, they do not drive the app or edit files, and each returns: a summary of the feature, its entry points,
   the drift it found or "none", and one recipe to verify it live.
4. **Reconcile.** Every feature has a result. Spot-check the drift that was reported; do not re-check claims that came
   back clean. Merge the recipes so the live pass needs as few app states as it can.
5. **Drive every feature live.** This is required even when the source looked clean. You do all the driving yourself,
   following the skill's own Launch section: one instance driven feature by feature for a server or UI, a fresh
   session per drive for a short-lived CLI. Exercise every feature at least once, and keep three rules the whole way:
   - Never drive an instance that has not passed doctor since it last surprised you. Run doctor before the first
     drive, on every fresh session, and after every failed drive. When doctor cannot see the problem, such as a UI
     stuck in a modal, reset the state or relaunch.
   - Evidence survives every cleanup. Check it at its named location, do not assume it.
   - Nothing a drive started outlives the drive's use. Clean up after every failed attempt, whether the session hung,
     exited, or is shared. On a shared instance, clean up what the attempt left, not the instance.

   When doctor fails because the skill is wrong, that is drift: fix it, restart what the fix affects, and retry once
   before calling the pass blocked. A feature is unreachable only with the concrete prerequisite it needs (an account,
   an entitlement, an OS, external state) and the route you tried. When the feature file does not mention that
   prerequisite, that is drift too. Run the final cleanup after the last drive, including the re-drives in step 6.
6. **Sort what you found.**
   - **Drift** - the feature file or `CONTEXT.md` describes the app wrong. Fix it.
   - **Harness gap** - the app works, but the skill cannot drive it. Fix the harness, keep helper scripts executable
     with their invocation in `SKILL.md`, and drive the feature again with the fix before it ships.
   - **Product bug** - the app is broken. Record it for the user. It stays out of the PR.
   - **Gap** - a feature from `CONTEXT.md` without a file. Map it when it can be driven, following
     `../create-verification-skill/references/feature-example.md`, and prove it live like any other feature.
7. **Ship or stop.** For Changed, reread every changed file, then run Opening a PR from the engineering skill
   (`../engineering/playbooks/opening-a-pr.md`). For Clean or Blocked, open nothing.

Keep run notes (features covered, prerequisites of unreachable features, drift confirmed) in a scratch location outside
the repository. Do not commit them.

## Done

The reply states the outcome, the features covered from source and live, the drift fixed, the product bugs found, the
unreachable features with their prerequisites, and the PR when there is one.
