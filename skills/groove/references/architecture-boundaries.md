# Architecture boundaries

## The rule

Code is split into modules, each with one responsibility written in its
`README.md`, or in its docstring for a single-file module. A module is a
top-level package under `src/acme/`, split internally into layers, or a
single top-level file while it is small (see `module-layout.md`).

- **Public API.** A module's public API is what its `__init__.py`, or its
  single file, exports in `__all__`: its domain values and rules, use cases,
  ports, errors, and the fakes for its ports. Adapters (`infrastructure/`) and entry points
  (`api/`, `cli/`) are not exported. Everything else in the module is
  internal.
- **Import only the public API.** Code outside a module imports from
  `acme.invoicing`, never from `acme.invoicing.domain.model`. Tests of other
  modules follow the same rule. A module's own tests may import its
  internals.
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
- **Choose the direction on purpose.** Which of two modules sits in the
  higher layer is a design decision, made per pair. Existence pulls one
  way: the module that can exist without the other goes lower, and the one
  built from it goes higher (catalog above procurement when Products are
  built from SupplierProducts). Importance can pull the other way: a core
  module may need to stay free of a supporting one. Neither wins by
  default. Existence is a domain fact, so confirm it with the user. To
  invert it, the core goes lower and owns a port; the higher module
  implements it in its `infrastructure/`. Say which way you chose and why.
- **Hold other modules' entities by ID.** A domain value refers to another
  module's entity by its ID type (`based_on: tuple[SupplierProductId, ...]`),
  never by holding the entity. Only use cases load the entity itself.
- **A link lives in the higher module.** When an entity refers to another
  module's entity, the referring entity is in the higher module and holds
  the ID (`Product.based_on` in catalog). A lower module cannot hold a
  higher one's ID. When the link grows a lifecycle, validity periods, or
  rules of its own, it is a concept: give it its own entity in the higher
  module and its own glossary term.
- **Downstream identities have a downstream owner.** A field belongs to the
  context that gives it meaning, not wherever the legacy database stored it.
  Catalog's Product does not require an OMS or SAP identifier. A mapping in
  Exports holds the Catalog ProductId, the export system, and that system's
  product ID; Catalog does not depend on Exports. External wire names and
  payload formats stay in adapters, but a locally owned mapping can be a
  domain concept. Identify its owner before adding the field, not after
  choosing the import direction.
- **Every write has one owner.** One use case in one module runs each
  operation that changes state. A module changes state owned by another
  module only through that module's public API: its rules and its
  repositories, never by building or editing its values directly. Find the
  owner by asking in this order:
  - **It writes one module.** That module owns it. It reads lower modules
    through their public API and siblings through a port it owns.
  - **It writes modules in different layers.** The highest module it writes
    owns it when the rule is in its language. It changes the lower modules
    through their public rules and repositories, in one unit of work while
    they share a store, and through events otherwise. When the rule is in a
    lower module's language instead, that module commits its own change and
    records an event, and the higher module reacts.
  - **It writes siblings, and one of them has the rule.** The rule is in
    that module's language, such as "an issued Invoice is charged" in
    invoicing. That module commits its own change and records an event, and
    the other reacts in its own transaction.
  - **It writes siblings that must commit together.** The boundary needs a
    decision. If one module is built from the other, they do not belong in
    one layer: move it up (see "Choose the direction on purpose") and ask
    again. If the business already names the workflow (Checkout), it gets a
    module of its own one layer above the modules it uses, owning the use
    case and the unit of work. That module is a domain module like any
    other; it may have no rules yet, and grows a `domain/` once it has one.
    Do not coin a term to give a workflow a home. Otherwise, merge the
    modules.

  A unit of work spans modules only while they share a store that can
  commit together; when they do not, fall back to events.
- **The trigger is not the owner.** What starts an operation (an API
  handler, a CLI command, an event subscriber) calls the owner's use case.
  It does not sequence the steps itself.
- **Events belong to the module that records them.** The event type is part
  of its public API, in its own language (`SupplierProductDiscontinued` in
  procurement). The reaction is a use case of the reacting module, started
  by a subscriber among its entry points and wired by the composition root.
  Events follow the direction of imports: a higher module reacts to a lower
  one's events directly. A sibling reacts through an adapter in its
  `infrastructure/` that translates the event into its own terms, listed in
  `ignore_imports` like a read.
- **A read belongs to the module asking the question.** A query that
  combines modules lives in the module whose question it is, which must sit
  above the modules it reads, or read siblings through a port. A read that
  belongs to none of them (a report, a dashboard) gets a read-only module
  above them that never writes.
- **Composition root.** One place builds the application: it constructs
  adapters and wires them into use cases. It sits in the top layer, and it
  is the only code outside a module that imports the module's
  `infrastructure/` and entry points directly. Everything a module offers
  to the application's assembly rather than to other modules lives there:
  adapters, HTTP routers, CLI commands, message handlers, metric
  registration. Exporting them from `__init__.py` instead would put
  framework and storage imports into every import of the module, and a
  router that calls other modules' use cases easily closes an import cycle.
  If the application is assembled in several top-level modules (an app
  factory, telemetry setup, a worker entry point), together they are the
  composition root; list each one in the contracts.

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
customers module. Naming an owner for every write puts its sequencing and
failure handling in one use case, instead of spread across handlers or
dropped into whichever module the agent opened first. Asking what an
operation writes before anything else keeps most operations in the module
they change, and lets a higher module commit across the modules it already
depends on when the domain says the changes belong together. Only a
workflow the business names on its own becomes a module, so invoicing does
not need to know that checkout exists, and agents do not invent workflow
modules to resolve a boundary they should have moved. The unit of work
keeps consistency in one place instead of scattered try/except blocks.

