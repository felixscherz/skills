"""Fake unit of work. Changes become visible only on commit."""

from copy import deepcopy
from types import TracebackType
from typing import Self

from acme.customers import InMemoryCustomerRepository
from acme.invoicing import InMemoryInvoiceRepository


class InMemoryCheckoutUnitOfWork:
    def __init__(
        self, invoices: InMemoryInvoiceRepository, customers: InMemoryCustomerRepository
    ) -> None:
        self.committed_invoices = invoices
        self.committed_customers = customers
        self.invoices = invoices
        self.customers = customers

    def __enter__(self) -> Self:
        self.invoices = deepcopy(self.committed_invoices)
        self.customers = deepcopy(self.committed_customers)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.invoices = self.committed_invoices
        self.customers = self.committed_customers

    def commit(self) -> None:
        self.committed_invoices = self.invoices
        self.committed_customers = self.customers
