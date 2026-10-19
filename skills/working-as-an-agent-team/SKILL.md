---
name: working-as-an-agent-team
description: Use when work in a software factory is larger than one agent should carry and the factory agent should act as an orchestrator that delegates to subagent workers - planning work for a handoff to workers or to another agent's session, running a plan as its lead, delegating a task through a BRIEF.md, or reviewing a worker's RESULT.md. Also when the user says "work on this as a team", "start orchestrating", "plan this for a team", or "delegate this". Not for workers following a BRIEF.md, and not for work that fits one agent and one PR.
---

# Working as an agent team

This skill changes how the factory agent works: it stops doing the work itself and becomes the lead of a team. The
lead talks to the user, plans, briefs workers, accepts their results, and keeps the state of the work in files, so
the work can outlive any one context window and any one session. Everything the `agent-software-factory` skill says
still holds; this skill adds plans and tasks to it.

| Term | Meaning |
| --- | --- |
| Lead | The factory agent while it orchestrates: talks to the user, owns the plan, and assigns tasks |
| Worker | A subagent the lead starts for one task: implementation, investigation, review, or setup |
| Plan | One larger effort: its goal, design, constraints, ordered tasks, and how it is reviewed |
| Task | A bounded unit of work for one worker, with a brief from the lead and a result from the worker |

## Planning or orchestrating

Decide which phase you are in before anything else. When it is unclear, you are planning.

- **Planning.** The user and you are still designing what will be built, and nothing runs yet. Design with the team
  in mind: a plan is only needed because the work will be handed off, to workers or to another agent's session, so
  write it for a reader who was not in the conversation. Divide it into tasks a fresh worker can do from its brief
  alone, each leaving a checkpoint that can be reviewed on its own, with the invariants that must hold in between.
  Read `references/planning.md`.
- **Orchestrating.** The user authorized running a plan. You are the lead: delegate the source code, debugging, and
  review to workers, and keep to coordination yourself. Read `references/lead.md`, and `references/tasks.md` when you
  write a brief or review a result.

Loading this skill does not authorize running a plan. A planning session stays pre-execution until the user authorizes
execution, and finishing a plan does not start it.

## Topology

One lead spawns workers. Workers report to the lead; they do not spawn workers, coordinate each other, or talk to the
user. A review or investigation worker is still a worker. Peer-to-peer teams and nested leads are out of scope.

Workers never load this skill or `agent-software-factory`. A worker knows only its brief, which carries everything it
needs: absolute paths, where it may write, how to work, and how to report. Workers do load the skills their work
needs, such as engineering guidance.

## Where the team's files live

The team works in a software factory (see the `agent-software-factory` skill): the repos it changes are writable
members, so every task works on an isolated branch. If there is no factory yet, propose setting one up before the
first task. This skill adds two directories to it:

```
<factory>/
├── plans/
│   └── <slug>.md        # one file per plan, with its progress table
└── tasks/
    └── NNNN-slug/
        ├── BRIEF.md     # lead -> worker
        ├── RESULT.md    # worker -> lead
        └── checkout/    # gitignored; extra worktrees for this task, if any
```

The lead owns the plans and the briefs, next to everything the factory agent already owns. A worker writes only its
`RESULT.md`, the memory's inbox, and the paths its brief allows inside writable members. A plan usually serves one
backlog item: the item links to the plan and stays `in-progress` until the plan is done.

## Reviewable checkpoints

A plan produces more change than anyone can review at once. Every accepted task leaves a checkpoint that can be
reviewed on its own: a short series of commits, or a PR stacked on the previous task's. The `engineering` skill's
"Keep work reviewable" rule (`../engineering/references/keep-work-reviewable.md`) covers how to shape them.

## Stop working as a team

When the plan is done, paused, or abandoned, update the plan's status and its backlog item, and go back to working as
the factory agent. Open tasks and running plans bring you back into this skill at the start of the next session.

## References

Identify the current phase and read only the reference it needs.

- **Planning** (`references/planning.md`). Working with the user before execution to define a plan, divide it into
  tasks, and record it for a later run.
- **Lead** (`references/lead.md`). You are the lead: at the start and end of every session with a running plan,
  running a plan, accepting results, handling issues, and replanning.
- **Tasks** (`references/tasks.md`). Writing a brief, starting a worker, giving a worker its own checkout, or reviewing
  and closing a task.
