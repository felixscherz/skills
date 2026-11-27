# Triggers: what deserves to be a skill, and what its description is for

A skill is a way to influence
how an agent behaves in a particular situation:
to nudge it in the right direction
at the moment it would otherwise go wrong or go generic.
The situation is the trigger.
Design a skill around its trigger,
not around its topic.

## One skill per trigger

A separate skill is worth it
when there is a distinct situation
in which an agent should load it.
Guidance that only matters once another skill is already loaded,
or that always comes up together with it,
is not a separate skill.
It is a reference inside that skill's package.

This gives two shapes that work well together:

- **A package behind a router.** One skill whose `SKILL.md` routes to `references/`
  and `playbooks/` files,
  each with a line saying when to read it.
  Many topics, one trigger, one description in context.
  `engineering` is this shape:
  feature work, debugging, refactoring,
  and PR review all start from "software engineering work in a codebase",
  and the router picks the playbook.
- **Several skills on one concept.** One concept seen from different situations,
  each with its own trigger,
  all pointing to the same reference material.
  A setup skill and a lookup skill
  for the same workspace map;
  a skill that creates a verification skill and one that maintains it.
  Each skill is small
  and holds what is specific to its situation,
  and the shared concept lives
  once (see `shared-material.md`).

Signs a split is wrong:

- Two skills always load together. Merge them,
  or make one a reference of the other.
- A reference inside a package is needed
  in a situation where the package would never be loaded.
  Give that situation its own skill that points to the reference.
- A router lists files without saying when to read them.
  The agent then reads all of them or none.

Keep references one level deep,
so a router never routes to another router,
and keep a `SKILL.md` short enough to read in one pass.

## The description is the trigger, written down

Every installed skill's description
sits in the agent's context in every session;
the body loads only when the agent decides the description matches.
So the description has one job:
make the agent load the skill in the situations it was written for,
and not in the ones it was not.
It is a routing rule,
not a summary of the contents.

A good description has just enough to route:

- **The situations**,
  named the way they appear in a task:
  what the user is doing,
  what they say ("make a verify skill",
  "hand this off"),
  what the agent is about to do
  ("before calling the change done").
- **The boundaries**:
  the nearby situations where it should not load,
  and which skill covers them instead.
  "Not for writing tests,
  and not for a repository
  that already has a verify-* skill
  (use maintain-verification-skill)."

What to leave out:
what the skill contains, how it works,
and why it exists.
None of that helps the agent decide whether to load it,
and every word is paid for in every session.

## Read descriptions as one routing table

The descriptions of all installed skills together form one routing table,
and a description is only as good as its neighbours let it be.
When writing or changing one,
read the descriptions of the skills next to it:

- If a request could plausibly route to two skills,
  one of them says "not for X (use Y)",
  and ideally both do.
- When several skills share a concept (above),
  each description names its own situation, not the concept.
  Three descriptions that all say "workspace maps" compete;
  "create or update the map" and "find a repository
  whose location is unknown" do not.
- A quick check:
  given only the descriptions and a handful of realistic requests,
  which skill would each request load?
  Any request that lands on two skills,
  or on none it should,
  is a description to fix.
