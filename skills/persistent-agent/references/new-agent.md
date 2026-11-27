# Scaffolding a new agent

Done only when the user asks,
in a session they started.
    `<home>` is the agents home,
    `<agent>` the new folder name.

1. Get from the user:
   the agent's name (kebab-case),
   the path of the agents home (ask, there is no default),
   and the content of its role
   (see [roles.md](roles.md)).
   Stop if `<home>/<agent>` exists.
2. If `<home>/AGENTS.md` is missing,
   this is the first agent:
   write the shared file with the user
   (see [layout.md](layout.md))
   and link it, `ln -s AGENTS.md CLAUDE.md` in `<home>`.
3. Create the folders:

   ```sh
   mkdir -p <home>/<agent>/journal <home>/<agent>/inbox/archive
   ```

4. Fill from `templates/` into `<home>/<agent>/`:
   `AGENTS.md`, `ROLE.md`, `STATUS.md`.
   Show the user the `ROLE.md` before writing it.
5. Link: `ln -s AGENTS.md CLAUDE.md` in `<home>/<agent>`.
6. Write the first journal line,
   "Agent created.",
   in `journal/YYYY-MM.md`
   (see [journal.md](journal.md)).
7. Tell the user the path to start sessions in,
   and which other agents' `ROLE.md` need a line
   for the new agent under "Other agents".
   The user makes those edits,
   or tells the owning agent to;
   do not edit them yourself.

`brief.md` and `report.md` are not copied;
    agents read them from the skill
when they write a message.
