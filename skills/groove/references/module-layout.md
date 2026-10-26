# Module layout

## The rule

The source root is split by domain first, then by layer. Each top-level
package or file is a module named with a glossary term (`invoicing`,
`customers`), or a small technical module named for its job (`clock`,
`ids`). A module starts as a single file and becomes a package with layers
when it grows. Inside every package module, the layers have the same names.
A module has only the layers it needs, and a missing layer says nothing
else about it:

```text
src/acme/
|-- clock.py, ids.py      port modules: port, fake, real implementation
|-- customers.py          a single-file module: values, rules, ports, fakes
|-- invoicing/            a package module
|   |-- __init__.py       public API
|   |-- README.md
|   |-- domain/           decides: values, entities, rules, domain errors
|   |-- usecases/         does: one file per intent, the ports they consume, fakes
|   `-- infrastructure/   adapters for the ports, persisted record shapes
|-- checkout/             owns a workflow: usecases/, no rules of its own yet
`-- composition.py        composition root (top layer)
```

- **A small module is one file.** `customers.py` holds its values, rules,
  ports, fakes, and use cases, with its public API in `__all__` and its
  responsibility in the docstring instead of a README. Keep the file in
  the order decide, then ports and fakes, then do, so the split is a cut,
  not a rewrite.
- **It becomes a package when it needs an adapter or an entry point.** Only
  `infrastructure/` may touch the real world, so the first adapter forces
  the split. Split earlier when the file no longer reads in one go, at a
  few hundred lines. Splitting means: move each part to its layer, turn
  `__all__` into `__init__.py`, the docstring into a README, and add the
  module to the contracts (see Codify it).
- **The rules below hold in a single file too.** Domain functions stay
  pure and take the time and IDs as arguments, ports and fakes still come
  in pairs, and use cases still decide first, then do. Only the checks
  differ: no contract sees the layers inside one file.

- **The domain decides.** It answers "is this allowed, and what is the new
  state?" from values it is given. It does no I/O, defines no ports, and
  imports nothing from `usecases/` or `infrastructure/`. The time and new IDs
  arrive as arguments.
- **Pure does not mean only functions.** A method on an entity
  (`invoice.issue(now)`) is domain code as long as it does no I/O. Prefer
  returning a new frozen value over mutating `self`.
- **No `<Concept>Service` holding a repository.** A class like
  `InvoicingService(invoices, clock)` decides and does in one place. Its
  loading and saving belong in use cases, its rules on the entity or in
  domain functions. Domain tests then need no fakes at all.
- **Use cases do.** A use case is named after one intent (`issue_invoice`).
  It loads through ports, lets the domain decide, saves, and owns the
  transaction boundary. Ports live in `usecases/ports.py`, because use cases
  are what consume them, and their fakes in `usecases/fakes.py`. A use case
  does not call another use case.
- **Decide first, then do.** Inside a use case, run every rule on loaded
  values before the first write. A rule that fails then fails before
  anything changed.
- **Infrastructure implements ports** against the real world: files,
  databases, HTTP, other modules. It is the only layer that may touch them.
- **A unit of work when a use case writes more than once.** Its protocol
  lives in the `usecases/ports.py` of the module whose use case needs it, and
  lists only the repositories that must commit together. One use case is one
  unit of work.
- **A layer may start as a file.** In a package module, `domain.py`
  becomes `domain/` when it grows. The contracts treat both the same.
- **Entry points are a layer too.** HTTP routes, CLI commands, or message
  handlers for a module go in its `api/` (or `cli/`), above `usecases/`. They
  never import `infrastructure/`; the composition root hands them use cases.
- **The composition root is global.** One top-level module (`composition`) builds
  every adapter and use case. The application's CLI may handle process
  startup separately; together they form the composition root. Read
  configuration once along that startup path and pass it into assembly
  rather than reading it again in the app factory. Only the composition
  root imports a module's `infrastructure/` and entry points from outside
  that module; they are not exported from `__init__.py`. List each part of
  the composition root by name in the contracts (see
  `architecture-boundaries.md` and `application-cli.md`).
- **Moving API models can rename generated schemas.** FastAPI and Pydantic
  name an OpenAPI component after its class, prefixed with the module path
  when two classes share a name, so moving a DTO into `api/` can rename the
  component. A rename alone, with fields, types, and requiredness unchanged,
  does not block the move: regenerate the schema and mention the rename in
  the pull request.

Some logic sits on a boundary. Two cases come up often:

