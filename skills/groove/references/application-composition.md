# Application composition and lifecycle

## The rule

Composition builds the application's dependency graph.
Lifecycle starts, supervises, and stops its long-lived work.
They are related, but need not be the same object
or be owned by an HTTP framework.

- **Compose explicitly.** Construct a shared dependency once per intended scope
  and pass that same instance to its consumers.
  A process, request, transaction, and child process
  can have different scopes.
  Importing a module must not start the application or create its runtime graph.
  Constructors should not secretly start background work;
  make resource acquisition and startup explicit.
- **Treat FastAPI as an adapter.** It translates HTTP into application calls;
  it does not define the application or own its behavior.
  An HTTP route, message consumer, or CLI command
  calls application behavior with dependencies supplied by the composition root.
  FastAPI's `Depends` resolves HTTP inputs and retrieves already-composed dependencies;
  it is not the dependency system for a worker or the domain.
  The app factory accepts its dependencies,
  mounts routes and middleware,
  and does not silently create a second service.
- **One lifecycle owner per resource.** FastAPI lifespan can manage
  HTTP-owned resources and a worker when their lifecycle needs fit.
  If liveness must be served while startup is blocked,
  or a worker and server need independent supervision,
  a process runner can supervise them separately.
  The HTTP app can still own HTTP-specific resources.
  Do not start or stop the same resource from both owners.
- **Supervise the job.** Start prerequisites before accepting work.
  When readiness is exposed,
  keep it down until the service can accept work
  and withdraw it on shutdown.
  Unexpected startup or server failure must reach the process owner;
  choose an explicit restart or exit policy for background tasks.
  A startup flag does not establish ongoing health.
  Track partial acquisition, stop accepting work before dependencies,
  and bound and report shutdown.
  See `../../engineering/references/lifecycle-hygiene.md`
  when the engineering skill is available.
- **Process boundaries are real.** A cached object is shared only within its process.
  Decide which processes or workers should run consumers,
  create process-local clients and telemetry where required,
  and preserve the deployment's worker and signal semantics.
  Do not assume objects, threads, or connections survive a spawn or fork safely.

## Why

An import-time singleton hides both construction and ownership.
Tests cannot supply an isolated application,
and a route may talk to a different instance from the worker.
An HTTP server can be healthy while the actual worker is blocked or dead.
FastAPI lifespan startup normally completes before requests are served,
so making it own a slow worker can also make liveness unreachable.
Separating assembly from lifecycle makes these choices visible
without requiring a DI framework.

## Example

An application that consumes messages as well as serving health:

```text
serve command / process runner
  build one worker and its shared dependencies
  create HTTP app with worker readiness and use cases
  supervise worker startup and HTTP server on the same event loop
  on shutdown: withdraw readiness, stop accepting work, clean up
```

The health route reads the supplied readiness object;
the consumer and route use dependencies from the same composition.
If the service is only HTTP and its startup may block requests,
the simpler app factory plus FastAPI lifespan is enough.
Neither arrangement requires a generic container or a protocol for every object.

## Codify it

Add behavioral tests to the project's check command:

- Import the app factory in a fresh process
  without constructing or starting the runtime.
- Supply test dependencies to each entry point;
  exercise their public interfaces and verify shared identity and isolation
  where the design requires them.
- For a long-running service, hold startup at a controlled gate
  and check that work is not accepted prematurely.
  Where liveness or readiness are exposed,
  check their contracts during and after startup.
  Cover failure, shutdown during partial startup,
  cleanup ordering and a bounded shutdown as applicable.
- Where a process runner is used,
  test it with fakes and exercise the real server and installed command
  in a subprocess for signal handling, bind failure, and exit status.
- When an ASGI lifespan owns resources,
  manage it explicitly in tests;
  an HTTPX ASGI transport does not start it on its own.

Use import-linter to keep domain and use cases independent of FastAPI
and to name composition modules as the permitted importers of adapters
(see `architecture-boundaries.md`).
Import checks cannot prove that two entry points received the same instance
or that shutdown really completed; behavioral tests and review cover those.

## Review by hand

- Which scope owns each dependency, task, and resource?
  Can any be created or started twice,
  especially across worker processes?
- Does HTTP merely expose the application's behavior and health,
  or has it accidentally become the owner of a separate service?
  Is the extra process runner justified by an actual requirement?
- What happens when startup is blocked, fails halfway,
  or races a shutdown request?
  Does readiness describe startup only or ongoing health too?
- Are worker count, deployment configuration, signal handling,
  and old launch paths preserved or deliberately migrated?
