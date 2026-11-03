# Find the cause

Investigate a failure until its cause is known and proven by a reproduction. The goal is a diagnosis, not a fix: the
agent explains what went wrong and why, and shows a minimal reproduction as evidence. Fixing is a separate task the
user decides on afterwards.

## Applies when

The user brings information about a bug in production, an error in a system, or a regression, and asks what the
problem is or why it happened. The information can be an error message, a stack trace, a ticket, a link to logs or a
dashboard, or a description of what users saw.

## Who decides

- The user decides whether, when, and how the problem gets fixed. The agent does not change product code, commit, or
  open a PR in this playbook.
- The user confirms the expected behavior when it is not clear from the code, the docs, or the report.
- Access to running systems is read-only. Reading logs, metrics, traces, and data is fine where the user pointed to
  them or the agent already has access. Anything that changes state in a shared environment, such as replaying
  messages, restarting a service, or writing to a database, waits for the user.
- The agent decides how to investigate: which codebases to read, which hypotheses to test, and how to reproduce.

## Steps

1. Pin down the failure. State what should have happened, what happened instead, and exactly where they differ: the
   inputs, the time, the environment, the error. When the expected behavior is unclear, ask the user before going on.
2. Determine which systems play a role and which codebases belong to them. Read the nearest `CONTEXT.md` of each. When
   a codebase is not available locally, ask the user for it. Find out which version of each system was running when
   the failure happened, and read that version of the code, not only the main branch.
3. Gather the evidence the user pointed to: follow links, read logs, traces, and persisted data. Read the actual error
   and the events around it rather than the summary. Ask the user for access or for more information when the
   evidence that would settle a question is out of reach.
4. Find the cause (`../references/find-the-root-cause.md`). Follow the data and control flow back from the symptom to
   where the bad state was first created. When several causes could explain the evidence, list them and eliminate them
   one by one.
5. Reproduce the failure with the smallest setup that shows it: a unit test against the code at the version that was
   running, or a short script. It must fail the same way the report describes, for the reason you named. Keep a
   reproducing test uncommitted in the working tree, and put a script outside the repository. When the failure cannot
   be reproduced, say so and do not call the cause proven.

## Done

A diagnosis in the reply: the symptom, the cause with the file and line where the bad state is created, the chain from
cause to symptom, and the evidence for each link. It names the reproduction and how to run it, the candidate causes
that were eliminated and what ruled each out, and anything that is still unexplained. It may say where a fix belongs,
without making it. The next step is the user's: usually a bug fix, which starts from the reproduction as its failing
test.
