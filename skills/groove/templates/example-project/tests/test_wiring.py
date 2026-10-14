from decimal import Decimal
from pathlib import Path

from acme.customers import Customer, InMemoryCustomerRepository
from acme.invoicing import InvoiceStatus, LineItem
from acme.wiring import build_invoicing


def test_built_invoicing_stores_issued_invoices_as_json_files(tmp_path: Path) -> None:
    customers = InMemoryCustomerRepository(Customer(id="cus_01", name="Ada", balance=Decimal(0)))
    invoicing = build_invoicing(tmp_path, customers)

    invoice = invoicing.draft("cus_01", (LineItem("Consulting", Decimal("100")),))
    issued = invoicing.issue(invoice.id)

    assert issued.status is InvoiceStatus.ISSUED
    assert invoicing.invoices.get(invoice.id).status is InvoiceStatus.ISSUED
    assert (tmp_path / f"{invoice.id}.json").exists()
