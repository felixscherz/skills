# FastAPI applications

Use these patterns where the project does not already have a suitable convention. The important distinction is
between adapters, use cases, focused domain behavior, and infrastructure, not the directory names. Any layout works that
gives each of them one obvious place (see `../program-design.md`). The default splits by bounded context first and by
layer inside each context, with the same layer names everywhere:

```text
src/<package>/
|-- <context>/             one package per bounded context, named with a glossary term
|   |-- __init__.py        the context's public API; other contexts import only this
|   |-- domain/            decides: values, entities, rules, domain errors. No I/O, no ports
|   |-- usecases/          does: one module per intent, the ports they consume, workflow errors
|   |-- infrastructure/    adapters for the ports: repositories, clients, other contexts
|   `-- api/               FastAPI routers and DTOs for this context
|-- clock/, ids/           small technical modules named for their job, never `shared` or `common`
|-- wiring/                the composition root
`-- app/                   settings, logging, lifecycle, mounting each context's router, error translation
```

A change to one concept then stays in one directory, and import contracts can keep contexts apart (see
`project-tooling/project-tooling.md`). A service with a single context still uses one context package, so a second
context is an added directory rather than a reorganization. A layer may start as a module (`domain.py`) and become a
package when it grows.

## Keep the domain independent

- Express domain concepts with the domain's vocabulary. Use immutable value objects for meaningful IDs and constrained
  values, and plain Python entities and domain functions for business behavior. Keep FastAPI, `Depends`, Pydantic
  transport DTOs, HTTP exceptions, database documents, and framework state out of domain code and use cases.
- The domain decides, the use case does. Domain code answers "is this allowed, and what is the new state?" from
  values it is given: it is synchronous, takes the time and new IDs as arguments, and never loads or saves. A use case
  named for the intent loads through ports, lets the domain decide, saves, and owns the transaction and failure policy.
  Run every rule before the first write, so a failed rule leaves nothing half done. See `../domain-driven-design.md`.
- When a rule needs loaded data (a uniqueness check), the use case loads it and passes it in, or a store constraint
  enforces it and the adapter translates the conflict into a domain error. Do not give the domain a port. A rule over
  several aggregates is a pure domain function taking all of them.
- Convert primitives and DTOs to domain types at input boundaries, and convert domain results to response DTOs at output
  boundaries. Map persistence shapes separately; an HTTP schema or database document need not become the domain model.
- Raise domain or use-case failures without HTTP dependencies. Translate them to status codes and response shapes at the
  HTTP boundary. Keep async I/O async; do not block the event loop.

## Keep the domain pure

The domain module of a context defines no repository and no service that loads or saves. An order context:

```python
# orders/domain.py: decides. No ports, no I/O, no async
@dataclass(frozen=True)
class Order:
    id: OrderId
    lines: tuple[OrderLine, ...]
    status: OrderStatus
    cancelled_at: datetime | None = None

    def cancel(self, now: datetime) -> "Order":
        if self.status is OrderStatus.SHIPPED:
            raise OrderAlreadyShipped(self.id)
        return replace(self, status=OrderStatus.CANCELLED, cancelled_at=now)


def place(order_id: OrderId, lines: tuple[OrderLine, ...]) -> Order:
    if not lines:
        raise EmptyOrder(order_id)
    return Order(id=order_id, lines=lines, status=OrderStatus.PLACED)


# orders/usecases/ports.py: what the use cases need from the outside
class OrderRepository(Protocol):
    async def get(self, order_id: OrderId) -> Order: ...
    async def save(self, order: Order) -> None: ...


# orders/usecases/cancel_order.py: does. Load, let the domain decide, save
class CancelOrder:
    def __init__(self, orders: OrderRepository, clock: Clock) -> None:
        self._orders = orders
        self._clock = clock

    async def execute(self, order_id: OrderId) -> Order:
        order = await self._orders.get(order_id)
        cancelled = order.cancel(now=self._clock.now())
        await self._orders.save(cancelled)
        return cancelled


# orders/infrastructure/sql_orders.py implements OrderRepository on the database.
```

- Pure does not mean only functions. Methods on entities (`order.cancel(now)`) are often the most readable form. What
  makes code domain code is no I/O, and the time and new IDs arriving as arguments. Prefer returning a new frozen
  entity; a method that mutates `self` is still domain code, but harder to test and reason about.
