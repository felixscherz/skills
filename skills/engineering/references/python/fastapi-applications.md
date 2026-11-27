# FastAPI applications

Treat FastAPI as an adapter:
it translates HTTP into application calls,
but does not define the application or own its behavior.
Follow an existing project convention where one fits.

## HTTP boundary

- Keep routes focused on HTTP:
  parse and validate input,
  translate it into application values,
  invoke the application behavior,
  and map the result to a response.
  Do not make a route the owner of a business workflow.
- Keep `Request`, `Depends`, HTTP exceptions,
  and transport DTOs out of the domain and use cases.
  Translate application failures to HTTP at the boundary;
  a shared exception handler is useful when several routes need the same mapping.
  Do not leak unexpected errors to clients or log them repeatedly.
- Use FastAPI dependency providers for HTTP inputs
  and to supply the dependencies an endpoint needs.
  They are not the dependency mechanism for the domain or a message consumer.
  A provider can retrieve a supplied object from `app.state`;
  the application itself should not look up dependencies there.
  Scope request-specific state and transactions separately
  from long-lived dependencies.
- Keep async I/O async and avoid blocking the event loop.
  When a workflow spans writes or external effects,
  decide what must be atomic and what happens on partial failure;
  a transaction or unit of work is one option,
  not a requirement for every multi-write operation.
  See `../domain-driven-design.md`.

## Composition and lifecycle

Compose dependencies at the application boundary
and supply them to the HTTP app.
An explicit object, factory, or container can all serve this purpose;
do not add a generic container solely for FastAPI.
An app factory can receive dependencies,
store what its providers need on `app.state`,
and mount routes and middleware.
Non-HTTP entry points receive their dependencies directly,
without FastAPI dependency resolution.
Avoid constructing or starting the application graph on import.

Choose one owner for each resource
and make startup, failure, and shutdown observable:

- FastAPI lifespan is suitable for HTTP-owned resources
  and can also manage a worker when its lifecycle and availability requirements fit.
  The server normally waits for lifespan startup to finish before serving requests.
- If liveness must respond while a worker is still starting,
  or the worker and server need independent supervision,
  a process runner can own and supervise both.
  Pass the same composed dependencies to the app and worker.
  The app may still own its HTTP-specific resources;
  neither owner starts or stops the other's resources.
  Backgrounding startup in lifespan is another possibility,
  but its failure still needs an explicit supervision policy.

For either arrangement,
decide how startup and server failures reach the process owner,
how readiness relates to the work the service can accept,
and how partial startup and shutdown are handled
(`../lifecycle-hygiene.md`).
Do not add a process runner without a requirement for it.

For example, a small HTTP-owned service can use lifespan
without a container:

```python
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Annotated, cast

from fastapi import APIRouter, Depends, FastAPI, Request

# Import Bookings, BookingResponse, and Database from their respective modules.
router = APIRouter()


def get_bookings(request: Request) -> Bookings:
    return cast(Bookings, request.app.state.bookings)


@router.get("/bookings/{booking_id}")
async def read_booking(
    booking_id: str, bookings: Annotated[Bookings, Depends(get_bookings)]
) -> BookingResponse:
    booking = await bookings.find(booking_id)
    return BookingResponse.from_booking(booking)


def create_app(bookings: Bookings, database: Database) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        await database.connect()
        try:
            yield
        finally:
            await database.close()

    app = FastAPI(lifespan=lifespan)
    app.state.bookings = bookings
    app.include_router(router)
    return app
```

The bootstrap supplies `bookings` and `database` from the same composition.
`BookingResponse` is an HTTP DTO;
the application and database implementations are project-specific.
The database's `connect` operation must clean up any partial acquisition on failure.

## Test the boundaries

- Exercise routes as HTTP and verify the response contract.
  Supply application dependencies through the app factory
  or override a FastAPI provider when testing a route in isolation.
  Test application behavior separately through its own API
  (`../test-behavior.md`).
- Where HTTP and a non-HTTP entry point share a dependency,
  exercise both and verify they see the intended state.
  Test separate instances for isolation when the design promises it.
- For long-running work,
  test the startup, failure, and shutdown contracts that apply to the service.
  If health must be served during blocked startup,
  hold startup at a controlled gate and test liveness, readiness,
  and that work cannot enter before its prerequisites are ready.
  A startup-complete flag alone does not prove ongoing health.
  For a supervised server,
  use fakes at the supervisor boundary and process-level tests
  for real bind failures, signals, and exit status as appropriate.
- HTTPX `ASGITransport` does not itself run ASGI lifespan;
  manage lifespan explicitly when the test needs it,
  or start and stop an independently owned runtime separately.
  Starlette's synchronous `TestClient` runs the app on a separate loop,
  so async tests sharing loop-bound resources should use an async client.

## Know how OpenAPI names schemas

FastAPI names each component after its Pydantic class.
When two models share a class name,
both can get the full module path instead
(`psp__testspots__api__classification__Classification`),
so moving a DTO or enum can rename its component and every `$ref` to it.
When validation and serialization schemas differ,
FastAPI can emit separate `Model-Input` and `Model-Output` components;
a change can also make them equal and collapse them into one.

- Before moving models, decide whether component names are part of the contract.
  Generated clients use them as type names,
  so a rename can break consumers even when the wire shape is unchanged.
  Regenerate and review the schema,
  and coordinate any incompatible client change.
- When a name must stay stable,
  a unique class name or a named `TypeAliasType` may help.
  Verify the generated schema for the versions in use;
  an alias does not necessarily carry through generic models.
- Diff the generated schema after moving models
  and check for unintended changes to names, references,
  fields, types, and requiredness.
