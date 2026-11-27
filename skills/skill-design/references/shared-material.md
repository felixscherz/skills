# Shared material: one home for each piece of guidance

Design a skill as part of the set it is installed
with, not on its own.
Before writing one,
look at the skills next to it:
the ones whose triggers sit close to its own
(see `triggers.md`),
and the ones that already explain something it needs.
For a skills repository,
that means reading at least the descriptions of every skill in it.

## Every fact has one home

Each piece of guidance lives in exactly one place,
and everything else that needs it points there.
Copies drift: one gets updated,
the other keeps teaching the old way,
and the agent cannot tell which is right.

- **A repository fact**
  (what the app is,
  where its features live) belongs in the repository,
  such as its `CONTEXT.md`. A skill that needs it reads it
  and does not restate it.
  The verify skills written by `create-verification-skill` name features as `CONTEXT.md` does and hold only how to run, drive,
  and prove them.
- **Guidance
  one skill owns** stays in that skill.
  Another skill that needs it names the skill
  and says when to load it,
  instead of copying the passage.
- **A concept several skills share** lives
  in one reference that each of them points to.
  This is what lets several small skills,
  each with its own trigger,
  approach the same concept from different situations.

## Where shared references live

Skills are installed flat and copied one by one,
so a skill cannot assume another skill's files
are next to it unless both are installed.
The options:

- **One skill owns the reference,
  the others point to it by path**,
  such as `../engineering/references/context.md`. Simple,
  and it works while both skills are installed together,
  as everything from one repository is.
  The pointing skill should say what to do
  when the path is missing.
- **The others
  load the owning skill by name**
  and follow its router to the reference.
  Works across harnesses and does not depend on file layout,
  but costs a load.
- **The material lives outside skills**,
  in the repository or a document both can read.
  Right for repository facts.

Whichever you pick, keep the chain shallow.
A skill that loads a skill that loads a third one is fragile;
if that chain appears,
the material probably belongs in one place closer to where it is used.

## When changing shared material

A change to shared material changes the behaviour
of every skill that points to it.
Before changing it, find those skills
(search the repository for the path or the skill name)
and check that the change still fits each of their situations.