- There is no `OrderService` holding a repository. Such a class decides and does in one place. Its loading and saving
  move into use cases, its rules onto the entity or into domain functions.
- A domain service is a pure function over several aggregates that neither can decide alone, such as
  `allocate(order, stock) -> tuple[Order, Stock]`. It lives in the domain, takes both, and loads nothing.
- When a rule needs data, the use case loads it. For "at most five open orders per customer", the use case calls
  `orders.count_open(customer_id)` and passes the count into `place(..., open_orders=count)`; the domain checks the
  number.
- Domain tests need no fakes: build an `Order`, call `cancel`, assert. Only use-case tests need
  `InMemoryOrderRepository` and a fake clock.

## Inject ports through narrow Protocols

Define each port in the `usecases/` of the context that consumes it, with only the operations that consumer needs. Type
constructors against those ports rather than concrete repositories, other full-service interfaces, or HTTP clients. A
port can represent a repository, an external lookup, an event publisher, or a callable operation. The application
container supplies concrete implementations.

```python
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class BookingId:
    value: str


class InvalidGuestError(Exception): ...


@dataclass(frozen=True)
class GuestName:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise InvalidGuestError("Guest name is required")


@dataclass(frozen=True)
class Booking:
    id: BookingId
    guest: GuestName


class BookingRepository(Protocol):
    async def save(self, booking: Booking) -> None: ...


class ReserveBookingId(Protocol):
    async def __call__(self) -> BookingId: ...


def book(booking_id: BookingId, guest: GuestName) -> Booking:
    return Booking(id=booking_id, guest=guest)


class CreateBooking:
    def __init__(self, repository: BookingRepository, reserve_id: ReserveBookingId) -> None:
        self._repository = repository
        self._reserve_id = reserve_id

    async def execute(self, guest: GuestName) -> Booking:
        booking = book(await self._reserve_id(), guest)
        await self._repository.save(booking)
        return booking
```

Use real implementations at runtime and fakes in use-case tests (see `../test-behavior.md`). Protocols describe capabilities; they
do not require inheritance or a general-purpose DI framework. If a workflow spans several writes or external effects,
decide what commits together and what happens on partial failure before moving it. Extraction alone does not make a
workflow atomic.

## Own the transaction in the use case

A use case that writes more than once takes a unit of work instead of repositories. The protocol lives in the
context's `usecases/`, lists only the repositories that commit together, and rolls back unless committed.
Infrastructure implements it on a database session; wiring passes a factory, so every `execute` gets a fresh
transaction.

```python
class BookingsUnitOfWork(Protocol):
    @property
    def bookings(self) -> BookingRepository: ...
    @property
    def rooms(self) -> RoomRepository: ...

    async def __aenter__(self) -> Self: ...
    async def __aexit__(self, *exc: object) -> None: ...  # rolls back unless committed
    async def commit(self) -> None: ...


class ReserveRoom:
    def __init__(self, uow: Callable[[], BookingsUnitOfWork], reserve_id: ReserveBookingId) -> None:
        self._uow = uow
        self._reserve_id = reserve_id

    async def execute(self, room_id: RoomId, guest: GuestName) -> Booking:
        async with self._uow() as uow:
            room = await uow.rooms.get(room_id)
            booking, occupied = reserve(room, await self._reserve_id(), guest)  # decide
            await uow.bookings.save(booking)  # do
            await uow.rooms.save(occupied)
            await uow.commit()
        return booking
```

## Cross contexts through ports the reader owns

A use case may need data or behavior from another context. It does not import that context. Its own context defines a
port in its own words, and an adapter in its `infrastructure/` implements the port by calling the other context's public
API and translating the result. That adapter is the only file that imports the other context; list the import in the
contract's `ignore_imports` with a comment, so every link between contexts is visible in one place.

```python
# billing/usecases/ports.py: billing's view of bookings, only what billing needs
@dataclass(frozen=True)
class StayToBill:
    booking_id: BookingRef
    nights: int


class Stays(Protocol):
    async def get(self, booking_id: BookingRef) -> StayToBill: ...


# billing/infrastructure/bookings_stays.py: the one file in billing that imports bookings
from service.bookings import FindBooking


class BookingsStays:
    def __init__(self, find_booking: FindBooking) -> None:
        self._find_booking = find_booking

    async def get(self, booking_id: BookingRef) -> StayToBill:
        booking = await self._find_booking.execute(BookingId(booking_id.value))
        return StayToBill(booking_id=booking_id, nights=booking.nights)
```

