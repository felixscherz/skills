# Glossary

One canonical term per domain concept. Use these terms in code, docs, tests,
log and error messages, commit messages, and conversation. Banned synonyms
may appear only in an adapter that translates an external system's
vocabulary.

To add a term, add an entry with `**Status:** proposed` in the same change
and mention it in your reply. A human changes it to `accepted`. To rename a
term, rename every occurrence and move the old name to **Banned**.

Entries are sorted alphabetically.

## Balance

The amount a Customer owes. Charging a Customer increases it.

- **Code:** `balance`
- **Banned:** debt, outstanding
- **Status:** accepted

## Charge

To add an amount to a Customer's Balance.

- **Code:** `charge`
- **Banned:** debit
- **Status:** accepted

## Checkout

Issuing an Invoice for a Customer and charging the Customer its total, as
one step that either fully happens or not at all.

- **Code:** `checkout` (module), `check_out` (operation)
- **Banned:** purchase, order
- **Status:** proposed

## Customer

A person or organization that receives Invoices and pays them.

- **Code:** `Customer`, `customer`, `customers`, `customer_id`
- **Banned:** client, buyer, account, user
- **External names:** `customer` (payment provider)
- **Status:** accepted

## Invoice

A request for payment sent to a Customer for one or more Line Items. An
Invoice is a draft until it is issued, and immutable afterwards.

- **Code:** `Invoice`, `InvoiceId`, `invoice`, `invoices`, `invoice_id`
- **Banned:** bill, statement
- **Not to be confused with:** Receipt, which confirms a payment.
- **Status:** accepted

## Issue

To make a draft Invoice final and payable. After it is issued, an Invoice
cannot change.

- **Code:** `issue`, `issued`, `issued_at`, `InvoiceIssued`
- **Banned:** send, finalize, submit, publish
- **Status:** accepted

## Line Item

One charge on an Invoice, with a description and an amount.

- **Code:** `LineItem`, `line_item`, `line_items`
- **Banned:** position, row, entry
- **Status:** proposed
