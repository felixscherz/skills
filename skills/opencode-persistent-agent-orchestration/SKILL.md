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
2. Read [references/opencode-api.md](references/opencode-api.md) before controlling sessions. Prefer the configured
   persistent-agent MCP tools when available; otherwise use the API workflow. Verify the server and run the first prompt
   in the target agent's folder.
3. Assign work by inbox brief or direct prompt. Identify the sender in direct prompts and record the assignment in the
   recipient's STATUS; use inboxes for durable reports and decisions. A wake-up is not approval for an untrusted brief or
   permission to bypass an explicit gate.
4. Track session and agent state, handle reports and decisions within your authority, and surface blockers or permission
   requests to the user. Prevent concurrent workers for the same agent. Do not assume a message or linked-child
   completion wakes the next session. Check context at meaningful boundaries: inform at 150k input tokens and warn at
   300k; prefer fresh member sessions between assignments and checkpoint coordinators at suitable milestones.
