# Open question: glossary design

Not loaded by the skill. Notes for deciding how the glossary should evolve.

## Current state

One global `docs/glossary.md` in Markdown, linked from `CONTEXT.md`, with a
loose entry format (definition, code forms, banned synonyms, status). It is
read by agents and reviewed by hand. No tool checks it: an earlier codespell
check on the Banned lines was removed until the format is settled.

## Why a structured format

A check needs a format it can parse reliably. A TOML or YAML glossary could
feed checks (banned synonyms, code forms, statuses) and generated docs, while
a Markdown line format such as `- **Banned:**` is fragile to parse.

## One term, several meanings

In a growing domain, the same word legitimately means different things in
different modules (DDD bounded contexts). "Order" in checkout is a basket
being paid for; in fulfilment it is a set of parcels. A single global entry
with one definition and a global banned list cannot express that. The
`engineering` skill's `references/context.md` answers it for documentation:
each bounded context with its own language gets its own `CONTEXT.md` and
glossary. Within one context, the open points remain:

- A banned synonym in one context may be the canonical term in another.
- Each module needs to declare which meaning it uses.
- Translation between contexts needs a home. For reads it now has one: the
  reading module's adapter in `infrastructure/` (see
  `references/architecture-boundaries.md`). Whether the glossary should also
  record the mapping is open.

## Questions to decide

1. Where does the line run between a module of one context and a context
   of its own, with its own glossary?
2. How does a module declare which context or meaning it uses? In its
   README, in the glossary entry, or in a config file a check can read?
3. Are banned synonyms global or per context?
4. How are code forms (`invoice_id`, `InvoiceIssued`) derived: listed by
   hand, or generated from the term with casing rules?
5. Is the `proposed` / `accepted` status enough as a review workflow, or
   does it need an owner and date?
6. What file format: TOML (next to `pyproject.toml`), YAML, or Markdown with
   front-matter so it stays readable on GitHub?
7. When the glossary is checked again, which tool reads it, and does it run
   per bounded context?
8. Do domain verbs (issue, cancel) live in the same list as nouns, or get
   their own section?
