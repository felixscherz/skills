"""The unit of work belongs to checkout, because the owner of the workflow is the
only one that knows which repositories must commit together."""

from types import TracebackType
from typing import Protocol, Self

from acme.customers import CustomerRepository
from acme.invoicing import InvoiceRepository


class CheckoutUnitOfWork(Protocol):
    @property
    def invoices(self) -> InvoiceRepository: ...

    @property
    def customers(self) -> CustomerRepository: ...

    def __enter__(self) -> Self: ...

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        """Roll back everything not committed."""
        ...

    def commit(self) -> None: ...
