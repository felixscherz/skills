"""Persisted shape of an Invoice, with versioned migrations.

Bump CURRENT_VERSION on every shape change, add a migration step from the
previous version, and add tests/fixtures/invoice/v<N>.json.
"""

from collections.abc import Callable
from datetime import datetime
from decimal import Decimal
from typing import Any

from acme.invoicing.domain.model import Invoice, InvoiceId, InvoiceStatus, LineItem

type Record = dict[str, Any]

CURRENT_VERSION = 2


def to_record(invoice: Invoice) -> Record:
    return {
        "version": CURRENT_VERSION,
        "id": invoice.id,
        "customer_id": invoice.customer_id,
        "line_items": [
            {"description": item.description, "amount": str(item.amount)}
            for item in invoice.line_items
        ],
        "status": invoice.status.value,
        "issued_at": invoice.issued_at.isoformat() if invoice.issued_at else None,
    }


def from_record(record: Record) -> Invoice:
    record = _migrate(record)
    return Invoice(
        id=InvoiceId(record["id"]),
        customer_id=record["customer_id"],
        line_items=tuple(
            LineItem(description=item["description"], amount=Decimal(item["amount"]))
            for item in record["line_items"]
        ),
        status=InvoiceStatus(record["status"]),
        issued_at=datetime.fromisoformat(record["issued_at"]) if record["issued_at"] else None,
    )


def _v1_to_v2(record: Record) -> Record:
    """v1 stored amounts as integer cents, v2 as decimal strings."""
    line_items = [
        {"description": item["description"], "amount": str(Decimal(item["amount_cents"]) / 100)}
        for item in record["line_items"]
    ]
    return {**record, "version": 2, "line_items": line_items}


_MIGRATIONS: dict[int, Callable[[Record], Record]] = {1: _v1_to_v2}


def _migrate(record: Record) -> Record:
    version = record.get("version")
    if not isinstance(version, int) or not 1 <= version <= CURRENT_VERSION:
        raise ValueError(
            f"Invoice record has version {version!r}, expected an int from 1 to "
            f"{CURRENT_VERSION}. If the shape changed, bump CURRENT_VERSION in "
            "acme/invoicing/infrastructure/records.py and add a migration step."
        )
    while record["version"] < CURRENT_VERSION:
        record = _MIGRATIONS[record["version"]](record)
    return record
