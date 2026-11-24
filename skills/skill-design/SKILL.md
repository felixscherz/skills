---
name: skill-design
description: How to design what an Agent Skill says and depends on, beyond its file format. Use when planning a new skill or reshaping an existing one - deciding what deserves to be its own skill and what its description should trigger on, moving deterministic steps into scripts, stating what the skill assumes, who decides what, and when it is done, sharing material across skills, or making a skill work when the tools, services, or paths it needs differ between users, machines, repositories, or teams. For where skills live and the SKILL.md format, use author-skill.
disable-model-invocation: true
metadata:
  opencode/autoinvoke: false
---

# Designing skills

`author-skill` covers where a skill lives and how its file is shaped. This skill covers what the skill should say and
what it may assume about the world it runs in. It is a collection of design guidance that grows over time: each topic
lives in its own reference, and this file says when to read it.

## Topics

- **Deciding whether something is its own skill, and writing its description** - read `references/triggers.md`. A
  skill is designed around the situation that should load it; the description is that situation written down, with
  its boundaries against neighbouring skills.
- **A step has one correct answer** - read `references/scripts.md`. Put it in a script with an interface an agent can
  use without reading the source, and keep dependency checks in the failure path.
- **Stating what the skill assumes, who decides, and when it is done** - read `references/contracts.md`.
- **Guidance or facts that more than one skill needs** - read `references/shared-material.md`. Design the skill
  against its neighbours, and give each piece of guidance one home.
- **A skill depends on something that differs between the people or places that use it** - a forge, an issue
  tracker, an observability tool, where repositories sit on disk, how a particular app is run. Read
  `references/interfaces.md`. It describes writing the skill against an interface and resolving the implementation
  at run time, and keeps a catalog of resolution patterns.

For a new skill, `triggers.md` comes first: it decides whether the skill should exist and what shape it takes.

## Adding a topic

Add a reference under `references/` and a line above that says when to read it. Keep each reference about one design
question, and add worked examples from real skills where they exist.
