from datetime import UTC, datetime
from decimal import Decimal

import pytest

from acme.checkout import InMemoryCheckoutUnitOfWork, check_out
from acme.clock import FakeClock
from acme.customers import Customer, CustomerNotFound, InMemoryCustomerRepository
from acme.ids import SequentialIdGenerator
from acme.invoicing import (
    InMemoryInvoiceRepository,
    InvoiceId,
    InvoiceNotFound,
    InvoiceStatus,
    LineItem,
)

NOW = datetime(2026, 4, 30, 12, 0, tzinfo=UTC)
ADA = Customer(id="cus_01", name="Ada", balance=Decimal("0"))


def make_uow() -> InMemoryCheckoutUnitOfWork:
    return InMemoryCheckoutUnitOfWork(
        invoices=InMemoryInvoiceRepository(), customers=InMemoryCustomerRepository(ADA)
    )


def test_check_out_issues_invoice_and_charges_customer() -> None:
    uow = make_uow()

    invoice = check_out(
        uow,
        clock=FakeClock(NOW),
        ids=SequentialIdGenerator(prefix="inv_"),
        customer_id=ADA.id,
        line_items=(LineItem("Consulting", Decimal("100")),),
    )

    assert uow.invoices.get(invoice.id).status is InvoiceStatus.ISSUED
    assert uow.customers.get(ADA.id).balance == Decimal("100")


def test_check_out_for_unknown_customer_changes_nothing() -> None:
    uow = make_uow()

    with pytest.raises(CustomerNotFound):
        check_out(
            uow,
            clock=FakeClock(NOW),
            ids=SequentialIdGenerator(prefix="inv_"),
            customer_id="cus_unknown",
            line_items=(LineItem("Consulting", Decimal("100")),),
        )

    assert uow.customers.get(ADA.id).balance == Decimal("0")
    with pytest.raises(InvoiceNotFound):
        uow.invoices.get(InvoiceId("inv_01"))


def test_check_out_with_zero_total_changes_nothing() -> None:
    uow = make_uow()

    with pytest.raises(ValueError, match="Charge a positive amount"):
        check_out(
            uow,
            clock=FakeClock(NOW),
            ids=SequentialIdGenerator(prefix="inv_"),
            customer_id=ADA.id,
            line_items=(LineItem("Free sample", Decimal("0")),),
        )

    assert uow.customers.get(ADA.id).balance == Decimal("0")
    with pytest.raises(InvoiceNotFound):
        uow.invoices.get(InvoiceId("inv_01"))
