# Application CLI

## The rule

A service exposes an installed command named for the application, such as
`acme serve --hostname 127.0.0.1 --port 8000`. Users should not need to know
the ASGI factory import path or invoke `uvicorn` to start it. The server is
an implementation detail, not the application's operational interface.
This applies to runnable services, not libraries with no process to start.

- **Install the command with the application.** Declare it in
  `pyproject.toml` under `[project.scripts]`. A repository-only shell script
  or Make target is not a substitute for the installed command. A tool
  runner such as `uv run --locked acme serve` is fine; it still invokes the
  application's CLI.
- **Own startup configuration.** Parse and validate options before starting
  the server. Provide documented defaults and `--help`. For a web service,
  expose its bind address and port. Choose network exposure according to
  the project's deployment decisions, not the server's incidental defaults.
  Do not mirror every server option without a requirement.
- **Own logging before initialization.** Configure application, server, and
  third-party logging centrally before importing or constructing components
  that may emit startup logs. Default to INFO; `--verbose` enables DEBUG.
  Keep formatting and handler configuration consistent, avoid duplicate
  records, and prevent the server from replacing the application's setup.
  Module loggers do not configure handlers themselves.
- **Keep assembly and business behavior separate.** The CLI bootstrap and
  app factory are parts of the composition root, not competing owners of
  configuration. The bootstrap gathers configuration and starts the server
  through its Python API; assembly constructs dependencies from those
  values. Module-specific commands call their owning module's use cases,
  not adapters or business logic written in the argument parser. See
  `module-layout.md` and `architecture-boundaries.md`.
- **Keep process behavior intact.** Startup failures exit unsuccessfully.
  Preserve graceful signal handling and shutdown cleanup. Do not spawn a
  server subprocess or swallow errors merely to hide its command line.
- **Use the same interface everywhere.** Local instructions, container
  entry points, and service definitions use the application command. A
  user should not need a different launch path to get correct logging.

## Why

`uvicorn acme.composition:create_app --factory` makes internal module names and
server-specific flags part of the user's interface. It also leaves startup
configuration to whoever writes each launch command. One path can enable
application logging while another silently falls back to the server's
format or level.

An application-owned command gives configuration one home. The app can
change its internal factory location or server without making users rewrite
their launch commands. The CLI stays thin; it owns how the process starts,
not what the business does.

## Example

Install the application command:

```toml
[project.scripts]
acme = "acme.cli:main"
```

Document that command, not the server's:

```sh
acme serve --hostname 127.0.0.1 --port 8000
acme serve --verbose
acme serve --help
```

For Uvicorn, configure logging first and pass `log_config=None` when calling
`uvicorn.run(...)` so it does not install its default handlers. Apply the
selected level to the application's logging setup as well; setting only
Uvicorn's `log_level` does not configure application logging.

## Codify it

Add subprocess integration tests to the project's existing check command.
Run the installed console script from a fresh process, not only its parser
or app factory. Verify:

- `--help` succeeds and documents the supported options and defaults.
- Invalid options fail before the server starts, with an actionable error.
- The command serves a real request on the requested interface and port.
  Use an OS-assigned port in tests to avoid collisions, and wait for a
  readiness signal with a timeout rather than sleeping for a fixed delay.
- Default logs exclude DEBUG; `--verbose` enables DEBUG for application and
  server loggers. Records use the configured format without duplicates.
- A termination signal shuts the process down and runs cleanup. Always
  terminate the test process in a `finally` block, even after a failed
  assertion, with a bounded wait and forced termination as a last resort.

Declare the CLI bootstrap and app factory in the import contracts as parts
of the composition root. Domain modules must not depend on the CLI or
server. No new lint tool is needed to test this behavior.

## Review by hand

- Are the flags useful application options, or a copy of the server's API?
- Do the defaults match the project's deployment and security decisions?
- Do README examples and deployment commands use the installed CLI?
- Is configuration read once, and is logging ready before components start?
- Does switching servers require changes only in startup code, not in
  domain modules or the documented command?
