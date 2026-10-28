## What changed and why

<!--
A few sentences. Lead with the motivation: the problem, goal, or request that
led to this change. Then say what was changed to address it. A reviewer who
only reads this section should know what the PR is trying to achieve and be
able to judge whether the diff achieves it. Call out decisions the reviewer
might disagree with and the alternatives considered. Link the issue or ticket
if one exists, but do not rely on the link alone.
-->

## Review guidance

<!--
Get the reviewer up to speed quickly and point them where to look.

Start with the shape of the change as the smallest visual that makes it clear:
pseudocode, a call tree, a file tree, or a Mermaid diagram, written as a `diff`
when the surrounding shape already exists (see "Review guidance" in
ship-changes.md). Keep only the steps, files, and boundaries that matter.

Then list where the reviewer's judgement is needed, most important first, each
with what to check there. Name tests whose expected behavior changed and any
check removed or weakened. Say what is mechanical and can be skimmed.

Add before/after evidence only when it shows something CI does not: changed
output, a screenshot, a manual check you ran. Never "run the tests".
-->

```diff
 entry point
   existing step
-  old behavior
+  new behavior
```

- `path/to/file` - what to check there
