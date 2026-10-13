"""Functional core: Invoice values and the rules for changing them.

No I/O, no clock, no randomness, no IDs generated here. Everything comes in
as an argument.
"""

from dataclasses import dataclass, replace
from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import NewType

InvoiceId = NewType("InvoiceId", str)


class InvoiceStatus(StrEnum):
    DRAFT = "draft"
    ISSUED = "issued"


@dataclass(frozen=True, slots=True)
class LineItem:
    description: str
    amount: Decimal


@dataclass(frozen=True, slots=True)
class Invoice:
    id: InvoiceId
    customer_id: str
    line_items: tuple[LineItem, ...]
    status: InvoiceStatus
    issued_at: datetime | None


class InvoiceAlreadyIssued(Exception):
    def __init__(self, invoice_id: InvoiceId) -> None:
        super().__init__(
            f"Invoice {invoice_id} is already issued and cannot be issued again. "
            "Check invoice.status before calling issue(), or draft a new Invoice."
        )


class EmptyInvoice(Exception):
    def __init__(self, invoice_id: InvoiceId) -> None:
        super().__init__(
            f"Invoice {invoice_id} has no line items and cannot be issued. "
            "Draft it with at least one LineItem."
        )


def draft(invoice_id: InvoiceId, customer_id: str, line_items: tuple[LineItem, ...]) -> Invoice:
    return Invoice(
        id=invoice_id,
        customer_id=customer_id,
        line_items=line_items,
        status=InvoiceStatus.DRAFT,
        issued_at=None,
    )


def issue(invoice: Invoice, now: datetime) -> Invoice:
    if invoice.status is InvoiceStatus.ISSUED:
        raise InvoiceAlreadyIssued(invoice.id)
    if not invoice.line_items:
        raise EmptyInvoice(invoice.id)
    return replace(invoice, status=InvoiceStatus.ISSUED, issued_at=now)


def total(invoice: Invoice) -> Decimal:
    return sum((item.amount for item in invoice.line_items), Decimal(0))
