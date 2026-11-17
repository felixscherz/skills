# Orchestrating with the OpenCode API

Use this when an authorized coordinator or external runner starts or wakes persistent-agent sessions. It describes
OpenCode V2; for current API shapes check the running server's `/openapi.json` and the
[API](https://opencode.ai/docs/api), [client](https://opencode.ai/docs/build/client),
[instructions](https://opencode.ai/docs/instructions) and [permissions](https://opencode.ai/docs/permissions) guides.
The session routes are experimental. This skill installs no runner or automatic dispatch. If the repository configures
the persistent-agent MCP server, use its `list_agents`, `wake_agent`, `wait_for_change` and `context_status` tools;
the API commands below are the fallback when the MCP server is unavailable.

For `wake_agent`, provide one direct prompt or the name of an existing inbox message and a unique request ID. Reuse that
ID only for an exact retry. If creation or prompt admission is uncertain, inspect the reported session and receipt before
taking further action; do not retry with a new ID to bypass the guard. MCP admission does not mean work completed.
`wait_for_change` runs only while called. Discovery and session metadata do not authorize any assignment.

## Authority and handoffs

- An agent may control another agent's session only when the user explicitly authorizes it or its `ROLE.md` permits
  session control for that named agent. A role that prohibits session control still wins. An external runner also needs
  the user's authorization. Follow any stricter project, harness and tool rules; API access is not permission to bypass
  them. The destination agent must follow its own role, brief and permissions.
- Assignments may be sent by inbox brief or a direct prompt from an authorized coordinator. Identify the sender in a
  direct prompt and record the assignment in the recipient's STATUS. A prompt to process the inbox is a wake-up, not a
  brief or confirmation. A user assignment or a source pre-approved in the recipient's role may start without another
  confirmation; other sources and explicit gates still need the required approval. Send durable reports and decisions
  through inboxes.
- A coordinator handles reports and ordinary decisions within its role and task constraints. Escalate only what falls
  outside those constraints or requires the user's review. Keep ownership of each agent's status, journal and inbox with
  that agent. An orchestrator does not modify another agent's state to unblock it.

## Select and verify the server

Use the server that owns the sessions you intend to control, not whichever server happens to answer first. OpenCode can
have a managed service, an explicit `--server`, and a standalone server with separate session stores. In Code Mode use
the available `opencode` tools for operations they support; for other operations use `opencode api` against the same
server and authentication context as the current session. Plain `opencode api` can discover or start the default managed
service, which may be the wrong server.

1. Find the active connection from the user's configured command, wrapper or profile. Shell aliases and functions may
   not exist in a non-interactive shell. Inspect the configuration or ask the user; do not assume a port, a data
   directory, or that a managed-service discovery result is the active explicit server.
2. With that connection, call `GET /api/info` and look up a **known session ID** with `GET /api/session/{sessionID}`.
   Verify its identity and location match the intended session. A server responding to `/api/info` alone is not proof
   that it owns the right sessions. If the ID or connection is unavailable, ask rather than create or send on a guess.
3. Use the wrapper's authentication and environment, or supply the same credentials through the supported client
   mechanism. Never print, log, commit or place passwords or tokens in example arguments. Do not copy credentials into
   prompts, agent files or reports. Treat a 401, a missing known session or a mismatch as a stop, not a reason to fall
   back to another server.

For example, the user's `opencode-work` shell function selects an explicit server, separate `XDG_DATA_HOME` and
authentication. Read its current definition rather than assuming it is available as a command or hard-coding its port.
In this user's setup it is defined in `~/.zshrc`; `zsh -ic 'typeset -f opencode-work'` shows the function without
executing it. Inspect the related configuration for the server URL and authentication setup, without printing secrets.
`@opencode/client`'s `Service.discover()` discovers a registered managed service; it does not identify an unrelated
explicit server merely because that server owns the current session.

Once the connection and authentication are set up in the shell, the following uses an explicitly verified URL. The
variables are placeholders, not default values:

```sh
opencode api get /api/info --server "$OPENCODE_SERVER"
opencode api get "/api/session/$KNOWN_SESSION_ID" --server "$OPENCODE_SERVER"
```

## Start in the right folder

First ensure no other session is running or blocked on input for the same persistent agent. Use the agent path from the
coordinator's role or the user's explicit instructions. Identify a suitable existing session before creating another;
do not adopt or interrupt somebody else's active session without authorization. The role and `AGENTS.md` in the agent
folder must be present. Its first prompt must run there so it loads the correct instructions and performs its boot.

**Independent session:** `POST /api/session` with `location.directory` set to the absolute agent folder, then verify the
returned `location.directory` before prompting. This is the simplest option when linked-child behavior is unnecessary.
Save the returned session ID so the same session can be resumed and observed.

```sh
opencode api post /api/session \
  --data "$(jq -n --arg dir "$AGENT_DIR" '{location: {directory: $dir}}')" \
  --server "$OPENCODE_SERVER"
```

**Linked child:** `POST /api/session` with `parentID` creates the child at the parent's location, even if a different
location is requested. Before the child's first prompt, call `POST /api/session/{childID}/move` with
`{"directory": "<absolute-agent-folder>"}`; then retrieve the child and verify its location before prompting. If the
move or verification fails, stop. A tested idle, unprompted child loaded the destination instructions; this does not
prove every agent configuration or server version will behave identically. Check that the intended `AGENTS.md` and role
are used. Moving after a session has already run retains its history and instruction state; do not repurpose it as a
clean persistent-agent identity.

With `PARENT_ID` and `AGENT_DIR` set, create and move an unprompted child as follows. Extract the returned `data.id` as
`CHILD_ID`, and inspect the final response before sending any prompt:

```sh
opencode api post /api/session \
  --data "$(jq -n --arg parent "$PARENT_ID" '{parentID: $parent}')" \
  --server "$OPENCODE_SERVER"
opencode api post "/api/session/$CHILD_ID/move" \
  --data "$(jq -n --arg dir "$AGENT_DIR" '{directory: $dir}')" \
  --server "$OPENCODE_SERVER"
opencode api get "/api/session/$CHILD_ID" --server "$OPENCODE_SERVER"
```

Native subagent tool calls and manually API-linked sessions are not interchangeable. OpenCode documents automatic
reports for native subagent calls; do not assume a manually linked child's report automatically wakes its parent. In a
test, a manually linked child's completion did not add a report to an idle parent's transcript. Process its durable
inbox report explicitly.

## Wake, observe and follow up

After the file is in the inbox and session identity is verified, send `POST /api/session/{sessionID}/prompt` with a
short wake-up such as `{"text":"Process your inbox according to your role and instructions."}`. Alternatively, an
authorized coordinator may send a direct assignment with its own identity and scope. The API admits the
input asynchronously; a successful response is not proof the work completed. Reuse an idle session when appropriate;
if an authorized session is already running, do not start a second worker for that agent. Queue a follow-up only when
it is genuinely needed, using `delivery: "queue"`; do not repeatedly queue the same wake-up for an unchanged blocker.

```sh
opencode api post "/api/session/$AGENT_SESSION_ID/prompt" \
  --data '{"text":"Process your inbox according to your role and instructions."}' \
  --server "$OPENCODE_SERVER"
```

Inspect the session, its messages and pending permissions through `GET /api/session/{sessionID}`,
`GET /api/session/{sessionID}/message`, `GET /api/session/{sessionID}/inbox` and
`GET /api/session/{sessionID}/permission`. `POST /api/experimental/session/{sessionID}/wait` waits for idle, but can
remain blocked while the session needs permission or user input. Monitor for those conditions separately. An idle
session may have failed or be waiting on an inbox decision; check its outcome and the agent's durable report before
deciding what happens next. Wake the coordinator when a report or decision request arrives; let it decide or escalate.
When the coordinator itself started the workers and remains active, it can monitor them, process incoming reports and
send follow-ups within its authority instead of having the user relay each message. If the coordinator goes idle, it
will need a later wake-up; API-linked sessions do not themselves provide a scheduler.

Do not auto-approve permission requests or answer user decisions on the user's behalf. Surface them to the user unless
the user has explicitly authorized a narrower policy. In a test, rejecting a permission request prevented the command and
allowed a queued follow-up to run. Pre-approval of a brief does not change tool permissions.

For an automated runner, serialize by agent identity, remember delivered message IDs and session IDs, and reconcile
inboxes, session state and pending permissions after restarts. Do not infer completion from a notification alone or
repeatedly retry a blocked or failed task. OpenCode event subscriptions are live-only, with no replay or automatic
reconnection; use them as wake-up hints and reconcile durable state on reconnect. These are runner requirements, not
features provided by this skill.

## Session length

Use the configured MCP `context_status` for the calling session and `list_agents` for members. It reports the latest
completed model call's input usage, including cached input, not cumulative session tokens. At 150,000 tokens inform the
user or coordinator; at 300,000 warn and recommend a fresh session at the next safe boundary. Do not repeatedly announce
the same threshold without a new crossing. A missing measurement is unknown, not zero. These are advisory signals, not
automatic interrupts or compaction. Check at milestones and before reuse; an MCP tool cannot notify an idle caller by
itself. OpenCode may compact automatically, but compaction is lossy and does not replace a durable checkpoint.

For a completed engineering assignment, checkpoint and prefer a new session for the next distinct assignment. A small
related follow-up can stay in the current session. A coordinator can keep several assignments in flight, then checkpoint
at a coherent milestone: agent names, session IDs, current assignments, decisions, artifacts, pending messages and next
actions. Never abandon pending permissions or input, or start a second worker, to reduce context.
