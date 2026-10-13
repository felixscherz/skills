# checkout

## Responsibility

Issues an Invoice and charges the Customer its total, as one step that
either fully happens or not at all.

A coordinating module: it sits one layer above `invoicing` and `customers`,
which never import each other, and owns the unit of work that makes both
writes commit together. It has no domain of its own; the rules stay in the
modules it coordinates.

Not responsible for: drafting or issuing an Invoice on its own
(`invoicing`), or a Customer's Balance rules (`customers`).

## Public API

- `check_out`: the use case.
- `CheckoutUnitOfWork`: port.
- `InMemoryCheckoutUnitOfWork`: fake for tests.

## Glossary terms

- Checkout
- Invoice
- Customer
- Charge

## Ports

| Port | Fake | Adapter |
|---|---|---|
| `CheckoutUnitOfWork` | `InMemoryCheckoutUnitOfWork` | none yet |

Dependencies are declared in the import-linter contracts in `pyproject.toml`.
