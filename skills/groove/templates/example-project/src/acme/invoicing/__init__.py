"""Invoicing: drafting and issuing Invoices for Customers.

This file is the module's public API. Other modules import only names listed
in __all__, never from the submodules. Adapters in infrastructure/ are not
exported: only the composition root (acme.composition) constructs them.
"""

from acme.invoicing.domain.model import (
    EmptyInvoice,
    Invoice,
    InvoiceAlreadyIssued,
    InvoiceId,
    InvoiceStatus,
    LineItem,
    draft,
    issue,
    total,
)
from acme.invoicing.usecases.draft_invoice import draft_invoice
from acme.invoicing.usecases.fakes import FakeCustomerLookup, InMemoryInvoiceRepository
from acme.invoicing.usecases.issue_invoice import issue_invoice
from acme.invoicing.usecases.ports import (
    CustomerLookup,
    InvoiceForUnknownCustomer,
    InvoiceNotFound,
    InvoiceRepository,
)

__all__ = [
    "CustomerLookup",
    "EmptyInvoice",
    "FakeCustomerLookup",
    "InMemoryInvoiceRepository",
    "Invoice",
    "InvoiceAlreadyIssued",
    "InvoiceForUnknownCustomer",
    "InvoiceId",
    "InvoiceNotFound",
    "InvoiceRepository",
    "InvoiceStatus",
    "LineItem",
    "draft",
    "draft_invoice",
    "issue",
    "issue_invoice",
    "total",
]
