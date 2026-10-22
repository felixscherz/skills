# Tasks

How the lead hands a task to a worker and takes the result back. A task lives in `tasks/NNNN-slug/` with a `BRIEF.md`
written by the lead and a `RESULT.md` written by the worker.

## The worker knows only its brief

A worker does not load this skill and does not know about plans, the memory, or the status. So the brief carries
everything it needs: the goal and why it matters, what to read first, where it may write, what is out of bounds,
what done looks like, how to work, and how to report. Write every path as an absolute path: the worker may run from
inside a member, where relative paths resolve differently. Writable paths come only from members with
`access = "write"`.

Keep acceptance criteria bounded to the task's role in the approved outcome. Include non-goals and known limitations
that affect implementation choices. Tell workers to report unexpected prerequisites or material growth before solving
them, naming the affected criterion, the concrete consequence, and the smallest safe next step with its limitation.
Workers and reviewers may recommend scope changes; only the lead, within the user's approval, may settle them.

## Delegate a task

1. Pick the id: the highest id in `tasks/` plus one, zero-padded to four digits, plus a short kebab-case slug. Task
   folders are never deleted, so ids are never reused.
2. Create `tasks/NNNN-slug/BRIEF.md` from `../templates/BRIEF.md` and fill in every placeholder. Copy the inbox item
   format from `../../agent-software-factory/templates/inbox-item.md` into it. Keep the opening line as the template
   has it: the factory's `AGENTS.md` may still reach the worker through parent-directory lookup, and that line tells it
   that it is not the factory agent.
3. Decide where the worker writes. If another worker writes the same member at the same time, give this one its own
   checkout (below), or run them one after the other. Read-only members can be shared freely.
4. Start the worker as a subagent with your harness's mechanism. Its prompt is only:
   `Read <absolute path to BRIEF.md> and carry out the task it describes.`
5. Add the task to the plan's progress table, if it belongs to a plan.

Run several workers in parallel only when their tasks are independent and do not write the same checkout.

## Give a worker its own checkout

Add a worktree of the member under the task folder, on a branch under the member's `branch_prefix`:

```sh
git -C <ws>/members/<member> worktree add -b <prefix><task id> <ws>/tasks/<task id>/checkout/<member> <start point>
```

The start point is usually the plan's branch. Name the checkout's absolute path as the writable path in the brief.
When the task is accepted, integrate its branch as the plan says, then remove the checkout with
`git -C <ws>/members/<member> worktree remove <ws>/tasks/<task id>/checkout/<member>`.

## Review a result

1. Read `RESULT.md`. For implementation tasks, start a fresh review worker with a read-only brief that names the task,
   the revision, the acceptance criteria, and the invariants (see "Keep review independent" in `lead.md`).
2. If the result falls short, apply the scope check in "Handle issues through workers" in `lead.md` before assigning
   another repair. For an in-scope repair, add a `## Follow-up` section to `BRIEF.md` that says what is missing, and
   start a worker on the same brief. It appends to `RESULT.md`. Do not silently enlarge acceptance criteria in a
   follow-up.
3. When it is accepted, set `status: closed` in the brief's frontmatter and update the plan's progress table. Do not
   delete the folder: inbox items name the task, and consolidation may need its result.

Leave the worker's inbox items in the memory's inbox. Consolidation resolves them, not the review.
