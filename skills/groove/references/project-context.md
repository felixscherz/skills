# Project context and decisions

## The rule

Give working instructions, documentation navigation, and architectural decisions separate homes.

- `AGENTS.md`, or the repository's existing `CLAUDE.md`, holds instructions for working in the repository. Name the
  check command and tell agents to start with `CONTEXT.md` when looking for project context. Keep architectural
  explanations out of this file.
- `CONTEXT.md` briefly says what the project does, then provides a "Read when" list. Each entry names a task or
  decision and links to the relevant documentation. Link to `docs/glossary.md`, relevant ADRs, and module documentation
  where useful. Keep it an index, not a second copy of those documents or an exhaustive inventory of the code.
- `docs/adrs/` holds numbered architecture decision records. Each records its status, context, decision, and
  consequences. Explain why the approach was chosen and any relevant alternatives. Distinguish acceptance from
  implementation: "Accepted. Implementation is pending." is a valid status. Name unresolved choices explicitly rather
  than letting an agent mistake a candidate for an agreed decision.

Read the relevant ADR before choosing an approach. An accepted decision is a constraint even when it has not been
implemented. If the task conflicts with it, raise the conflict rather than silently replacing the decision.

When a decision is agreed, record it and add a task-based link in `CONTEXT.md`. Keep implementation status current.
When an agreed decision changes, add a new ADR and mark the earlier one as superseded, with links between them.
Preserve the earlier reasoning. Module READMEs may link to ADRs instead of duplicating their explanations.

Do not require an ADR for every implementation detail. Record choices that future work needs to respect or that a
later session would otherwise have to rediscover. Follow an existing repository's numbering and ADR format.

## Why

Agents read working instructions on every task, but most architectural context matters only for some tasks.
Putting everything in `AGENTS.md` makes every session load it all. Scattering decisions without an index makes
agents miss them and choose an approach again.

A task-based index makes the relevant decision easy to find. The ADR keeps the reasons and consequences together,
including what has been agreed but not yet built. The code remains the source for how the implementation works.

## Example

`AGENTS.md`:

```markdown
When looking for project context, domain concepts, or architectural decisions, start with [CONTEXT.md](CONTEXT.md).
It points to the relevant documentation.

Run `just check` before finishing a change. It runs all checks and the test suite.
```

`CONTEXT.md`:

```markdown
# Product catalog

Models Products, their procurement sources, and their identities in downstream systems.

## Read when

- Naming or changing a domain concept: [Glossary](docs/glossary.md).
- Changing deployment or temporary storage: [Deployment](docs/adrs/001-deployment.md).
- Working on persistence, restore, or compatibility: [Snapshots](docs/adrs/002-snapshots.md).
- Building screens or HTTP routes: [User interface](docs/adrs/003-user-interface.md).
```

Use `templates/adr.md` for a new record. The example project's `CONTEXT.md` links to a worked ADR.

## Codify it

Documentation content is reviewed by hand. No check currently enforces this convention in the example project.
File existence and local Markdown link targets can be checked mechanically. When adopting such a check, use an
existing Markdown link checker in the project's single check command. It should report the source file, broken
target, and how to repair the link. Do not treat passing link checks as proof that decisions are current or clear.

Do not add a documentation tool to a repository without being asked to apply Groove; propose it instead.

## Review by hand

- Does `AGENTS.md` name the check command and point to `CONTEXT.md`, without duplicating architectural explanations?
- Can someone starting with the task find the relevant decision through "Read when"?
- Does each ADR explain the choice, its reasons, and consequences, rather than just listing technologies?
- Are accepted decisions, unresolved choices, and implementation status distinguishable?
- Do changed decisions preserve the earlier reasoning through superseding records?
