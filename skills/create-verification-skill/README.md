# create-verification-skill

My version of `create-verification-skill` from [pstack](https://github.com/cursor/plugins/tree/main/pstack) by
[Lauren Tan (poteto)](https://github.com/poteto), a Cursor plugin under the MIT license. The idea is hers: a skill
that writes a project-local skill to drive the real app as a user would and prove behavior with evidence, plus a map of
how to verify each feature. Her original:
[`pstack/skills/create-verification-skill`](https://github.com/cursor/plugins/tree/main/pstack/skills/create-verification-skill).
Its companion, `maintain-verification-skill`, has its own README.

How this version differs:

- It starts from the repository's `CONTEXT.md` (see `skills/engineering/references/context.md`) for what the app is
  and which features it has, and reads the code only for what `CONTEXT.md` does not say. The generated skill names
  features as `CONTEXT.md` does and does not repeat what it says about them.
- The generated skill always goes to `.agents/skills/verify-<app>/`, so every harness finds it, and it is
  auto-invokable so agents load it on their own when they need to see a change working.
- It links the generated skill from `CONTEXT.md`.
