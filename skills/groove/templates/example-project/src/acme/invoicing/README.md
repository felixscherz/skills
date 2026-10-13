# invoicing

## Responsibility

Drafts Invoices for Customers and issues them.

Not responsible for: charging Customers (`customers`), or Checkout, which
issues an Invoice and charges the Customer in one step (`checkout`).

## Layout

- `domain/`: the Invoice values and rules. Pure: takes the time and new IDs
  as arguments.
- `usecases/`: one file per intent, plus the ports they consume and fakes.
- `infrastructure/`: adapters for the ports, and the persisted record shape.

## Public API

- `Invoice`, `InvoiceId`, `InvoiceStatus`, `LineItem`: the Invoice values.
- `draft`, `issue`, `total`: the rules, for modules above it such as `checkout`.
- `draft_invoice`, `issue_invoice`: use cases.
- `InvoiceRepository`, `CustomerLookup`: ports.
- `InMemoryInvoiceRepository`, `FakeCustomerLookup`: fakes for tests.
- `JsonFileInvoiceRepository`, `CustomerRepositoryLookup`: adapters, for the
  composition root only.
- `InvoiceAlreadyIssued`, `EmptyInvoice`, `InvoiceNotFound`,
  `InvoiceForUnknownCustomer`: errors.

## Glossary terms

- Invoice
- Issue
- Line Item
- Customer (by id only)

## Ports

| Port | Fake | Adapter |
|---|---|---|
| `InvoiceRepository` | `InMemoryInvoiceRepository` | `JsonFileInvoiceRepository` |
| `CustomerLookup` | `FakeCustomerLookup` | `CustomerRepositoryLookup` |

`CustomerRepositoryLookup` is the only code in invoicing that imports another
module (`customers`), declared in `ignore_imports` of the layers contract.

Uses `Clock` from `clock` and `IdGenerator` from `ids`.

## Persisted data

| Shape | Current version | Fixtures |
|---|---|---|
| Invoice record (`infrastructure/records.py`) | 2 | `tests/fixtures/invoice/` |

Dependencies are declared in the import-linter contracts in `pyproject.toml`.
