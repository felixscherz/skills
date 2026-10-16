# checkout

## Responsibility

Issues an Invoice and charges the Customer its total, as one step that
either fully happens or not at all.

Not responsible for: drafting or issuing an Invoice on its own
(`invoicing`), or a Customer's Balance rules (`customers`).

## Glossary terms

- Checkout
- Invoice
- Customer
- Charge

## Decisions

Owns the Checkout workflow, because its rule (all or nothing) belongs to
neither `invoicing` nor `customers`. It sits one layer above them, and owns
the unit of work that makes both writes commit together. It has no rules of
its own yet, so no `domain/`; it calls the rules of `invoicing` and
`customers`.
