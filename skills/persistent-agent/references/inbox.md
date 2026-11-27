# Inbox

One way agents and the user reach an agent
is a markdown file per message in its `inbox/`.
Every message is a file the user can read, edit, or delete
before anyone acts on it.
Authorized coordinators may also send direct session prompts;
record assignments and decisions from them in STATUS and send durable reports
through the recipient's inbox.

## Ownership rule

An agent keeps its own state inside its folder
and may create new files
in other agents' `inbox/`.
It may also work in repositories
or strands authorized by the user or an approved brief,
within the task's scope.
Never edit another agent's `ROLE.md`, `STATUS.md`, journal, or a message already delivered.
A correction is a new message.

Other agents' paths come from your `ROLE.md`.
If the recipient is not named there, ask the user;
do not search for it.

## Message file

Name:
`YYYY-MM-DD-HHMM-<from>-<slug>.md`, so the inbox sorts by time.

```markdown
---
from: eng-lead
to: engineer-1
type: brief
date: 2026-11-16 14:05
---

<body>
```

`from` and `to` are agent folder names,
or `user`.

## Types

| Type | Meaning | Body |
| --- | --- | --- |
| `brief` | Work for the recipient to do | `templates/brief.md` |
| `report` | Result of work, back to whoever briefed it | `templates/report.md` |
| `decision-request` | A decision the sender may not make alone | Question, options, recommendation, what waits on it. A few lines. |
| `fyi` | Information, no action expected | A few lines. |

Sending an inbox message starts nothing.
The recipient sees it when a user,
an authorized coordinator or a runner starts or wakes its session.
An assignment from the user or a source explicitly pre-approved
in the recipient's `ROLE.md` is approved without further confirmation,
whether delivered by inbox or direct prompt.
For any other source,
ask the user to confirm before starting.
A wake-up is not confirmation.
Stay within the assignment and applicable permissions;
a pre-approved source
does not authorize work outside those bounds.
Explicit approval gates still apply unless properly superseded.

## Handling and archiving

A message is handled
when its content is acted on or absorbed into STATUS:
a brief when its report is sent,
a report or fyi when STATUS reflects it,
a decision-request when the decision is made.
At checkpoint,
move handled messages to `inbox/archive/` unchanged.
Unhandled messages stay,
and STATUS says why.
