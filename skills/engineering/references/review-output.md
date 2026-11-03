# Review output

A review is read by the author, who has to act on it, and sometimes by an agent that addresses the feedback. Both need
to see quickly whether the reviewer understood the change, which parts got close scrutiny, and what must change before
merging. The categories are defined in `code-review.md`.

- Write the summary in your own words, not copied from the PR description, so the author can spot where the reviewer
  got the intent wrong. Mark it when the intent was inferred rather than stated.
- Omit a section only if it is empty, and say "None" for Blockers rather than dropping it.
- Number the findings, so a reply or an agent addressing them can refer to each one.
- Apply the `unslop` skill to the prose.

```markdown
## Summary of changes

<The intent and the change, in your own words. What problem this solves, what the change does to solve it, and how
the pieces fit. Written so the author can read it and say "yes, that is what I meant" or spot where the reviewer got
it wrong.>

## Review focus

<Which areas got deep scrutiny and which got a lighter pass, and why, based on blast radius and longevity.>

## Behavior changes

<Each existing test whose expectations changed: the old behavior, the new behavior, and whether the intent covers it.>

## Blockers

1. **<short title>** - `path:line`
   <What is wrong, why it matters, suggested fix.>

## Non-blockers

1. **<short title>** - `path:line`
   <What and why, suggested change.>

## Open questions

<Questions for the author where the answer could change the verdict.>
```
