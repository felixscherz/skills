# Skills

My Agent Skills, written to work across Claude Code, Codex, and opencode. Each skill is a directory with a `SKILL.md`
under `skills/`, installed globally with `npx skills` (see `README.md`). This repository is the source of truth; the
installed copies are overwritten on every update.

## Read when

- Changing how the `engineering` skill is organized, or adding a playbook or reference to it:
  `docs/engineering-skill.md`
- Authoring or changing any skill: the `author-skill` skill (`skills/author-skill/SKILL.md`)
- Picking up an unfinished idea for this repository: `docs/ideas/`

## Skills

### Engineering

- **engineering** - how I write software: principles and best practices in `references/`, and workflows that route
  to them in `playbooks/`. `skills/engineering/`
- **reflect-on-engineering** - turns a finished piece of work into proposed changes to `engineering`.
  `skills/reflect-on-engineering/`
- **groove** - a convention for Python codebases built for agentic coding. `skills/groove/`
- **pair-program** - a session with the user as navigator. `skills/pair-program/`
- **create-verification-skill** and **maintain-verification-skill** - generate and maintain a project-local
  `verify-<app>` skill that drives the real app like a user and captures proof, built on the repository's
  `CONTEXT.md`. Based on Lauren Tan's pstack; credit in each skill's `README.md`. `skills/create-verification-skill/`,
  `skills/maintain-verification-skill/`

### Working with agents

- **benchmarking-the-harness** and **create-benchmark** - blinded experiments on how a skill or instruction change
  affects agent behavior. `skills/benchmarking-the-harness/`, `skills/create-benchmark/`
- **author-skill** - how to write a skill that works across harnesses. `skills/author-skill/`

### Communication

- **unslop** - cuts AI tells from prose. `skills/unslop/`
- **html-communication** - self-contained HTML write-ups. `skills/html-communication/`
- **show-me** - walks the user through code in a Neovim pane. `skills/show-me/`
