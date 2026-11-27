# Injected external factors

## The rule

Domain code is a functional core
wrapped in an imperative shell.

- **Functional core.** Domain logic takes values and returns values.
  It does not read the clock,
  generate randomness or IDs,
  read configuration or the environment,
  or perform I/O.
  Whatever it needs from the outside world is a parameter:
  `issue(invoice, now)` takes the time,
  it does not fetch it.
- **Imperative shell.** Thin code around the core
  that gathers inputs, calls the core,
  and persists or sends the results.
  In a domain module this is the use case
  (see `module-layout.md`).
  The shell gets the outside world through injected protocols,
  never by calling it directly.
- **Ports.**
  Each external factor has a protocol:
  `Clock`, `Rng`,
  `IdGenerator`, repositories,
  gateways for external services,
  typed settings.
- **Choose test dependencies for the contract.** Prefer fakes for factors
  such as time or remote services when they make tests deterministic and fast.
  When a fake is useful,
  the module that defines the port also defines and exports it
  in `fakes.py` next to `ports.py`.
  Reuse it rather than writing a new fake in each test.
  Do not patch to replace dependencies.
  An isolated real adapter is preferable when its behavior is part of the contract
  and it is fast and reliable enough for the check command.
  A port does not need a fake merely because it exists.
  Keep tests independent of shared state, network services, and execution order;
  give each test its own isolated resources and clean them up.
  When both a fake and a real adapter implement the same contract,
  run shared contract tests against both to catch drift.
- **Adapters.** Real implementations (`SystemClock`,
  `JsonFileInvoiceRepository`)
  live in `infrastructure/` of the module that owns the port.
  A small port module like `clock` may keep port, fake,
  and real implementation together in one file,
  `clock.py`, with its own ignore.
- **Composition root only.** Only the composition root constructs real implementations
  and passes them in.
  No default argument constructs one:
  `clock: Clock = SystemClock()` is banned,
  as is `clock: Clock | None = None` followed by a fallback
  to the real one.
- **Configuration.** The composition root reads the environment once,
  into a typed settings object,
  and passes values or the object in.
  Nothing else reads `os.environ`.

### Domain IDs are values, not generation formats

Opaque domain IDs are string-backed,
frozen value objects owned by their domain concept:

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class InvoiceId:
    value: str
```

Do not use `NewType` for a domain ID:
it distinguishes types statically
but returns the underlying string at runtime,
with no `.value` or validation hook.
Frozen dataclasses
provide value equality and hashing,
and different ID classes stay distinct
even when their strings match.

Generation and representation are separate decisions.
The ID adapter may use UUIDs,
but returns a string;
the use case wraps it in `InvoiceId`
before calling the domain.
Domain code neither generates IDs nor imports `uuid`.
This is a representation policy,
not a claim that a supplied `UUID` value is impure.
A business requirement for UUID semantics
needs an explicit exception
and a reason in the check configuration.

Add only established validation rules.
The wrapper provides a home for validation later;
it does not justify inventing blank checks,
length limits, or whitespace trimming now.
Normalization changes identity.
Unwrap `.value` when formatting output,
serializing, or translating between contexts.
Adapters wrap strings when loading;
the persisted representation need not change.

The direct calls this rule
keeps out of domain code and shells:

| Factor | Direct call | Injected through |
|---|---|---|
| Time | `datetime.now()`, `date.today()`, `time.time()`, `time.monotonic()` | `Clock` |
| Waiting | `time.sleep()`, `asyncio.sleep()` with a computed delay | `Clock` or `Sleeper` |
| Randomness | `random.*`, `secrets.*` | `Rng` |
| IDs | `uuid.uuid4()`, `uuid.uuid1()`, ID libraries | `IdGenerator` |
| Configuration | `os.environ`, `os.getenv` | settings object |
| Files | `open()`, `Path.read_*`, `Path.write_*` | repository or store |
| Network | HTTP clients, SDK clients | gateway protocol |
| Database | sessions, connections, queries | repository, unit of work |

## Why

A function that calls `datetime.now()` gives a different answer every time.
An agent cannot reproduce a failure,
cannot write an exact assertion,
and reaches for `mock.patch`,
which couples the test to the implementation's import paths.
With the factor injected,
every test is a plain function call
with exact inputs and outputs,
and the signature shows what the code depends on
before anyone reads the body.

A pure core
is also what an agent can change most safely:
no hidden state, nothing to set up,
and the type checker sees every input.
Fakes next to the port give tests one reusable implementation
instead of a slightly different hand-rolled stub in every test file.
Some behavior cannot be established by a fake alone:
an isolated SQLite database can exercise real transactions,
foreign keys, and rollback in repository and use-case tests.
Use a file-backed database when reopening, connection lifetimes,
or file behavior matters.
An in-memory fake would need to reproduce those guarantees
and could silently diverge from the real adapter.
Keep injected ports and test the pure domain separately;
using SQLite in a test does not make domain code depend on it.

Default arguments are banned
because they turn the explicit path
into the long way round.
Once `clock: Clock = SystemClock()` exists,
callers stop passing a clock,
and the dependency disappears from every call site.

## Example

The clock module owns the port,
the real implementation,
and the fake:

```python
# acme/clock.py
from datetime import UTC, datetime, timedelta
from typing import Protocol

