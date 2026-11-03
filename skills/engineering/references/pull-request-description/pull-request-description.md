# Pull request description

The description is read by humans: the reviewer, and later anyone digging
through history to find out why the code looks the way it does. Write for a
person who has not seen the work in progress and wants to understand the
change quickly. Apply the `unslop` skill to it.

## Follow the project's conventions first

Before writing, find out how the project describes PRs:

- A repository template (`.github/pull_request_template.md`,
  `.github/PULL_REQUEST_TEMPLATE/`, `.gitlab/merge_request_templates/`, or
  similar). If one exists, fill it in.
- Recent merged PRs (`gh pr list --state merged --limit 10`, then
  `gh pr view <n>`). Their length, structure, and tone are the convention even
  when no template is checked in.
- Contribution guides (`CONTRIBUTING.md`, `AGENTS.md`).

Use `pull_request_template.md` next to this file only when the project has no
convention of its own. Do not force it onto a project that does things
differently, and do not bolt its sections onto a repository template. Within
the project's format, still cover what the reader needs (see below), worded
the way that format expects.

Scale the description to the change. A one-line fix needs a sentence or two,
not three headed sections.

## What the reader needs

The reader wants to verify two things: that the change achieves its goal, and
that it does so the way they would want.

- **Lead with motivation.** The problem, goal, or request that led to the
  change. This is the part that matters most and gets lost most often. If you
  do not know why the change was made, ask the user rather than invent a
  reason.
- **Surface decisions.** Name the choices the reviewer might disagree with:
  a design picked over an alternative, a trade-off accepted, a scope cut, a
  new dependency, a convention broken. State the alternative and why it lost.
  These are where "do I like this" gets decided, so do not bury them in the
  diff.
- **Call out behavior changes.** When existing tests had to change, say which
  ones and what behavior changed. A reviewer will treat a changed test as a
  possible regression until told otherwise.
- **Flag uncertainty.** Say where you are unsure or want the reviewer's
  judgement.
- **Show the shape, then point where to look.** Give a high-level picture of
  what changed before the reviewer opens the diff, then direct their attention
  (see "Review guidance" below).
- **Call out weakened checks.** Any test or CI that was removed or weakened,
  with the reason.
- Keep it short and plain. No filler, no restating the diff line by line, no
  agent workflow details the reader does not care about. Do not tell the
  reader that tests pass or how to run them; CI shows that.

## Review guidance

The goal is to get a reviewer up to speed in a minute and spend their attention
where it is needed. It has three parts, scaled to the change.

**The shape of the change.** Pick the smallest view that makes the key point
clear, and keep only the calls, files, and boundaries the reviewer needs. One
visual is usually enough; never use more than a few.

- Logic or an algorithm as pseudocode:

  ```text
  on(save)
    if content is unchanged
      return cached result
    write new content
  ```

- Runtime control flow as a call tree:

  ```text
  submitForm
    createSession
      persistPrompt
      launchAgent
    navigateToSession
  ```

- File responsibility or a broad refactor as a shallow file tree:

  ```text
  src/
  ├── commands/       # parses user actions
  ├── sessions/       # owns session state
  └── transport/      # sends API requests
  ```

- Interaction or data flow between components as a Mermaid diagram (GitHub and
  GitLab render it).

- When the surrounding shape already exists and the point is what changed,
  write any of the above as a `diff`: unchanged lines as context, `-` for what
  went away, `+` for what replaced it. This is the most useful form for most
  changes to existing code:

  ```diff
   Procedure.run
  -  spawn a fresh interpreter, import dependencies from scratch
  +  fork from a server that preloaded the dependencies
     load test modules
  -    per repo, sequential: import package, read config
  +    all repos in parallel threads: read config without importing
  ```

Use the domain's names, not invented ones, and put each visual next to the one
or two sentences it supports.

**Where to look.** The places that need the reviewer's judgement, most
important first, each with a file path and what to check there: a decision
that could have gone another way, a tricky edge case, a test whose expected
behavior changed, anything you are unsure about. Then say what is
mechanical (renames, moves, generated code) so it can be skimmed.

**Evidence, only when CI cannot show it.** A before and after that the
reviewer could not get from the checks: changed console output, a screenshot
of a visual change, a timing, a manual check against a real system. Leave it
out otherwise.

The visuals are adapted from Dex Horthy's `show-me` skill
(https://github.com/humanlayer/skills, MIT).
