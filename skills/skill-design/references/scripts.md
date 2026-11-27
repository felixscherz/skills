# Scripts: take the guesswork out of deterministic steps

When a step has one correct answer,
write it as a script and have the skill run it,
instead of describing it in prose
and letting each agent reconstruct it.
Prose gets reinterpreted on every run;
a script does the same thing every time.

Good candidates:

- Finding something:
  a file in the ancestor chain,
  the repository for a name,
  the forge behind a remote.
- Starting and stopping things:
  launching an app on its own port,
  waiting until it is ready,
  cleaning up by recorded PID.
- Transforming or checking data with fixed rules:
  parsing output,
  validating a file's shape,
  rendering a template.
- Any sequence of commands
  that has to run in a specific order with specific flags.

Leave judgement to the agent:
what to look up,
how to read the result,
what to do when it is surprising.

## The script's interface is part of the skill

The agent uses a script
through how it is called and what it prints,
so design that the way you would a CLI
for someone who will never read the source.
A helper the reader has to read to use
is not a helper.

- **Show the invocation in `SKILL.md`**,
  with the path relative to the skill's directory,
  and make the script executable.
- **Print what the agent needs,
  in a shape it can use.** A path on the first line and content after it;
  JSON when the output has structure;
  nothing decorative.
- **Fail with the next step.** Exit non-zero
  and say on stderr what was missing
  and what to do about it:
  "No WORKSPACE_MAP.md in this directory or its ancestors"
  tells the agent exactly what to ask for.
- **Be safe to rerun.** Idempotent where possible.
  Record what was started (PIDs, ports, session names)
  so cleanup stops exactly that and nothing else.
- **Stay portable.** Plain `bash` or a language the target machines have,
  no dependencies the skill does not mention,
  and no assumption about the current directory
  beyond what the skill states.

## Checks belong in the failure path

A script can check that the tools and files a skill needs exist,
but do not make the agent run that check every time the skill loads.
In the normal case everything is there,
and an upfront check costs time on every run to catch a rare problem.
Assume the dependencies are present,
act, and give the skill a section on what to do
when something turns out to be missing
(see `contracts.md`).
A check script is useful there:
run it after a failure to tell the agent which piece is missing.
