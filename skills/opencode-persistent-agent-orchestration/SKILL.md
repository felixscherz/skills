---
name: opencode-persistent-agent-orchestration
description: Use when coordinating, starting, waking, or following up folder-based persistent agents through the OpenCode API, including an engineering lead or external runner, selecting the right OpenCode server, or moving linked child sessions before their first prompt. Not for ordinary OpenCode subagents or working as one persistent agent without session orchestration.
---

# OpenCode persistent-agent orchestration

Coordinate folder-based persistent agents through OpenCode while keeping their inboxes and state files as the durable
handoff. This skill documents a workflow, not an installed scheduler or runner.

1. If you are a persistent agent, load `persistent-agent` and complete its boot ritual first. Check your `ROLE.md` and
   the user's authorization before starting or waking another agent. Follow stricter role, project, harness and tool
   rules. Do not treat API access as authorization.
2. Read [references/opencode-api.md](references/opencode-api.md) before controlling sessions. Select and verify the
   server that owns the intended sessions, then use the target agent's folder as the location of its first prompt.
3. Assign work and send decisions and reports through inbox files. Wake the recipient to process its inbox; a wake-up
   is not approval for an untrusted brief or permission to bypass an explicit gate.
4. Track session and agent state, handle reports and decisions within your authority, and surface blockers or permission
   requests to the user. Prevent concurrent workers for the same agent. Do not assume a message or linked-child
   completion wakes the next session.
