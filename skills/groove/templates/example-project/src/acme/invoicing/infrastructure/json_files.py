"""Stores Invoices as JSON files. Constructed only by the composition root."""

import json
from pathlib import Path

from acme.invoicing.domain.model import Invoice, InvoiceId
from acme.invoicing.infrastructure.records import from_record, to_record
from acme.invoicing.usecases.ports import InvoiceNotFound


class JsonFileInvoiceRepository:
    def __init__(self, directory: Path) -> None:
        self._directory = directory

    def get(self, invoice_id: InvoiceId) -> Invoice:
        path = self._directory / f"{invoice_id.value}.json"
        if not path.exists():
            raise InvoiceNotFound(invoice_id)
        return from_record(json.loads(path.read_text()))

    def add(self, invoice: Invoice) -> None:
        path = self._directory / f"{invoice.id.value}.json"
        path.write_text(json.dumps(to_record(invoice)))
