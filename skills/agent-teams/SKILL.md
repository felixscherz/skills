---
name: agent-teams
description: Use when work is larger than one agent should carry and a lead should plan it with the user, brief subagent workers, accept their results, and report status - planning work for delegation, running a plan as its lead, delegating a task through a BRIEF.md, reviewing a worker's RESULT.md, or the start and end of a session as the lead of an agent workspace. Not for workers following a BRIEF.md, and not for independent single-agent work.
---

# Agent teams

One lead agent coordinates; workers do the detailed work. The lead talks to the user, plans, briefs workers, accepts
their results, and keeps the state of the work in files, so the work can outlive any one context window and any one
session.

| Term | Meaning |
| --- | --- |
| Lead | The one agent that talks to the user, owns the plan and the status, and assigns tasks |
| Worker | A subagent the lead starts for one task: implementation, investigation, review, or setup |
| Plan | One larger effort: its goal, design, constraints, ordered tasks, and how it is reviewed |
| Task | A bounded unit of work for one worker, with a brief from the lead and a result from the worker |

## Topology

One lead spawns workers. Workers report to the lead; they do not spawn workers, coordinate each other, or talk to the
user. A review or investigation worker is still a worker. Peer-to-peer teams and nested leads are out of scope.

Workers never load this skill. A worker knows only its brief, which carries everything it needs: absolute paths, where
it may write, how to work, and how to report. Workers do load the skills their work needs, such as engineering
guidance.

## Where the team's files live

The team works in an agent workspace (see the `agent-workspace` skill): the repos it changes are writable members, so
every task works on an isolated branch. If there is no workspace yet, propose setting one up before the first task.

```
<workspace>/
├── AGENTS.md            # gets a "Who you are" section (templates/AGENTS-section.md)
├── STATUS.md            # the lead's report on the current state
├── memory/              # the lead's memory, via agent-memory; the journal lives here
├── plans/
│   └── <slug>.md        # one file per plan, with its progress table
└── tasks/
    └── NNNN-slug/
        ├── BRIEF.md     # lead -> worker
        ├── RESULT.md    # worker -> lead
        └── checkout/    # gitignored; extra worktrees for this task, if any
```

The lead owns `STATUS.md`, the plans, the briefs, and the memory. A worker writes only its `RESULT.md`, the memory's
inbox, and the paths its brief allows inside writable members.

## Reviewable checkpoints

A plan produces more change than anyone can review at once. Every accepted task leaves a checkpoint that can be
reviewed on its own: a short series of commits, or a PR stacked on the previous task's. The `engineering` skill's
"Keep work reviewable" rule (`../engineering/references/keep-work-reviewable.md`) covers how to shape them.

## References

Identify the current phase and read only the reference it needs.

- **Planning** (`references/planning.md`). Working with the user before execution to define a plan, divide it into
  tasks, and record it for a later run.
- **Lead** (`references/lead.md`). You are the lead: at the start and end of every session, running a plan, accepting
  results, handling issues, replanning, and setting a workspace up for a lead.
- **Tasks** (`references/tasks.md`). Writing a brief, starting a worker, giving a worker its own checkout, or reviewing
  and closing a task.

Loading this skill does not authorize running a plan. A planning session stays pre-execution until the user authorizes
execution.
