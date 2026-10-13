"""Fakes for invoicing's ports. Tests in every module use these, not mocks."""

from acme.invoicing.domain.model import Invoice, InvoiceId
from acme.invoicing.usecases.ports import InvoiceNotFound


class InMemoryInvoiceRepository:
    def __init__(self) -> None:
        self._invoices: dict[InvoiceId, Invoice] = {}

    def get(self, invoice_id: InvoiceId) -> Invoice:
        try:
            return self._invoices[invoice_id]
        except KeyError:
            raise InvoiceNotFound(invoice_id) from None

    def add(self, invoice: Invoice) -> None:
        self._invoices[invoice.id] = invoice


class FakeCustomerLookup:
    def __init__(self, *customer_ids: str) -> None:
        self._customer_ids = set(customer_ids)

    def exists(self, customer_id: str) -> bool:
        return customer_id in self._customer_ids
