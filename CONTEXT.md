# Skills

My Agent Skills,
written to work across Claude Code, Codex, and opencode.
Each skill is a directory with a `SKILL.md` under `skills/`,
installed globally with `npx skills` (see `README.md`).
This repository is the source of truth;
the installed copies are overwritten on every update.

Most skills here are tools.
Three carry what I think and care about,
and they matter more than the rest:
`skill-design`, `engineering`, and `groove`.
When a change touches one of them,
read its section below first,
and keep the change in line with the idea behind it.

## Read when

- Changing how the `engineering` skill is organized,
  or adding a playbook or reference to it:
  `docs/engineering-skill.md`
- Designing a skill,
  or changing how skills depend on each other or share material:
  the `skill-design` skill
  (`skills/skill-design/SKILL.md`)
- Authoring or changing any skill:
  the `author-skill` skill
  (`skills/author-skill/SKILL.md`)
- Picking up an unfinished idea for this repository:
  `docs/ideas/`

## The core skills

All three answer one question from different sides:
how do I get good work out of agents
that do most of the work
while I am not looking?
`engineering` shapes the agent:
it tells the agent how I want the work done.
`groove` shapes the codebase,
so the right decision is the easy one to make there.
`skill-design` is how I build skills like these,
so that they hold up as they grow and get shared.

### skill-design: skills are a kind of software

`skills/skill-design/`

A skill is more than a markdown file.
It is a kind of software,
and the ideas I use to design code apply to it:
interfaces and implementations,
contracts,
dependencies,
and one home for each fact.
This is where I write down how I want to think about skills,
and how I want agents to think about them,
once they stop being single files:
skills that come as a package,
reference each other,
depend on each other,
or run for people and machines
where the tools and paths differ.

- A skill is designed around the situation that should load it.
  Its description is that situation written down,
  with its boundaries against neighbouring skills
  (`references/triggers.md`).
- A skill says what it needs in domain verbs,
  such as "open a merge request",
  and a binding outside the skill says how that is done here
  (`references/interfaces.md`).
- A skill states what it assumes,
  who decides what,
  and when it is done
  (`references/contracts.md`).
- Guidance lives in one skill or reference,
  and every other skill that needs it points there
  instead of keeping a copy
  (`references/shared-material.md`).
- A step with one correct answer is a script,
  with an interface an agent can use without reading the source
  (`references/scripts.md`).

`author-skill` covers the mechanics:
where a skill lives and how its file is shaped.
`skill-design` covers what a skill says
and what it may assume.
New ideas about skills in general go here
as a new reference.

### engineering: quality when I am not looking

`skills/engineering/`

My distilled taste in software engineering,
in the spirit of Lauren Tan's pstack.
It is the main lever I have
on the quality of what agents build for me.
When an agent runs into a situation I have already thought through,
it follows a playbook I have approved
instead of improvising.

- **Playbooks** (`playbooks/`) say what to do
  for one kind of task:
  who decides what,
  the steps,
  and what done looks like.
- **References** (`references/`) say what good looks like.
  A playbook names them at the step where they apply,
  so the agent finds my principles
  in the course of the work
  rather than having to know them up front.
- **Tenets** at the top of `SKILL.md`
  carry the principles into every session,
  because agents read the playbook
  and often stop there.
- **Done** is explicit and checkable:
  a PR with green CI
  that a human reviewer can understand
  and should find no blocker in.

Unlike pstack,
it keeps me in the loop for design
and keeps the agent inside the scope it was given.
It is a living draft:
agents point out where a rule gets in the way,
and changes go through `reflect-on-engineering`.
`docs/engineering-skill.md` explains its structure
and the history behind it.

### groove: a codebase where the right thing is the easy thing

`skills/groove/`

Experimental.
A way to design Python applications
that AI agents build and maintain.
It starts from a question:
if agents do 95% of the development work,
how do I set up the codebase
so they make the right decisions on their own?
The answer it tries is to put the right decisions
into the structure of the codebase:
one name per concept,
one obvious home for every piece of code,
and every dependency on the outside world
visible in a signature.
As with Lauren Tan's Dune,
the shortcut should be the only correct path.

Groove stands on its own.
A project can adopt it
without the `engineering` skill,
and an agent working there
gets everything Groove asks for from Groove alone.
So Groove does not depend on `engineering`,
and some guidance appears in both:
`engineering` says what good looks like in any codebase,
and Groove restates the parts it builds on
in the stricter form it checks.
A Groove reference may point to `engineering`
for more depth,
but only as optional reading.

Agents take feedback differently from people,
and Groove is built around that:

- **A rule in CI holds,
  a rule in prose drifts.**
  Each agent session reads prose a little differently,
  so every mechanical rule becomes a check
  in one command.
- **Error messages point to the fix.**
  An agent acts on a message right away,
  so every check says how to fix what it found,
  not only what is wrong.
- **Strictness is cheap.**
  A rule that would wear a human down,
  firing again and again,
  costs an agent nothing.
  Groove can be stricter than a team of people would put up with,
  and uses that.
- **Rules graduate.**
  A rule starts as a review question
  and moves into a check
  once it has proved useful
  and a tool can express it.

Its principles are still being tested.
Agents report where a rule was unclear,
cost more than it gave,
or could be checked but is not,
and that feedback shapes the next version.
