# Lifecycle

Creating, onboarding, recreating, pausing, and closing a workspace. Templates are in this skill's `templates/`
directory; replace every `{{placeholder}}` when you copy one. Git does not track empty directories, so put an empty
`.gitkeep` in each directory you create empty.

Never commit in the workspace repo. When you are done, tell the user what changed so they can commit it.

## Create a workspace

1. Get a name (kebab-case), a one-line purpose, and a location from the user. This skill imposes no convention for
   where workspaces live; a directory next to the repos they work on works well.
2. Create the directory and run `git init` in it.
3. Scaffold it:
   - `.gitignore` from `templates/gitignore`.
   - `AGENTS.md` from `templates/AGENTS.md` with name and purpose filled in. Leave scope and done criteria as
     placeholders; onboarding fills them.
   - `workspace.toml` from `templates/workspace.toml` with name, purpose, today's date, and `status = "active"`. Leave
     out members.
4. Onboard it now if the user is here, otherwise tell them to open a session in the workspace root to do it.

## Onboard a workspace

A workspace needs onboarding when its `AGENTS.md` still has placeholders.

1. Ask the user what will be worked on, what is in and out of scope, and what "done" means.
2. Ask which git repos and files the work needs. For each: where it comes from (a local clone, a URL, or a path) and
   whether the workspace writes to it. Default to read-only unless the work changes it.
3. Fill in `AGENTS.md`.
4. Add each member (see `members.md`).
5. Ask whether the workspace should keep a memory across sessions (`agent-memory`) or be run by a lead that delegates
   to workers (`agent-teams`). Each of those skills says how to add itself to the workspace.

## Recreate a workspace

A workspace whose repo is there but whose `members/` is missing or incomplete, such as after cloning the workspace
repo on another machine, is recreated from `workspace.toml`:

1. Check each `git` source that is a local clone and each `path` source exists. A source that is missing on this
   machine is a question for the user: where is it here? Update the entry with their answer.
2. Build every missing member as in "Add a member" in `members.md`, skipping the step that records the entry. Writable
   git members continue on their existing `<branch_prefix>main` when it exists.
3. Report what was built, and anything that could not be: an unpushed branch in a clone that is gone is lost.

## Pause a workspace

Set `status = "paused"` in `workspace.toml`. Members stay. If the workspace has a `STATUS.md`, say there why it is
paused and what would resume it.

## Close a workspace

1. Follow the closing steps of the other skills the workspace's `AGENTS.md` names, such as a last memory
   consolidation.
2. Remove every member (see `members.md`).
3. Set `status = "closed"` in `workspace.toml`.

The workspace directory and its files stay, and in its git history once the user commits.
