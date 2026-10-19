---
id: {{NNNN-slug}}
created: {{YYYY-MM-DD}}
status: proposed           # proposed | approved | in-progress | pr-open | done | rejected
size: {{S | M | L}}
source: {{user | factory agent | worker in task NNNN-slug}}
member: {{member name}}
branch: {{<prefix><id>, once work starts}}
pr: {{PR link, once opened}}
plan: {{plans/<slug>.md, when the item is worked through a plan}}
---
# {{title}}

## Why

{{What is wrong or missing, and why fixing it is worth a PR.}}

## Evidence

- {{file:line references, commands and their output, or what the user said}}

## Done means

{{What the change achieves and how it is verified. What must not change.}}

## Risk

{{What could break, and who or what depends on the code it touches.}}

## Notes

{{Findings while working on it, such as why it stopped. Empty until there are any.}}

## Decision

{{Why the user rejected it, or anything they decided about it. Empty until there is one.}}
