# maintain-verification-skill

My version of `maintain-verification-skill` from [pstack](https://github.com/cursor/plugins/tree/main/pstack) by
[Lauren Tan (poteto)](https://github.com/poteto), a Cursor plugin under the MIT license. The idea is hers: a pass that
covers every feature of a verification skill from the source and live, sorts what it finds into doc drift, harness
gaps, and product bugs, and ships at most one PR of proven corrections. Her original:
[`pstack/skills/maintain-verification-skill`](https://github.com/cursor/plugins/tree/main/pstack/skills/maintain-verification-skill).

How this version differs:

- It audits the verify skill against the features in the repository's `CONTEXT.md`, which also becomes the check for
  features the map is missing, and fixes `CONTEXT.md` entries that turn out to be wrong.
- It looks for the skill in `.agents/skills/verify-*/`, where `create-verification-skill` puts it.
- It ships through the engineering skill's Opening a PR playbook.
