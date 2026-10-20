# Context

A `CONTEXT.md` at the repository root is the entry point to what an agent
needs to know about a system: what it does, in the domain's words, and where
to read further for a given task. It lets an agent go from "the user means X"
to the right code or document without searching the whole codebase. It is
committed and shared with the team, and `AGENTS.md` points to it.

- Read the nearest `CONTEXT.md` before exploring the code, and follow only the
  links whose trigger matches the task. A missing file never blocks a task:
  explore the code as usual, and do not offer to write one or ask about it.
  The user asks for one when they want it.
- Keep it short enough to read in one go. Open with a few sentences on what
  the system does and for whom, then a "Read when" list that states the
  trigger before each link, then the features.
- Put the documents it links to in a `docs/` folder beside it, such as the
  glossary at `docs/glossary.md`. A glossary entry holds the term, a short
  definition, and the synonyms to avoid.
- List features as someone outside the code observes them: an endpoint, a
  command, a screen, a scheduled job, an emitted event. Group them by domain
  area, and point to modules, directories, and key types, not lines or
  functions that churn. When the list no longer reads in one go, move it to
  `docs/feature_map.md` and link it from "Read when".
- Give each bounded context with its own language its own `CONTEXT.md` at the
  root of its directory, with its own `docs/` and glossary beside it. The
  parent `CONTEXT.md` lists its bounded contexts, how they relate, and links
  to each one's `CONTEXT.md` (see `domain-driven-design.md`).
- Build it together. Propose the summary, features, and terms, and let the
  user correct them. It is only useful if both sides use the same names.
- Keep it current. When a task adds, moves, renames, or removes a feature, a
  term, or a document it links to, update it in the same change. When it
  points to the wrong place, fix it.

```markdown
# Payments

Takes payments from customers for their orders and refunds them, and settles
with the payment provider every night.

## Read when

- Naming a domain concept: `docs/glossary.md`
- Working on payouts to merchants: `src/acme/payouts/CONTEXT.md`
- Changing how settlement runs: `docs/settlement.md`

## Features

### Refunds

- **Refund a payment** - `POST /payments/{id}/refunds`. Domain in
  `payments/domain/refund.py` (`Refund`), wiring in `payments/api/`.

### Settlement

- **Nightly settlement** - scheduled job, `payments/jobs/settlement.py`.
```
