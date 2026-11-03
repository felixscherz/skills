# Playbooks

This README is for developing the skill. Nothing links to it, and agents following a playbook do not need it.

## Goal

A playbook encodes the workflow I expect an agent to follow for one kind of task: the steps, in order, and where I
stay in the loop. When I hand an agent a task, the matching playbook should make it work the way I would want it to
without my having to spell the workflow out each time.

Playbooks do not hold principles or guidelines. They reference them. The material on what good looks like (type
design, testing, PR descriptions, the shape of a spec) lives in `../references/`, and each step names the reference it
needs at the point it applies. That keeps one definition per guideline, shared by every playbook that uses it, and it
lets the playbook decide when a guideline matters instead of the agent reading everything up front.

## Writing a playbook

- Start from what I expect to happen for the task, not from the references available. If I would be surprised or
  annoyed by an agent skipping a step, it belongs in the playbook.
- Say who decides what. The decisions that wait for me are the main thing a playbook adds over the references.
- Keep steps concrete and ordered, and link to references rather than restating them. When a step needs a rule that
  does not exist yet, write it as a reference.
- When an agent did something I did not expect, change the playbook so the next one does.

The file format and index rules are in the `reflect-on-engineering` skill, and the reasoning behind the split between
playbooks and references is in `docs/engineering-skill.md` at the root of the skills repo.
