"""Protocols through which invoicing's use cases reach the outside world.

The use cases consume these ports, so they live here and not in the domain:
the domain decides, and never loads or saves anything itself.
"""

from typing import Protocol

from acme.invoicing.domain.model import Invoice, InvoiceId


class InvoiceNotFound(Exception):
    def __init__(self, invoice_id: InvoiceId) -> None:
        super().__init__(
            f"No Invoice with id {invoice_id.value}. "
            "Draft it with draft_invoice() first, or check the id."
        )


class InvoiceForUnknownCustomer(Exception):
    def __init__(self, customer_id: str) -> None:
        super().__init__(
            f"Cannot draft an Invoice for Customer {customer_id}, who does not exist. "
            "Add the Customer first, or check the id."
        )


class InvoiceRepository(Protocol):
    def get(self, invoice_id: InvoiceId) -> Invoice:
        """Return the Invoice, or raise InvoiceNotFound."""
        ...

    def add(self, invoice: Invoice) -> None:
        """Insert or replace the Invoice with the same id."""
        ...


class CustomerLookup(Protocol):
    """Invoicing's view of the customers context: only what drafting needs.

    Invoicing owns this port and words it in its own terms. An adapter in
    infrastructure implements it on top of the customers module.
    """

    def exists(self, customer_id: str) -> bool: ...
