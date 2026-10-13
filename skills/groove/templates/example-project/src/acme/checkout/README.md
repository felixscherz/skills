# checkout

## Responsibility

Issues an Invoice and charges the Customer its total, as one step that
either fully happens or not at all.

Owns the Checkout workflow, because its rule (all or nothing) belongs to
neither `invoicing` nor `customers`. It sits one layer above them, and owns
the unit of work that makes both writes commit together. It has no rules of
its own yet, so no `domain/`; it calls the rules of `invoicing` and
`customers`.

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
