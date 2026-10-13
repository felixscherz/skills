"""Use case: draft an Invoice for an existing Customer."""

from acme.ids import IdGenerator
from acme.invoicing.domain.model import Invoice, InvoiceId, LineItem, draft
from acme.invoicing.usecases.ports import (
    CustomerLookup,
    InvoiceForUnknownCustomer,
    InvoiceRepository,
)


def draft_invoice(
    invoices: InvoiceRepository,
    customers: CustomerLookup,
    ids: IdGenerator,
    customer_id: str,
    line_items: tuple[LineItem, ...],
) -> Invoice:
    if not customers.exists(customer_id):
        raise InvoiceForUnknownCustomer(customer_id)
    invoice = draft(InvoiceId(ids.new_id()), customer_id, line_items)
    invoices.add(invoice)
    return invoice
