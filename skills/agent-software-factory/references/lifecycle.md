# Lifecycle

Creating, onboarding, recreating, pausing, and closing a factory. Templates are in this skill's `templates/`
directory; replace every `{{placeholder}}` when you copy one. Git does not track empty directories, so put an empty
`.gitkeep` in each directory you create empty.

Never commit in the factory repo. When you are done, tell the user what changed so they can commit it.

## Create a factory

1. Get a name (kebab-case), a one-line purpose, and a location from the user. This skill imposes no convention for
   where factories live; a directory next to the repos they work on works well.
2. Create the directory and run `git init` in it.
3. Scaffold it:
   - `.gitignore` from `templates/gitignore`.
   - `AGENTS.md` from `templates/AGENTS.md` with name and purpose filled in. Leave scope and permissions as
     placeholders; onboarding fills them.
   - `factory.toml` from `templates/factory.toml` with name, purpose, today's date, and `status = "active"`. Leave out
     members.
   - `STATUS.md` from `templates/STATUS.md`.
   - The memory (see "Set up the memory" in `memory.md`).
   - An empty `backlog/`.
4. Onboard it now if the user is here, otherwise tell them to open a session in the factory root to do it.

## Onboard a factory

A factory needs onboarding when its `AGENTS.md` still has placeholders.

1. Ask the user what the factory should work on and what is in and out of scope, such as which modules or which kinds
   of change.
2. Ask which git repos and files the work needs. For each: where it comes from (a local clone, a URL, or a path) and
   whether the factory writes to it. Default to read-only unless the work changes it.
3. Ask what the factory may do with its work: push branches, open PRs as drafts or ready for review, and what it must
   never touch. Default to pushing branches under the prefix and opening draft PRs.
4. Fill in `AGENTS.md`.
5. Add each member (see `members.md`).
6. Write what the user said about the work they want, beyond the scope, into a note, such as
   `memory/notes/what-the-user-wants.md`.

## Recreate a factory

A factory whose repo is there but whose `members/` is missing or incomplete, such as after cloning the factory repo
on another machine, is recreated from `factory.toml`:

1. Check each `git` source that is a local clone and each `path` source exists. A source that is missing on this
   machine is a question for the user: where is it here? Update the entry with their answer.
2. Build every missing member as in "Add a member" in `members.md`, skipping the step that records the entry. Writable
   git members continue on their existing `<branch_prefix>main` when it exists.
3. For each backlog item that is `in-progress` or `pr-open`, add its checkout again on its existing branch, fetching it
   from the remote if the local clone does not have it.
4. Report what was built, and anything that could not be: an unpushed branch in a clone that is gone is lost.

## Pause a factory

Set `status = "paused"` in `factory.toml`. Members stay. Say in `STATUS.md` why it is paused and what would resume
it.

## Close a factory

1. Consolidate the memory (see `memory.md`).
2. Tell the user which backlog items are still `in-progress` or `pr-open`, and ask what to do with them.
3. Remove every item checkout, then every member (see `members.md`).
4. Set `status = "closed"` in `factory.toml`.

The factory directory and its files stay, and in its git history once the user commits.