## Example

An external identity mapping belongs to the context that owns the mapping:

```text
exports                  depends on catalog
  ExportedProduct
    product_id: ProductId
    system: ExportSystem
    system_product_id: SystemProductId

catalog                  does not depend on exports
  Product
    id: ProductId
```

Catalog can describe a Product without a downstream integration. Exports
owns the mapping; its adapters translate it into OMS or SAP payloads. The
import contracts enforce the direction, not whether a field has the right
owner.

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

Good, a workflow that is a concept of its own, owned by its own module
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

invoicing and customers are siblings that must commit together, and neither
is built from the other. Checkout is a term the business already uses, and
its rule, all or nothing, belongs to neither module, so checkout owns the
workflow. The unit-of-work
protocol belongs to checkout, because only the owner knows which
repositories must commit together. Its repositories are read-only
properties: a mutable protocol attribute is invariant, and pyright strict
would reject the in-memory fakes. checkout has no rules of its own yet, so it
has no `domain/` and calls the rules of invoicing and customers. A rule of
Checkout itself would start its `domain/`.

Good, a higher module owning a write that spans the modules below it. A
Product in catalog is built from SupplierProducts in procurement, so catalog
sits above procurement. Listing a Product reserves its SupplierProducts, and
both must commit together. The rule is in catalog's language, so catalog
owns it and changes procurement only through procurement's public rules and
repository:

```python
# acme/catalog/usecases/create_product.py
from acme import procurement


def create_product(uow: CreateProductUnitOfWork, ids: IdGenerator,
                   command: CreateProduct) -> Product:
    with uow:
        sources = uow.supplier_products.get_many(command.based_on)
        product = new_product(ProductId(ids.new_id()), command.name, command.based_on)
        reserved = tuple(procurement.reserve(source) for source in sources)  # no ProductId: procurement sits lower
        uow.products.add(product)
        for source in reserved:
            uow.supplier_products.add(source)
        uow.commit()
    return product
```

`CreateProductUnitOfWork` lives in catalog's `usecases/ports.py` and lists
catalog's `ProductRepository` and procurement's `SupplierProductRepository`.
No workflow module is needed.

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
layers = ["composition", "checkout", "invoicing | customers", "clock | ids"]
ignore_imports = [
    # invoicing's adapter for its CustomerLookup port; translates customers into invoicing's terms
    "acme.invoicing.infrastructure.customer_lookup -> acme.customers",
]
broken_contract_guidance = """
A module may import only modules in lower layers, and modules in the same layer are \
independent. To read from a sibling module, define a port in your module's usecases/ports.py \
and implement it in an adapter in your infrastructure/, then add that one import to \
ignore_imports here. An operation that changes state in several modules belongs to the \
module it writes, or to the highest module it writes, which changes the lower ones through \
their public API. Siblings that must commit together mean one should move up a layer, or, \
when the business already names the workflow, a module of its own one layer up, like \
checkout. If the layers are wrong, change them here on purpose and say why in the pull \
request."""
```

One `protected` contract per package module keeps everything below its
`__init__.py` private. A single-file module has nothing below it, so it
needs none until it becomes a package. `**` covers the layer subpackages. The composition root is the one
allowed importer from outside, so it can construct adapters and mount
entry points:

```toml
[[tool.importlinter.contracts]]
name = "invoicing is used through its public API"
type = "protected"
protected_modules = ["acme.invoicing.**"]
allowed_importers = ["acme.invoicing", "acme.composition"]
broken_contract_guidance = """
Import from acme.invoicing, not from its submodules. If the name you need is missing and it \
is a domain value, rule, use case, port, error, or fake, add it to __all__ in \
acme/invoicing/__init__.py. Adapters and entry points are not exported: only acme.composition \
constructs them."""
```

When the tests are a package that import-linter analyzes, add the module's
own tests (`"tests.invoicing.**"`) to `allowed_importers`, and nothing
broader: tests of other modules use the public API. When the application is
assembled in several top-level modules, list each one instead of
`acme.composition`, by exact name.

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

- Did you add a module? Add it to the layers contract. If it is a package,
  also add it to `containers` of the contract inside modules and give it a
  `protected` contract.
- Did you add a name to a module's `__all__`? Is it part of the module's
  responsibility, or an internal detail leaking out? An adapter, router, or
  framework hook belongs in the composition root's imports, not in
  `__all__`.
- Does the composition root import anything from a module's `domain/` or
  `usecases/` directly? The protected contract allows it, so check by hand:
  the composition root takes adapters and entry points from their files, and
  everything else from the public API.
- Did you add an `ignore_imports` entry? It must be an adapter in
  `infrastructure/` implementing a port of its own module, and the pair must
  not already link in the other direction. Say so in your reply.
- Did you change the layers contract? Say so in your reply and why.
- Did you place a module in a layer, or move one? Say which module of each
  pair it touches sits higher, and whether existence or importance decided.
- Does a new domain value hold another module's entity instead of its ID?
- Would each entity still make sense if a downstream integration disappeared?
  Which fields exist only because that integration needs them? Check their
  owner by hand: an import contract cannot detect a misplaced string field.
- Does this module now change state that another module is responsible for
  without going through that module's public rules and repositories?
  The layers contract catches imports, not calls passed in through
  callbacks or ports.
- Does an operation change state in several modules? Name its owner in your
  reply and which case of "Every write has one owner" decided it. An entry
  point that sequences the steps itself has no owner.
- Did you add a workflow module? Say where the business uses its name, and
  why moving one of the modules up a layer did not fit.
- Did you add an event or a reaction? The event type is in the recording
  module's public API, the reaction is a use case of the reacting module,
  and it does not react against the layers except through an adapter.
