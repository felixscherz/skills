# Planning

Plan with the user before execution. The output should let a fresh lead run the plan and fresh workers complete their
tasks without reconstructing the planning conversation.

## Define the plan

- Agree on the goal, completion criteria, scope, non-goals, and decisions that remain with the user.
- Understand the affected system and dependencies. Use investigation tasks when delegation is authorized; their
  results inform the plan and do not authorize implementation.
- Record behavior and other invariants that must hold throughout execution, not just in the final state.
- Record execution permissions, including whether commits, pushes, PRs, or other external changes are authorized.
  Planning permission alone is not permission to execute or ship. Name the systems workers must not touch precisely
  (for example deployed databases) and whether local test infrastructure is allowed.
- Record where the work happens: which members it changes and the branch under the member's prefix, such as
  `<prefix><plan slug>`, created before the first task.
- Agree on the review checkpoints: what each task hands over for review (commits on a shared branch, or one PR per
  task stacked in dependency order), who reviews it (the user, a review worker, or both), and whether a dependent
  task waits for that review. Without permission to commit, tasks cannot leave checkpoints, so raise it with the user
  rather than planning work that ends in one large uncommitted diff.

## Divide it into tasks

- Give each task one coherent outcome, dependencies, boundaries, and concrete acceptance criteria.
- Size each task so its result fits in one review. Split a task whose change would be too large to review in one
  sitting, and give preparatory refactors or mechanical moves their own task or commits.
- Include the integration points necessary for the outcome. Scope is not just a list of files: say which behavior may
  change and which must remain intact.
- For staged changes, distinguish adding a replacement, activating it, and removing the old path. State which task
  owns each transition. Every intermediate state should satisfy the plan's invariants.
- Name ownership of shared changes so workers do not independently make conflicting edits or each leave the same
  integration work to someone else.
- Check the order against the code, not only against the design. For each move, rename, or removal, list the modules
  that import or call the code and assign each to a task. For each task, check that its acceptance criteria can be met
  from the state the earlier tasks leave: a test that needs an injection seam belongs after the task that adds it, and
  a caller switched to new code belongs with the wiring that provides it.
- Separate implementation tasks from supporting tasks such as setup, review, or diagnosis.
- Default to sequential tasks. Only plan parallel work when dependencies and writable checkouts are independent and
  that execution model is agreed with the user.

## Record the plan

Write `plans/<slug>.md` in the factory from `../templates/PLAN.md`, and link it from the backlog item it serves, if
any. Use existing document names when the user supplied a plan. Keep shared constraints in the plan and reference
them from briefs; make the constraints critical to one task explicit in its brief rather than relying on the worker to
infer them from the final design.

Write briefs for the first tasks only when their content is settled; later briefs are best written once the earlier
results are in (see `tasks.md`).

Close the planning session with the plan's path, unresolved decisions, and whether the plan is ready to run. Do not
imply that planning completed any task. The user can start a separate lead session from this handoff; the planning
agent does not have to be the later lead.
