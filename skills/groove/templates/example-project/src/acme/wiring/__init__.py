"""Wiring: the composition root. Builds every adapter and hands it to the use cases.

The only code outside a module that imports the module's infrastructure/ (and
its api/, once it has one). Everything else comes from the public APIs.
"""

from dataclasses import dataclass
from pathlib import Path

from acme.clock import Clock, SystemClock
from acme.customers import CustomerRepository
from acme.ids import IdGenerator, UuidIdGenerator
from acme.invoicing import (
    CustomerLookup,
    Invoice,
    InvoiceId,
    InvoiceRepository,
    LineItem,
    draft_invoice,
    issue_invoice,
)
from acme.invoicing.infrastructure.customer_lookup import CustomerRepositoryLookup
from acme.invoicing.infrastructure.json_files import JsonFileInvoiceRepository

__all__ = ["Invoicing", "build_invoicing"]


@dataclass(frozen=True)
class Invoicing:
    """The invoicing use cases with their ports bound, ready for a route or command."""

    invoices: InvoiceRepository
    customers: CustomerLookup
    clock: Clock
    ids: IdGenerator

    def draft(self, customer_id: str, line_items: tuple[LineItem, ...]) -> Invoice:
        return draft_invoice(self.invoices, self.customers, self.ids, customer_id, line_items)

    def issue(self, invoice_id: InvoiceId) -> Invoice:
        return issue_invoice(self.invoices, self.clock, invoice_id)


def build_invoicing(directory: Path, customers: CustomerRepository) -> Invoicing:
    # customers has no storage adapter yet, so the caller supplies its repository.
    return Invoicing(
        invoices=JsonFileInvoiceRepository(directory),
        customers=CustomerRepositoryLookup(customers),
        clock=SystemClock(),
        ids=UuidIdGenerator(prefix="inv_"),
    )
