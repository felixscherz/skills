"""Use case: issue a drafted Invoice.

Load, let the domain decide, save. A use case that saves more than once takes
a unit of work instead of a repository, so the saves commit together.
"""

from acme.clock import Clock
from acme.invoicing.domain.model import Invoice, InvoiceId, issue
from acme.invoicing.usecases.ports import InvoiceRepository


def issue_invoice(invoices: InvoiceRepository, clock: Clock, invoice_id: InvoiceId) -> Invoice:
    invoice = issue(invoices.get(invoice_id), now=clock.now())
    invoices.add(invoice)
    return invoice
