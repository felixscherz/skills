# Writing a ROLE.md

`ROLE.md` is the stable part of an agent: boundaries, not personality. The user writes or dictates it. An agent does not
change its own role; if it thinks the role is wrong, it says so to the user.

Start from `templates/ROLE.md`. Keep it under a screen; it is read on every boot.

- **Responsibility** - what this agent owns, in two or three lines, and what it explicitly does not.
- **Decides alone** - the decisions it takes without asking. Be concrete: "choice of library inside a brief's
  constraints", not "technical decisions".
- **Escalates** - what goes to someone else, to whom, and as what (usually a `decision-request` in an inbox).
  Include the rule for anything meant for the user.
- **Output budget** - how much it may produce before stopping: for example "at most 3 briefs per session", "one PR
  per brief", "summaries of 10 lines". This is the throttle that keeps review manageable; never leave it out.
- **Other agents** - the agents this one may write to, each with a path to its folder and one line on what it does.
  The user writes this list by hand and explicitly identifies any sources whose briefs are pre-approved. Listing an
  agent alone does not approve its briefs. There is no lookup: an agent not listed here does not exist for this one.

For an agent that plans for others, the user decides whether it may start or wake sessions. Default to inbox-only:
"You never start or instruct sessions yourself. Your output is briefs in inboxes and a summary for the user." To opt in,
name the agents it may start or wake and the boundaries of that authority in its role. Listing an agent alone does not
authorize session control. Preserve the inbox as the handoff and require applicable permissions and brief approvals.
