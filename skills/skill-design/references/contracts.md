# Contracts: what a skill assumes, who decides, and when it is done

A skill sets up an agent
to act on its own for a while.
Three things keep that autonomy useful:
knowing what it may assume,
knowing which decisions are its to make,
and knowing when to stop.

## Assumptions, and what to do when they fail

Write the skill for the normal case:
the tools are installed, the files exist,
the binding is in place.
Do not open with a checklist
the agent works through before doing anything;
in the normal case it only costs time.

Instead,
give the skill a short section
for when an assumption turns out not to hold,
and say what the agent does then.
For each dependency that can be missing:

- **What it is** -
  the tool, file, MCP server, or binding.
- **How it shows** - the error, the missing file,
  the script's non-zero exit.
- **What to do** -
  ask the user, fall back to something named,
  proceed without it, or stop.
  `interfaces.md` covers the choice for bindings.

A check script
can help the agent diagnose the failure
once it has happened (see `scripts.md`).

## Who decides

Say which decisions belong to the user
and which belong to the agent. Without this,
an agent either asks about everything
or decides things it should not.

- **The user decides**
  what only they can know or should own:
  which of several valid targets to work on,
  anything involving credentials, cost, accounts, or shared state,
  and trade-offs
  that depend on their priorities.
- **The agent decides**
  everything else in the skill's scope:
  approach, tools, order, file layout, naming.
  Say so explicitly,
  so it does not stop to ask.
- **Ask only what the environment cannot answer.** If the repository, the binding,
  or a command can settle it,
  the agent looks instead of asking.

A short "Who decides" section near the top works well.
`create-verification-skill` has one:
    the user picks the surface
when several are equally primary and anything needing credentials;
    the agent picks the harness, the helpers,
and which features to map first.

## Done

Say when the work is finished
and what the agent hands back. Without it,
the agent stops when it feels finished,
and that point moves from run to run:
sometimes before the result is verified,
sometimes after a round of unrequested polish.

A "Done" section at the end states:

- **The result** - the files, commits,
  or state that exist when it is finished,
  and where.
- **The evidence** -
  what has to have been run or observed,
  such as the generated skill
  followed end to end once.
- **The reply** -
  what the final message names:
  what was done, where it is,
  what stayed unverified,
  what comes next.

When the skill has natural stopping points
before the end,
such as waiting for the user to approve a proposal,
name those too.
