<!-- Add this section to the repository's AGENTS.md (or CLAUDE.md). -->

## Groove

This repository follows Groove: load the `groove` skill before changing code.

- Check command: `make check`. Run it before reporting done; CI runs the same.
- When looking for project context, domain concepts, or architectural decisions, start with
  [CONTEXT.md](CONTEXT.md). Follow its "Read when" links to the glossary and relevant ADRs before choosing an approach.
  Use glossary terms for every domain concept.
- Module boundaries and layers: the import-linter contracts in `pyproject.toml`.