- Keep each pair of contexts one-directional. If billing reads from bookings, bookings reacts to billing through events,
  not a port back. Calls in both directions mean the boundary is in the wrong place.
- Do not stretch one transaction over two contexts. The context that owns the intent commits its change and records an
  event (an outbox table makes this reliable), and the other context reacts in its own transaction. Only when two
  contexts share a store and must change all or nothing does a coordinating use case above both, in its own top-level
  package, own one unit of work over both. Needing that often means the contexts should merge.
- A process that spans time (approvals, retries) is a use case triggered by events, with its own persisted state. Its
  rules stay in the domain, for example `next_step(state, event) -> Command`.

## Make HTTP handlers adapters

Each context's `api/` holds its router, request and response DTOs, and providers; `app/` mounts every router and
registers the error translation. Routes never import `infrastructure/`. Use `Annotated[UseCase, Depends(provider)]` for
a handler implementing a use case. The provider obtains it from the application container rather than constructing
repositories or workflows per request. Keep handlers focused on parsing, domain conversion, invoking one use case, error
translation, and response mapping. Two routes for the same intent can call the same use case with different domain
inputs; neither route should coordinate several services. Existing simple operations need not be wrapped solely to
satisfy a naming convention.

```python
from typing import Annotated, cast

from fastapi import APIRouter, Depends, FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Import CreateBooking, GuestName, InvalidGuestError, and Container from their respective modules.
router = APIRouter(prefix="/bookings")


class CreateBookingRequest(BaseModel):
    guest: str


class BookingResponse(BaseModel):
    id: str
    guest: str


def get_container(request: Request) -> Container:
    return cast(Container, request.app.state.container)


def get_create_booking(container: Annotated[Container, Depends(get_container)]) -> CreateBooking:
    return container.create_booking


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_booking(
    request: CreateBookingRequest,
    create_booking: Annotated[CreateBooking, Depends(get_create_booking)],
) -> BookingResponse:
    booking = await create_booking.execute(GuestName(request.guest))
    return BookingResponse(id=booking.id.value, guest=booking.guest.value)


async def invalid_guest(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"code": "invalid_guest", "message": str(exc)},
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(InvalidGuestError, invalid_guest)
```

Register error translation once at the application boundary rather than catching domain errors in each route, so every
route maps the same failure to the same status and a stable error shape. Expected domain failures need no stack trace;
unexpected ones return a generic 500 and are logged once at the boundary.

For route tests, override `get_create_booking` through `app.dependency_overrides` and check the HTTP contract without
starting real infrastructure. Test the use case through `execute()` with fakes for its ports. Test focused domain
behavior without involving FastAPI.

## Compose once at the application boundary

Keep construction in a single composition root, for example a `Container` with `@cached_property` providers for shared
settings, clients, repositories, services, and use cases. Providers make the dependency graph explicit. Share a
container per app/process, not per request; do not use process-scoped instances for mutable request-specific state. Use
local imports in providers only when needed to break import cycles.

Construct the container at bootstrap (or in the app factory), attach it to `app.state`, and use FastAPI lifespan for
starting and stopping resources such as database clients, message consumers, and background work. Non-HTTP entry points
use the same composition root directly, not FastAPI dependency resolution. Allow a container to be supplied to the app
factory in tests. Keep FastAPI `Depends` and `Request` out of the container, use cases, and services.

```python
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from functools import cached_property

from fastapi import FastAPI


class Container:
    def __init__(self, database: Database) -> None:
        self.database = database

    @cached_property
    def booking_repository(self) -> BookingRepository:
        return SqlBookingRepository(self.database)

    @cached_property
    def reserve_booking_id(self) -> ReserveBookingId:
        return DatabaseBookingIdReserver(self.database)

    @cached_property
    def create_booking(self) -> CreateBooking:
        return CreateBooking(self.booking_repository, self.reserve_booking_id)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    container: Container = app.state.container
    await container.database.connect()
    try:
        yield
    finally:
        await container.database.close()


def create_app(container: Container) -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.state.container = container
    register_exception_handlers(app)
    app.include_router(router)
    return app
```

The infrastructure adapter classes in this sketch are application-specific; construct `Container` with configured
infrastructure at startup. Cache long-lived dependencies deliberately; manage request/transaction-scoped dependencies
separately. Check the existing project's OpenAPI contract and test conventions when changing routes or DTOs.
