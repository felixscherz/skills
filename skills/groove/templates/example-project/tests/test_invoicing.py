import json
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

import pytest

from acme.clock import FakeClock
from acme.customers import Customer, InMemoryCustomerRepository
from acme.ids import SequentialIdGenerator
from acme.invoicing import (
    FakeCustomerLookup,
    InMemoryInvoiceRepository,
    InvoiceAlreadyIssued,
    InvoiceForUnknownCustomer,
    InvoiceStatus,
    LineItem,
    draft_invoice,
    issue_invoice,
)

# Tests of a module may use its internals. Tests of other modules may not.
from acme.invoicing.infrastructure.customer_lookup import CustomerRepositoryLookup
from acme.invoicing.infrastructure.records import CURRENT_VERSION, from_record

FIXTURES = sorted((Path(__file__).parent / "fixtures" / "invoice").glob("v*.json"))
NOW = datetime(2026, 4, 30, 12, 0, tzinfo=UTC)
CONSULTING = (LineItem("Consulting", Decimal("100")),)


def test_issue_sets_status_and_issued_at() -> None:
    invoices = InMemoryInvoiceRepository()
    ids = SequentialIdGenerator(prefix="inv_")
    invoice = draft_invoice(invoices, FakeCustomerLookup("cus_01"), ids, "cus_01", CONSULTING)

    issued = issue_invoice(invoices, FakeClock(NOW), invoice.id)

    assert issued.status is InvoiceStatus.ISSUED
    assert issued.issued_at == NOW


def test_issuing_twice_fails() -> None:
    invoices = InMemoryInvoiceRepository()
    ids = SequentialIdGenerator(prefix="inv_")
    invoice = draft_invoice(invoices, FakeCustomerLookup("cus_01"), ids, "cus_01", CONSULTING)
    issue_invoice(invoices, FakeClock(NOW), invoice.id)

    with pytest.raises(InvoiceAlreadyIssued):
        issue_invoice(invoices, FakeClock(NOW), invoice.id)


def test_drafting_for_unknown_customer_fails() -> None:
    with pytest.raises(InvoiceForUnknownCustomer):
        draft_invoice(
            InMemoryInvoiceRepository(),
            FakeCustomerLookup(),
            SequentialIdGenerator(prefix="inv_"),
            "cus_unknown",
            CONSULTING,
        )


def test_customer_lookup_answers_from_customers_module() -> None:
    customers = InMemoryCustomerRepository(Customer(id="cus_01", name="Ada", balance=Decimal(0)))
    lookup = CustomerRepositoryLookup(customers)

    assert lookup.exists("cus_01")
    assert not lookup.exists("cus_unknown")


@pytest.mark.parametrize("path", FIXTURES, ids=lambda p: p.stem)
def test_every_invoice_fixture_loads(path: Path) -> None:
    from_record(json.loads(path.read_text()))


def test_current_invoice_version_has_a_fixture() -> None:
    assert f"v{CURRENT_VERSION}" in {p.stem for p in FIXTURES}, (
        f"Add tests/fixtures/invoice/v{CURRENT_VERSION}.json with a realistic record "
        "of the current shape. Do not edit older fixtures."
    )
