# Architecture boundaries

## The rule

Code is split into modules, each with one responsibility written in its
`README.md`. A module is a top-level package under `src/acme/`, split
internally into layers (see `module-layout.md`).

- **Public API.** A module's public API is what its `__init__.py` exports in
  `__all__`. Everything else in the module is internal.
- **Import only the public API.** Code outside a module imports from
  `acme.invoicing`, never from `acme.invoicing.domain.model`. Tests of other
  modules follow the same rule.
- **Declared dependencies.** The allowed dependencies between modules are
  declared in one place, as import-linter contracts. Adding a dependency that
  is not allowed means changing the contract, on purpose, in the same change.
- **No cycles.** If two modules seem to need each other, one of them holds
  the wrong responsibility, or the shared part is a third module.
- **Reading from a sibling module.** Domain modules in the same layer do not
  import each other, with one narrow exception. When a use case needs
  something from a sibling, its module defines a port in its own terms
  (`CustomerLookup` in invoicing) and implements it in an adapter in its
  `infrastructure/`. That adapter is the only file that imports the sibling,
  through its public API, and it translates the sibling's types into its
  own. The import is listed in `ignore_imports` of the layers contract, so
  every link between siblings is visible in one place.
- **One direction per pair.** If invoicing reads from customers, customers
  does not read from invoicing. Links in both directions mean the boundary
  is in the wrong place: merge the modules or move the responsibility.
- **Changing state in several modules.** A domain module never changes state
  owned by another domain module. When one operation must change state in
  several modules all or nothing, it lives in a coordinating module (a use
  case) one layer up. It depends on all of them and wraps the change in a
  unit of work. This works only while the modules share a store that can
  commit together. When they do not, the owning module commits its own
  change and records an event, and the other module reacts in its own
  transaction.
- **Composition root.** One place builds the application: it constructs
  adapters and wires them into use cases. It sits in the top layer.

## Why

An agent sees only the files it opens. When any file may import any other,
the agent cannot know what a change will break, and will happily import a
private helper from three packages away because it was the nearest match.
Explicit public APIs give each module a small, stable surface to read
instead of its whole body. Declared layers make the architecture something
an agent can read in seconds, and turn a quiet drift into a broken contract
with a message saying what to do.

A port owned by the reader keeps the sibling's model out of the reader's use
cases: a rename in customers breaks one adapter in invoicing, not its rules
or tests, and the use case is tested with a fake instead of a real
customers module. Coordinating modules keep domain modules small and
independent: invoicing does not need to know that checkout exists. The unit
of work keeps consistency in one place instead of scattered try/except
blocks.

## Example

Bad, reaching into internals and changing another module's state:

```python
# acme/invoicing/usecases/issue_invoice.py
from acme.customers.domain.model import Customer  # internal import, sibling module

def issue_and_charge(invoice: Invoice, customer: Customer) -> None:
    customer.balance += total(invoice)  # invoicing changes customers' state
```

Good, reading from a sibling through an owned port
(`templates/example-project/src/acme/invoicing/`):

```python
# acme/invoicing/usecases/ports.py
class CustomerLookup(Protocol):
    def exists(self, customer_id: str) -> bool: ...


# acme/invoicing/infrastructure/customer_lookup.py: the one file that imports customers
from acme.customers import CustomerNotFound, CustomerRepository

class CustomerRepositoryLookup:
    def __init__(self, customers: CustomerRepository) -> None:
        self._customers = customers

    def exists(self, customer_id: str) -> bool:
        try:
            self._customers.get(customer_id)
        except CustomerNotFound:
            return False
        return True
```

Good, changing state in two modules through a coordinating use case
(`templates/example-project/src/acme/checkout/`):

```python
# acme/checkout/usecases/ports.py
class CheckoutUnitOfWork(Protocol):
    @property
    def invoices(self) -> InvoiceRepository: ...
    @property
    def customers(self) -> CustomerRepository: ...

    def __enter__(self) -> Self: ...
    def __exit__(self, exc_type: type[BaseException] | None, exc: BaseException | None,
                 tb: TracebackType | None) -> None: ...  # rolls back unless committed
    def commit(self) -> None: ...


# acme/checkout/usecases/check_out.py
def check_out(
    uow: CheckoutUnitOfWork,
    clock: Clock,
    ids: IdGenerator,
    customer_id: str,
    line_items: tuple[LineItem, ...],
) -> Invoice:
    with uow:
        customer = uow.customers.get(customer_id)
        invoice = issue(draft(InvoiceId(ids.new_id()), customer.id, line_items), now=clock.now())
        charged = charge(customer, total(invoice))
        uow.invoices.add(invoice)
        uow.customers.add(charged)
        uow.commit()
    return invoice
```

The unit-of-work protocol belongs to the coordinating module, because only
it knows which repositories must commit together. Its repositories are
read-only properties: a mutable protocol attribute is invariant, and pyright
strict would reject the in-memory fakes. The coordinating module has no
domain of its own; it calls the rules of the modules it coordinates.

## Codify it

import-linter, configured in `pyproject.toml`. The `layers` contract declares
the allowed direction between modules; `|` marks modules in a layer as
independent of each other, and `ignore_imports` lists the adapters that read
from a sibling:

```toml
[tool.importlinter]
root_package = "acme"

[[tool.importlinter.contracts]]
name = "Modules depend down the layers"
type = "layers"
containers = ["acme"]
layers = ["checkout", "invoicing | customers", "clock | ids"]
ignore_imports = [
    # invoicing's adapter for its CustomerLookup port; translates customers into invoicing's terms
    "acme.invoicing.infrastructure.customer_lookup -> acme.customers",
]
broken_contract_guidance = """
A module may import only modules in lower layers, and modules in the same layer are \
independent. To read from a sibling module, define a port in your module's usecases/ports.py \
and implement it in an adapter in your infrastructure/, then add that one import to \
ignore_imports here. If an operation changes state in two modules, move it into a \
coordinating module like checkout. If the layers are wrong, change them here on purpose \
and say why in the pull request."""
```

One `protected` contract per module keeps everything below its `__init__.py`
private. `**` covers the layer subpackages:

```toml
[[tool.importlinter.contracts]]
name = "invoicing is used through its public API"
type = "protected"
protected_modules = ["acme.invoicing.**"]
allowed_importers = ["acme.invoicing"]
broken_contract_guidance = """
Import from acme.invoicing, not from its submodules. If the name you need is missing, \
add it to __all__ in acme/invoicing/__init__.py."""
```

A violation reads:

```text
invoicing is used through its public API BROKEN
- acme.checkout.usecases.check_out -> acme.invoicing.domain.model (l.8)
Import from acme.invoicing, not from its submodules. ...
```

The layering inside each module is a third contract, in `module-layout.md`.

Alternative: tach expresses the first two in one `tach.toml`, with an
explicit `depends_on` allowlist per module and `interfaces` for the public
API.

## Review by hand

- Did you add a module? Add it to the layers contract, to `containers` of
  the contract inside modules, and give it a `protected` contract.
- Did you add a name to a module's `__all__`? Is it part of the module's
  responsibility, or an internal detail leaking out?
- Did you add an `ignore_imports` entry? It must be an adapter in
  `infrastructure/` implementing a port of its own module, and the pair must
  not already link in the other direction. Say so in your reply.
- Did you change the layers contract? Say so in your reply and why.
- Does this module now change state that another module is responsible for?
  The layers contract catches imports, not calls passed in through
  callbacks or ports.
