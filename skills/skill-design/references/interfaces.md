# Interfaces: skills that depend on things that vary

A skill written for yourself
can name the tool it uses:
`gh pr create`, the Jira MCP,
`~/workspaces/foo`.
Once the skill is shared with a team or an organization,
those names stop being true for everyone.
One repository uses GitLab, another GitHub.
One developer keeps their checkouts in `~/src`,
another in `~/work`.
One team tracks issues in Jira, another in Linear.

The fix is the one code uses:
write the skill against an interface
and supply the implementation at run time.
The skill says what it needs in domain terms
("open a merge request for this branch",
"find the repository that holds the billing service").
Something outside the skill, a binding,
says how that is done here.

Not every skill needs this.
Inside a team where everyone uses GitLab,
write against GitLab.
Introduce an interface
when a second implementation shows up,
or when the skill is about to cross the boundary
where the assumption stops holding.

## Write the interface in domain verbs

The skill body names actions and things,
not tools:

- "Publish the plan to the issue tracker",
  not "run `gh issue create`".
- "Look up where the `payments` repository is checked out",
  not "`cd ~/workspaces/payments`".
- "Verify the change in the running app",
  not a list of Playwright commands.

A binding can then map each verb to a concrete action.
The verbs are the interface,
so keep them stable
and use the same wording
in every skill that relies on them.

## Know which kind of dependency it is

The kind of dependency decides where its binding lives
and who owns it.

| Kind | Examples | Varies per | Binding usually lives | Committed? |
|---|---|---|---|---|
| **Capability** | git forge, issue tracker, metrics or logs backend, an MCP server | repository or team | the repository, or nowhere when it can be detected | yes, when written down |
| **Location** | where other repositories, tools, or shared folders are on disk | machine or developer | the developer's workspace, often outside any repository | no |
| **Procedure** | how to run, drive, and verify this app; how to release this project | repository | the repository, often as a project-local skill | yes |

When a dependency does not fit a row,
decide the scope that varies first.
The binding belongs at that scope:
a fact that differs per machine does not belong in a committed file,
and a fact the whole team shares
does not belong in one developer's home directory.

## Specify what happens when the binding is missing

Every skill that resolves a binding
says what to do when it finds none,
or finds one that is stale.
Without that instruction an agent guesses.
The usual choices:

- **Ask and point to setup.** Ask the user for the missing fact,
  and name the setup skill that would record it.
  Do not run setup as a side effect of a lookup.
  This is the safe default.
- **Proceed without it.** Right when the binding only adds context,
  such as optional domain docs.
  Say so explicitly,
  so the agent does not stop to ask.
- **Stop.**
  Right when acting without the binding could do harm,
  such as publishing to the wrong tracker.

## Pair a setup skill with each consumer

A binding someone has to write by hand rarely gets written.
A pattern that works:
one skill creates or updates the binding,
and one or more skills consume it.

- The **setup** skill
  is user-invoked only.
  It inspects what it can, proposes the binding,
  asks about what it cannot know,
  and writes the result after the user approves it.
- The **consumer** skills
  are auto-invoked.
  They read the binding, act through it,
  and fall back as described above when it is missing.
  They never edit it.

When the interface changes,
existing bindings go stale.
The setup skill should be safe
to rerun on an existing binding:
it reads what is there,
keeps what the user wrote,
and proposes a diff.

## Catalog of resolution patterns

How a consumer finds the binding.
These are options, not a ranking;
several can combine,
such as detection with a file that overrides it.
Add a pattern here when a skill uses one that is not listed,
with the same four parts.

### Detection

The agent works the binding out from the environment:
`git remote -v` for the forge,
the tools it has for an MCP server,
a `justfile` or `package.json` for how to run things.

- **Fits:** capabilities and procedures
  whose answer is observable and unambiguous.
- **Binding lives:** nowhere;
  the environment is the binding.
- **Missing:** detection found nothing or more than one candidate.
  Ask.
- **Watch for:**
  the skill has to say what to look at.
  "Use the repository's forge"
  without saying how to tell leaves each agent
  to invent its own check.

