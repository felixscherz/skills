# Layout

```
agents/                  # the agents home
├── AGENTS.md            # shared conventions for all agents
├── CLAUDE.md -> AGENTS.md
├── <agent>/
│   ├── AGENTS.md        # stub: "you are a persistent agent"
│   ├── CLAUDE.md -> AGENTS.md
│   ├── ROLE.md
│   ├── STATUS.md
│   ├── journal/
│   │   └── YYYY-MM.md
│   └── inbox/
│       ├── <message>.md
│       └── archive/
└── <agent>/
```

An agent's first prompt is always run in `agents/<agent>/`, never in `agents/` or another agent's folder.

## Shared `agents/AGENTS.md`

Holds what is true for every agent:
that these folders are persistent agents,
that each loads the `persistent-agent` skill,
    and any house rules the user adds.
    Keep it short;
it is loaded on every boot.
It does not list the agents.

## Per-agent `AGENTS.md`

A stub from `templates/AGENTS.md`. It names the agent,
    says it is a persistent agent,
and tells it to load this skill and boot.
Everything about the role goes in `ROLE.md`, not here.

The stub points
at `../AGENTS.md` explicitly,
because not every harness loads instruction files from parent folders.
Read the shared file at boot if it is not already
in your context.

## `CLAUDE.md` symlinks

Claude Code reads `CLAUDE.md`, opencode reads `AGENTS.md`.
Next to every `AGENTS.md`, in the agents home and in each agent folder:

```sh
ln -s AGENTS.md CLAUDE.md
```

Edit `AGENTS.md` only.