- **A rule needs loaded data** ("at most five open Invoices per Customer").
  The use case loads it and passes it in
  (`draft(..., open_invoices=invoices.count_open(customer_id))`), and the
  domain checks the number. If the data is too large, let a store
  constraint enforce the rule and translate the conflict into a domain
  error. Do not give the domain a port.
- **A rule spans several aggregates** of one module. A pure domain function
  takes all of them (`allocate(order, stock)`). It decides and does no I/O,
  so it stays in the domain.

## Why

Most changes touch one domain concept through every layer: a rule, the use
case that applies it, the adapter that stores it. When the top level is
split by layer, that change is scattered over four directories, and nothing
stops one domain's code from leaning on another's internals. Split by domain
first, a change stays in one directory, and the module boundary is checked.

Inside the module, fixed layer names give every piece of code exactly one
home. An agent asking "where does this go?" answers it with one question:
does this code decide, do, or talk to the outside world? The answer is also
what makes it testable: domain tests need no fakes at all, use-case tests
need only the fakes next to the ports.

Splitting decide from do is where codebases most often blur. A domain
service that validates and then saves looks harmless with one step. Once a
workflow needs a commit, a second aggregate, or an event, the service grows
orchestration, or the steps end up split across layers. Keeping I/O out of
the domain from the start avoids that choice.

## Example

Bad, a domain service that decides and does:

```python
# acme/invoicing/domain/service.py
class InvoicingService:
    def issue(self, invoice_id: InvoiceId) -> Invoice:
        invoice = self.invoices.get(invoice_id)  # I/O in the domain
        if invoice.status is InvoiceStatus.ISSUED:
            raise InvoiceAlreadyIssued(invoice.id)
        issued = replace(invoice, status=InvoiceStatus.ISSUED, issued_at=self.clock.now())
        self.invoices.add(issued)
        return issued
```

Good (`templates/example-project/src/acme/invoicing/`):

```python
# acme/invoicing/domain/model.py: decides
def issue(invoice: Invoice, now: datetime) -> Invoice:
    if invoice.status is InvoiceStatus.ISSUED:
        raise InvoiceAlreadyIssued(invoice.id)
    if not invoice.line_items:
        raise EmptyInvoice(invoice.id)
    return replace(invoice, status=InvoiceStatus.ISSUED, issued_at=now)


# acme/invoicing/usecases/issue_invoice.py: does
def issue_invoice(invoices: InvoiceRepository, clock: Clock, invoice_id: InvoiceId) -> Invoice:
    invoice = issue(invoices.get(invoice_id), now=clock.now())
    invoices.add(invoice)
    return invoice
```

## Codify it

import-linter, configured in `pyproject.toml`. One `layers` contract with
`containers` applies the same layering inside every package module.
Parentheses mark a layer as optional, since `checkout` has no domain.
Single-file modules are not listed: they have no layers inside.

```toml
[[tool.importlinter.contracts]]
name = "Inside every module, infrastructure -> usecases -> domain"
type = "layers"
containers = ["acme.checkout", "acme.invoicing"]
layers = ["(infrastructure)", "(usecases)", "(domain)"]
broken_contract_guidance = """
domain decides: pure rules on values, no ports. usecases do: load through ports, call the \
domain, save, commit. infrastructure implements the ports against the real world. Move the \
code to the layer that matches what it does. A module that becomes a package is added to \
containers here."""

[[tool.importlinter.contracts]]
name = "The domain gets time and IDs as values"
type = "forbidden"
source_modules = ["acme.*.domain"]
forbidden_modules = ["acme.clock", "acme.ids"]
broken_contract_guidance = """
Domain code takes the time and new IDs as arguments. Call clock.now() or ids.new_id() in \
the use case and pass the value in."""
```

The ruff `TID251` ignore and the semgrep I/O exclusion point at
`*/infrastructure/`, so only adapters may touch the real world (see
`injected-external-factors.md`). That is also what keeps a single-file
module honest: the first `open()` or `datetime.now()` in it fails the check,
and the fix is to split it. In an async codebase, forbid
`acme.*.domain` from importing `asyncio` and the HTTP and database clients:
domain code that needs to await is doing I/O.

## Review by hand

- Does every new domain function return the same result for the same
  arguments, and touch nothing else? The contracts catch imports, not a port
  passed in as an argument.
- Does a use case run all its rules before its first write?
- Did a use case start writing twice without a unit of work?
- Did you add a module? Add it to the layers contract between modules. If
  it is a package, also add it to `containers` here and give it a
  `protected` contract.
- In a single-file module, does each new function either decide or do, and
  does a domain function take the time and IDs as arguments? No contract
  sees inside the file.
- Did a single-file module grow past what reads in one go? Split it.
