# Spec

Design is the process of working out how to build something; a spec is the document that may come out of it. A spec
records a design the user agreed to and the decisions behind it, so that someone who was not in the conversation can
build it and later understand why it looks the way it does. It is the hand-off between designing and implementing. It
says what to build and why, not in which steps.

- Put it where the project already keeps design documents. When there is no obvious place, use `docs/specs/<slug>.md`
  in the directory you are working in: the repository root, or the root of the bounded context that has its own
  `CONTEXT.md`. When neither fits, ask the user. A spec is committed with the project, unlike plans and notes.
- Start with a title, a status, and the date. The status is `Draft` while the user reviews it, `Accepted` once they
  approve it, and `Implemented` once the change that builds it merges.
- Write these sections in order, and drop one only when it has nothing to say:
  - **Background.** The problem, who has it, and what exists today. Enough for a reader who never saw the
    conversation.
  - **Reasoning.** The forces that shaped the design: requirements, constraints, and what matters most when they
    conflict.
  - **Alternatives considered.** Each serious option that lost, and why. This is the part that stops a later reader
    from reopening a settled decision.
  - **Design.** The solution: the domain concepts and their names, where each responsibility lives, how dependencies
    flow, the data shapes and interfaces, and how it is verified.
  - **Open questions.** What is not settled, and what the implementer should do until it is.
- Mark what must be built exactly as written with `NORMATIVE`. A heading ending in `(NORMATIVE)` covers its whole
  section; a bullet or paragraph starting with `NORMATIVE.` covers only itself. Everything unmarked is guidance the
  implementer may adapt to what they find in the code. Reserve the marker for what really must hold, such as an
  external contract, a data format, a domain rule, or a decision the user made deliberately. When everything is
  normative, nothing stands out.
- Write each normative statement so it can be checked: observable behavior or a concrete shape, not a quality such as
  "clean" or "fast".
- Use the domain's names, the same ones as the glossary and the code (see `domain-driven-design.md`). Show shapes as
  code, types, or diagrams rather than prose, and keep implementation detail out unless it is normative.
- When the repository has a `CONTEXT.md`, link the spec from it while its work is ongoing (see `context.md`).
- A spec changes only with the user's approval. When implementation shows that it is wrong, update the spec, and
  record the change and its reason in it, before building differently.

```markdown
# Refund partial payments

Status: Accepted · 2026-11-03

## Background

Customers can only be refunded in full ...

## Reasoning

...

## Alternatives considered

- **Negative payments instead of refunds.** Rejected because ...

## Design

### Refund amount (NORMATIVE)

A `Refund` holds an `amount` no larger than the payment's remaining refundable amount ...

### Where it lives

...

## Open questions

- ...
```
