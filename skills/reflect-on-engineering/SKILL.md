---
name: reflect-on-engineering
description: User-invoked review of how the engineering skill served a piece of work. Use when the user asks to reflect on engineering, review the engineering skill based on this work, or decide what it should learn from an implementation. Not for applying engineering rules during a task.
disable-model-invocation: true
metadata:
  opencode/autoinvoke: false
---

# Reflect on engineering

The `engineering` skill
should describe how the user works today,
not how they worked when a rule was written.
This skill turns a finished piece of work
into evidence about which rules helped,
which got in the way,
and what is missing.

## Scope

Reflect on the most recent completed piece of work
unless the user names another scope,
such as a branch, a PR, a transcript,
or a set of past sessions.
Do not include the subsequent discussion
about editing the skill unless the user asks.
If several completed tasks could be meant,
clarify the scope.
State the scope you used at the top of your reply.

## Gather evidence

Read `../engineering/SKILL.md`, the playbook the agent named in its first message,
and the references that affected decisions in the work.
Read other playbooks and references
when needed to verify a suspected conflict,
a wrong route, or a missing rule.
Then walk through the work and note:

- **Rules applied.** Which rules were read,
  and which decision each one changed.
  A rule that was read but changed nothing is a signal too.
  So is a reference a playbook step named that was never opened:
  agents tend to stop at the playbook,
  and the principle then never reaches the work.
- **User corrections.** Every time the user redirected,
  rejected, or corrected the work.
  These are the strongest evidence.
  Ask whether a rule would have prevented the correction,
  or whether a rule caused it.
- **Stated preferences.** Anything the user said about how they want code written,
  tested, reviewed, or discussed that no rule captures.
- **Routing.** Check each layer that decides what gets read.
  The skill itself: did it load,
  or did the agent work without it (its description,
  and the global `AGENTS.md` line that points to it).
  The playbook:
  was the one the agent named the right one,
  and if the user redirected it,
  which rule under "When more than one seems to fit" in `SKILL.md` would have sent it there.
  The references:
  one that should have been read and was not,
  or one read without applying,
  points at its "when" text in the index
  or at the step that should name it.
- **Skipped steps.** Steps the agent said it skipped, and why.
  A step skipped for the same reason more than once
  does not fit the work it is written for.
- **Rules that misfired.** A rule that was ambiguous,
  contradicted another rule or the codebase,
  or pushed toward a worse result.
  This is friction with the rules,
  not the code friction the agent lists
  under "Friction" in its reply.
  Code friction goes to the follow-up tracker;
  it is evidence here only when the skill should have caught it
  and did not.
- **Flags.** Problems with a rule
  that the agent already raised during the work,
  as the engineering skill asks it to.
  Treat each as a finding to verify, not as settled.

Quote or point to the concrete moment for each note.
Do not report a finding you cannot tie to something
that happened in the scope.

## Judge each finding

- **General or local.** The engineering rules apply across codebases.
  A lesson tied to one project belongs in that project's `AGENTS.md` or a local skill.
  Say where it belongs instead.
  A language- or framework-specific lesson
  that carries across projects belongs in `references/<language>/`.
- **Pattern or one-off.** One session is weak evidence for a new rule.
  An explicit user preference or a repeated correction is strong evidence.
  Say how strong the evidence is.
- **Sharpen, remove, or add.** Prefer sharpening or removing a rule over adding one.
  A rule that never changes a decision is a candidate for removal.
- **Right skill.**
  Some findings belong in another skill,
  such as `groove`,
  or in the global `AGENTS.md`. Name the target.

## Report

For a review-only request, reply with:

1. **Scope** used.
2. **What helped.** Rules
   that changed a decision for the better,
   one line each.
3. **Proposed changes.** For each:
   the target file,
   the change (add, update, remove, or retrigger),
   the proposed wording or a precise summary of it,
   the evidence from the scope,
   and the evidence strength.
4. **Out of scope**,
   if relevant.
   Findings that belong somewhere other than the engineering skill,
   with the suggested destination.

"No changes needed"
is a valid result.
Do not invent changes to fill the report.
Keep the report proportionate to the evidence.
When the user has asked for an update,
apply the requested changes and report what changed
and why instead of stopping at a proposal.

## Apply

Edit when the user explicitly asks for an update
or approves specific proposed changes.
For ambiguous requests
such as "review this, it may need updates",
propose changes and ask before editing.

- The skill lives in `~/workspaces/personal/skills/skills/engineering/`.
  Remind the user to commit changes there.
- `../engineering/SKILL.md` opens with the tenets
  under "What I care about":
  one line each, at most fifteen,
  each naming the reference that holds the detail.
  When a reference changes what it stands for,
  update its tenet.
  A new tenet replaces a weaker one.
- Steps that every code-changing playbook
  shares live under "Changing code"
  in `../engineering/SKILL.md`,
  and what to do about friction
  under "When code resists",
  not in the playbooks.
- When a change alters
  how the skill is structured or routes work,
  such as a new playbook,
  a moved section,
  or a rule about what every reply holds,
  record the reason in `docs/engineering-skill.md`.
- One rule per file in `references/`:
  an H1 title,
  a short framing paragraph,
  and a few bullets.
  No frontmatter:
  when a rule applies is stated once,
  in its index entry,
  since references are only reached through an index.
- A rule with supporting files,
  such as a script,
  gets its own folder named after the rule,
  holding `<rule>.md` and those files.
- One workflow per file in `playbooks/`:
  an H1 title,
  a short framing paragraph,
  then `## Applies when`,
  `## Who decides`, `## Steps`,
  and `## Done`.
  The first step states what success looks like for the task,
  and a later step checks the result against it.
  Done opens with the end state
  as conditions an agent can check,
  then names each exit that is not success,
  such as blocked on the user or a "no",
  and what the reply says for it,
  then what the final reply holds
  and which playbook usually comes next.
  A playbook that changes product code ends in the shared end state
  under "Changing code" in `../engineering/SKILL.md` instead of restating it.
  Each step names the references it needs at the point it needs them.
  A playbook holds steps, not principles:
  a rule that applies beyond one playbook belongs in `references/`.
  The reasoning behind this split
  is in `docs/engineering-skill.md` at the root of the skills repo.
- Language- or framework-specific rules
  go in `references/<language>/`.
  They may be longer and include examples,
  but must not restate the general rules they build on.
  Keep their examples consistent with the general rules,
  since an agent copies the example
  before it reads the prose.
- Each `references/<language>/` folder has an `INDEX.md`: an H1 title,
  a short framing paragraph,
  and one bullet per reference with its name,
  its path relative to the folder,
  and when it applies,
  in the same format as the index in `../engineering/SKILL.md`.
- `../engineering/SKILL.md` links to a language folder's `INDEX.md` with one bullet that says when to open it,
  never to the individual references inside.
  This keeps the top-level index short and language-neutral.
- Keep the indexes in sync
  when adding, renaming, or removing a file:
  the folder's `INDEX.md` for language references,
  `../engineering/SKILL.md` for everything else,
  and every playbook that links to the file.
  A new or renamed playbook also needs its place
  under "When more than one seems to fit"
  when its situation borders another playbook's.