Prefer detection over configuration
for anything observable.
Ask users to configure only what cannot be detected,
such as which Jira project or which dashboard folder.

### Convention file in the repository

A file at a known path in the repository records the binding,
and the repository's `AGENTS.md` points to it.
Consumer skills read the file before acting.

- **Fits:** capabilities and procedures
  that the whole team shares for this repository.
- **Binding lives:** the repository,
  committed and reviewed like code.
- **Missing:** the file is absent.
  Ask, or proceed if the binding is optional,
  and name the setup skill.
- **Example:** Matt Pocock's
  `setup-matt-pocock-skills` writes
  `docs/agents/issue-tracker.md` from a template for GitHub, GitLab,
  or local markdown,
  or from a prose description for anything else.
  The templates are written as an interface table:
  "When a skill says 'publish to the issue tracker'"
  followed by the concrete action.
  Consumer skills only use the phrases.

### Generated project-local skill

The interface is a skill shape
(required sections, what each must contain),
and a generator skill writes one implementation per repository into `.agents/skills/`.
Consumers load whichever skill of that shape the repository has.

- **Fits:** procedures,
  where the implementation is too long or too specific
  for a config file.
- **Binding lives:** the repository,
  as a committed skill.
- **Missing:**
  no skill of that shape exists.
  Point to the generator.
- **Example:**
  `create-verification-skill` writes `verify-<app>`
  with Launch, Doctor, Drive, Proof, Cleanup, and Features sections;
  `maintain-verification-skill` keeps it current.
  Any skill that needs to see a change working loads
  the repository's `verify-*` skill
  without knowing how the app runs.

### Ancestor-walk lookup script

The consumer skill ships a script
that walks from the current directory up to `/`
and prints the first file with a known name,
with its absolute path on the first line
so relative paths inside it can be resolved.
The file sits in the developer's workspace root,
above the repositories it describes.

```sh
#!/usr/bin/env bash
set -euo pipefail
directory=$(pwd -P)
while :; do
  map="$directory/WORKSPACE_MAP.md"
  if [ -f "$map" ]; then printf '%s\n' "$map"; cat "$map"; exit 0; fi
  if [ "$directory" = / ]; then echo "No WORKSPACE_MAP.md in this directory or its ancestors." >&2; exit 1; fi
  directory=$(dirname "$directory")
done
```

- **Fits:** locations,
  and anything else that varies per machine or developer.
- **Binding lives:** the developer's workspace,
  outside version control or in a directory no repository commits.
- **Missing:** the script exits non-zero.
  Ask the user for the location and name the setup skill.
- **Watch for:** a workspace outside the ancestor chain
  (a worktree elsewhere, a second workspace)
  does not find the map.
  Say so in the skill
  rather than letting the agent assume the map is global.
  The script also keeps the binding out of context
  until a skill needs it,
  unlike content placed in `AGENTS.md`.
- **Example:** a workspace-map pair,
  where a setup skill inspects the child directories of a workspace,
  matches them against a catalog of expected repositories,
  and writes the map after review;
  the lookup skill runs the script
  and resolves only the entry it needs.

### Harness configuration

The harness asks the user for values
when the skill is installed
and substitutes them into the skill.
Claude Code plugins declare typed `userConfig` fields in `plugin.json` and substitute `${user_config.KEY}` into skill content.

- **Fits:** values per user
  that the harness can prompt for,
  such as a default project key.
- **Binding lives:** the harness's settings for that user.
- **Missing:** depends on the harness;
  often the literal placeholder reaches the agent.
- **Watch for:**
  it ties the skill to one harness.
  Avoid it for skills meant to work across harnesses.

### Environment variables

The skill reads a variable
such as `ISSUE_PROJECT`.

- **Fits:** values that tooling outside the agent already sets,
  or that CI must provide.
- **Binding lives:** the user's shell profile
  or the CI configuration.
- **Missing:** the variable is unset.
  Ask, and say which variable to set.
- **Watch for:** variables are hard to discover and rarely documented.
  The skill has to name every variable it reads.
