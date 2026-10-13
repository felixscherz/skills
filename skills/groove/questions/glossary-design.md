# Open question: glossary design

Not loaded by the skill. Notes for deciding how the glossary should evolve.

## Current state

One global `GLOSSARY.md` in Markdown, with a loose entry format (definition,
code forms, banned synonyms, status). An awk script turns the Banned lines
into a codespell dictionary, so banned synonyms are checked in CI. Everything
else (definitions, code forms, statuses) is read by agents, not checked.

## Why a structured format

The awk script depends on the exact `- **Banned:**` line format, which is
fragile. A TOML or YAML glossary would be parsed reliably and could feed more
checks (code forms, statuses) and generated docs.

## The blocker: one term, several meanings

In a growing domain, the same word legitimately means different things in
different modules (DDD bounded contexts). "Order" in checkout is a basket
being paid for; in fulfilment it is a set of parcels. A single global entry
with one definition and a global banned list cannot express that:

- A banned synonym in one context may be the canonical term in another.
- Each module needs to declare which meaning it uses.
- Translation between contexts needs a home. For reads it now has one: the
  reading module's adapter in `infrastructure/` (see
  `references/architecture-boundaries.md`). Whether the glossary should also
  record the mapping is open.

## Questions to decide

1. Global glossary with per-context sections, or one glossary per module
   plus a shared core?
2. How does a module declare which context or meaning it uses? In its
   README, in the glossary entry, or in a config file a check can read?
3. Are banned synonyms global or per context?
4. How are code forms (`invoice_id`, `InvoiceIssued`) derived: listed by
   hand, or generated from the term with casing rules?
5. Is the `proposed` / `accepted` status enough as a review workflow, or
   does it need an owner and date?
6. What file format: TOML (next to `pyproject.toml`), YAML, or Markdown with
   front-matter so it stays readable on GitHub?
7. Per-context banned synonyms need per-path codespell runs (one dictionary
   per module). Is that acceptable, or does it call for a different tool?
8. Do domain verbs (issue, cancel) live in the same list as nouns, or get
   their own section?
