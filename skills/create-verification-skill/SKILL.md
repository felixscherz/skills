---
name: create-verification-skill
description: Generate a project-local verify-<app> skill in .agents/skills/ that launches the real app, drives its features the way a user does, and captures proof that they work. Use when the user runs /create-verification-skill, asks to "make a verify skill" or "a way for agents to drive this app", or a repository has no scripted way to see a change working in the running app. Not for writing tests, and not for a repository that already has a verify-* skill (use maintain-verification-skill).
disable-model-invocation: true
metadata:
  opencode/autoinvoke: false
---

# Create a verification skill

Tests prove that code does what its author meant. A verification skill proves that the running app does what a user
needs: it starts the app, drives a feature through the same surface a user touches, and captures evidence of the
result. This skill writes that as a project-local skill, `.agents/skills/verify-<app>/`, for one repository.

The reader of the generated skill is another agent, in the middle of a task, that has never run this app. Every step
has to work for that reader without guessing.

The generated skill has a narrow job. What the app is, what its features are, and where their code lives belong in the
repository's `CONTEXT.md` (see `../engineering/references/context.md`). The verify skill names features the way
`CONTEXT.md` does and holds only what `CONTEXT.md` should not: how to run the app, drive each feature, and prove the
result.

## Who decides

- The user decides which surface to verify when the app has several (a web UI and a CLI, say) and none is clearly
  primary, and anything that needs credentials, paid services, or accounts the agent does not have.
- The agent decides the harness, the helper scripts, and which features to map first.
- Ask only what the repository cannot answer.

## 1. Read the context map

Read the `CONTEXT.md` at the repository root first, and follow the "Read when" links that cover running the app, its
architecture, or its features. From it, take:

- **The app** - what it does and for whom, and its name for `verify-<app>`.
- **The features** - the "Features" list, or `docs/feature_map.md` when it has moved there. These are the features the
  map will cover, under the same names.
- **Where to look next** - the modules and documents it points to for each feature.

Go to the code only for what `CONTEXT.md` does not say. When there is no `CONTEXT.md`, explore the code as usual and
do not offer to write one. When there is one and it turns out to be wrong about something you need, such as a feature
that no longer exists or a link to the wrong place, fix the entry as part of this work.

If `.agents/skills/` already has a `verify-*` skill, stop and point the user to `/maintain-verification-skill`.

## 2. Answer five questions

Answer each from what you read, with the command, file, or handle that backs it:

1. **Surface** - what does a user touch: a web UI, a CLI or TUI, a desktop app, an HTTP API, a mobile app, a library?
   Pick the primary one and note the others.
2. **Run** - how does the app start locally? Prefer the repository's own command (package scripts, `Makefile`,
   `justfile`, README) over one you assemble. Note ports, environment variables, migrations, seed data, and auth.
3. **Drive** - how can an agent act as a user? Reuse what the repository has first: end-to-end specs (Playwright,
   Cypress), PTY or expect helpers, HTTP fixtures, a debug port. Otherwise pick the plain recipe for the surface: a
   browser over CDP or Playwright for web and Electron, tmux or a PTY for a CLI or TUI, `curl` for an HTTP API.
4. **Observe** - what evidence can be captured: screenshots, accessibility snapshots, terminal transcripts, response
   bodies, exit codes, logs, rows in a database, files on disk?
5. **Isolate** - can a verification run start its own instance without touching the user's (its own port, data
   directory, profile)? If not, the generated skill says so and refuses to drive an instance it did not start.

## 3. Get it running

Start the app from a clean checkout before writing anything. A skill written against an app that does not start
teaches steps that were never true. When it does not start, fix the cause if it is small and in scope, or report it
precisely and stop. When startup fails only for something verification does not need, such as a missing sample config,
the skill may create it as marked verification scaffolding and remove it during cleanup.

## 4. Write the skill

Write `.agents/skills/verify-<app>/SKILL.md`. Unlike this skill, it must be auto-invokable: no
`disable-model-invocation`, no `opencode/autoinvoke`, and no `agents/openai.yaml` policy. Agents should load it on
their own whenever they need to see a change working.

Its frontmatter has `name: verify-<app>` and a single-line `description` that routes: it names the app and the
surface, and the situations to load it in, such as "after changing <app>'s behavior, before calling the change done",
"when asked to try, check, or reproduce something in the running app", and "to capture screenshots or transcripts as
proof". It ends with what the skill is not for, such as unit tests.

The body opens with one line: for what a feature does and where its code lives, read `CONTEXT.md`; this skill covers
only how to run, drive, and prove it. Then these sections, each filled with what you found, never with placeholders:

- **Launch** - the exact command that starts an isolated instance, and the signal that it is ready. Ready means a user
  could use it, not that a process answers: a database can accept connections while its migrations still run. Launch
  starts from an empty data directory, including migrations and seed data. For a short-lived CLI there is no server:
  launch builds or installs once, and each drive runs in its own PTY or tmux session.
- **Doctor** - one read-only check that the instance is worth driving: the process is up, it is the build under test,
  the port belongs to this run, auth works. Run it before the first drive and again after anything surprising.
- **Drive** - how to act as a user through the harness, with this repository's real selectors and commands. Prefer
  handles that survive a redesign: accessible roles and names, `data-testid` attributes, prompt strings, routes. Avoid
  coordinates, tab order, and DOM position.
- **Proof** - what counts as evidence and where it is written. The rules:
  - Drive the path a user takes, not internal setters or test-only endpoints.
  - Capture the action and the state that followed, not only the final screen.
  - Check side effects through a second view (the file written, the row inserted, the message sent), not only what the
    screen shows.
  - Mock only at a boundary production already isolates, such as a payment provider.
  - Do not trust a dry-run or test mode by its name. Observe what it skips (network, files, git refs) before relying on
    it.
- **Cleanup** - how to stop what the run started. Stop processes by the PID or session the run recorded, never by
  name. Cleanup removes instances and scratch state and keeps the evidence, in a location the skill names outside the
  scratch state.
- **Features** - one line per mapped feature, by its `CONTEXT.md` name, linking to its file in `features/`.

Put helper scripts in `scripts/`, make them executable, and show their invocation in the body. A helper the reader has
to read to use is not a helper.

## 5. Map the first features

Write one file per feature in `features/`, named after the feature, for the three to five features users rely on most,
taken from `CONTEXT.md`. Follow `references/feature-example.md`. Each file says how to reach the feature as a user, how
to drive it with exact commands and the observable result of each step, what to keep as proof, and the traps.

A feature file does not repeat what `CONTEXT.md` says about the feature or its code. When the seed data lacks
something a step needs, the step fails and the reason goes under Gotchas. Never weaken a step until it passes.

## 6. Prove the skill

Follow the generated skill yourself, end to end, once: launch, doctor, drive one mapped feature, capture its proof,
clean up. Then check that the proof is still at its named location. Fix what failed and run cleanup after every failed
attempt, so attempts do not leave processes and ports behind. A skill that was never run is a draft.

When you proved it somewhere other than where it will run, such as a container instead of a fresh machine, list each
setup step the stand-in did that the real target will not. Those stay unverified.

## 7. Link it

When the repository has a `CONTEXT.md`, add a "Read when" entry for it, such as
"Seeing a change work in the running app: `.agents/skills/verify-<app>/SKILL.md`".

## Done

The skill directory, committed on a branch when the user asked for commits. The reply names the surface and harness,
the features mapped and the one proven live, where its proof is, the setup steps that stayed unverified, and the
features from `CONTEXT.md` that are not mapped yet. It points to `/maintain-verification-skill` for keeping the map
current as the app changes.
