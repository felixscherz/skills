# invoicing

## Responsibility

Drafts Invoices for Customers and issues them.

Not responsible for: charging Customers (`customers`), or Checkout, which
issues an Invoice and charges the Customer in one step (`checkout`).

## Glossary terms

- Invoice
- Issue
- Line Item
- Customer (by id only)

## Decisions

Reads whether a Customer exists through its own `CustomerLookup` port.
`infrastructure/customer_lookup.py` is the only code in invoicing that
imports another module (`customers`), declared in `ignore_imports` of the
layers contract.
