# Acme billing

Drafts and issues Invoices for Customers, and charges a Customer's Balance
when they check out.

## Read when

- Naming a domain concept: `docs/glossary.md`
- Changing a module: its `README.md`, or the docstring of a single-file
  module
- Wiring a use case to a route or command: `src/acme/wiring.py`

## Features

There are no routes or commands yet. Each feature is a use case, built with
its adapters in `src/acme/wiring.py`.

### Invoicing

- **Draft an Invoice** - `draft_invoice`, `src/acme/invoicing/usecases/`.
  Rules in `src/acme/invoicing/domain/` (`Invoice`, `LineItem`).
- **Issue an Invoice** - `issue_invoice`, `src/acme/invoicing/usecases/`.

### Customers

- **Charge a Customer** - `charge`, `src/acme/customers.py`.

### Checkout

- **Check out** - `check_out`, `src/acme/checkout/usecases/`. Issues an
  Invoice and charges the Customer in one unit of work.