__all__ = ["Clock", "FakeClock", "SystemClock"]


class Clock(Protocol):
    def now(self) -> datetime: ...


class SystemClock:
    def now(self) -> datetime:
        return datetime.now(UTC)  # the one place allowed to read the real time


class FakeClock:
    def __init__(self, start: datetime) -> None:
        self._now = start

    def now(self) -> datetime:
        return self._now

    def advance(self, by: timedelta) -> None:
        self._now += by
```

Bad:

```python
def issue(invoice: Invoice) -> Invoice:
    return replace(invoice, status=InvoiceStatus.ISSUED, issued_at=datetime.now(UTC))


def issue_invoice(invoices: InvoiceRepository, clock: Clock = SystemClock()) -> Invoice: ...
```

Good:

```python
def issue(invoice: Invoice, now: datetime) -> Invoice:  # core: time is a value
    return replace(invoice, status=InvoiceStatus.ISSUED, issued_at=now)


# shell: a use case, factors are injected, no defaults
def issue_invoice(invoices: InvoiceRepository, clock: Clock, invoice_id: InvoiceId) -> Invoice:
    invoice = issue(invoices.get(invoice_id), now=clock.now())
    invoices.add(invoice)
    return invoice


def test_issue_sets_issued_at() -> None:
    invoices = InMemoryInvoiceRepository()
    invoices.add(draft(InvoiceId("inv_01"), "cus_01", line_items))
    issued = issue_invoice(invoices, FakeClock(datetime(2026, 1, 1, tzinfo=UTC)), InvoiceId("inv_01"))
    ...
```

## Codify it

ruff, configured in `pyproject.toml`.
  `TID251` bans the direct calls
with a message that names the port to use.
  `B008` bans calls in default arguments,
  which catches `clock: Clock = SystemClock()`:

```toml
[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "DTZ", "TID251"]

[tool.ruff.lint.flake8-tidy-imports.banned-api]
"datetime.datetime.now".msg = "Inject a Clock (acme.clock) and call clock.now()."
"datetime.date.today".msg = "Inject a Clock (acme.clock) and use clock.now().date()."
"time.time".msg = "Inject a Clock (acme.clock) and call clock.now()."
"time.sleep".msg = "Inject a Clock or Sleeper port so tests do not wait."
"random".msg = "Inject an Rng port and pass it in."
"uuid.uuid4".msg = "Inject an IdGenerator (acme.ids) and call ids.new_id()."
"os.environ".msg = "Read configuration in the composition root and pass a settings object in."
"unittest.mock.patch".msg = "Inject a fake or isolated real adapter instead of patching."

# The only places that may touch the real world. Every entry says why.
[tool.ruff.lint.per-file-ignores]
"src/acme/clock.py" = ["TID251"]  # SystemClock reads the real time
"src/acme/ids.py" = ["TID251"]    # UuidIdGenerator generates real UUIDs
"src/acme/*/infrastructure/*.py" = ["TID251"]  # adapters implement ports against the real world
```

ruff's `banned-api`
does not catch the `open` builtin,
  so semgrep covers file I/O:

```yaml
- id: io-outside-adapter
  languages: [python]
  severity: ERROR
  message: >-
    Direct file I/O outside an adapter. Define a port (a Protocol) in the
    use case's ports.py, implement it in the module's infrastructure/, and
    pass it in. Tests inject a fake or isolated real adapter.
  pattern-either:
    - pattern: open(...)
    - pattern: $PATH.read_text(...)
    - pattern: $PATH.write_text(...)
  paths:
    include: ["/src/"]
    exclude: ["**/infrastructure/**"]
```

Add the HTTP and database clients your project uses
to `banned-api`
the same way (for example `"httpx".msg = ...`),
with an ignore for their adapters.

For ID representation,
enable external-package analysis
in import-linter
and add a forbidden contract from package domain layers
and each single-file domain module to `uuid`
(see the example project's `pyproject.toml`, which lists `acme.customers` explicitly).
Add new single-file domain modules to that contract.
Single-file port modules
containing a real ID adapter,
such as `ids.py`,
may still import `uuid`.

The example's `semgrep.yml` rejects `NewType` definitions
whose names end in `Id` outside adapters,
including in single-file modules.
Other uses of `NewType` remain allowed.
Review the remaining details,
such as whether a dataclass is frozen
and its value is a string, by hand.

## Review by hand

- For each new core function:
  given the same arguments,
  does it always return the same result
  and touch nothing else?
  The checks catch known calls,
  not a new library that reads the clock.
- For each port:
  do tests use a deterministic fake or a suitably isolated real adapter?
  If both exist, do shared contract tests keep them aligned?
  Does a real-adapter test cover the behavior a fake cannot establish?
- Is each opaque domain ID a string-backed, frozen value object?
  Does its validation enforce established rules rather than assumptions?
  Outside the value object's own behavior,
  are primitives unwrapped only for formatting,
  serialization, or translation?
- Is there a `port: Port | None = None` with a fallback to the real implementation?
  `B008` does not catch it.
