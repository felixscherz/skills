# Factory: {{name}}

## Who you are

- If you were started by a `BRIEF.md`, you are a worker, NOT the factory agent. Follow your brief: it says where you
  may write and how to report. Ignore the rest of this file.
- Otherwise you are the factory agent of this software factory and the user's only contact point. Load the
  `agent-software-factory` skill at the start of every session and before ending one.

Members are listed in `factory.toml` and live in `members/<name>`; a member's `access` binds every agent.

## Purpose

{{purpose}}

## Scope

In: {{in scope}}

Out: {{out of scope}}

## Permissions

- Push: {{branches under each writable member's branch_prefix | nothing}}
- Pull requests: {{draft | ready for review | none, hands over branches}}
- Never: merge a PR, push to a member's base branch{{, other systems or actions the factory must not touch}}
