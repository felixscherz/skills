"""Customers: who receives Invoices, and their balance.

Not responsible for: Invoices (invoicing), or Checkout, which charges a
Customer for an issued Invoice (checkout).

A single-file module: small, with no adapter and no route or command yet.
The file is the module's public API, listed in __all__. It becomes a package
with layers once it needs an adapter, for example to store Customers.
"""

from dataclasses import dataclass, replace
from decimal import Decimal
from typing import Protocol

__all__ = [
    "Customer",
    "CustomerNotFound",
    "CustomerRepository",
    "InMemoryCustomerRepository",
    "charge",
]


# Decides: values and rules, pure.


@dataclass(frozen=True, slots=True)
class Customer:
    id: str
    name: str
    balance: Decimal


def charge(customer: Customer, amount: Decimal) -> Customer:
    if amount <= 0:
        raise ValueError(
            f"Cannot charge Customer {customer.id} an amount of {amount}. "
            "Charge a positive amount; to pay money back, add a refund operation."
        )
    return replace(customer, balance=customer.balance + amount)


# Ports and their fakes.


class CustomerNotFound(Exception):
    def __init__(self, customer_id: str) -> None:
        super().__init__(f"No Customer with id {customer_id}. Check the id, or add the Customer.")


class CustomerRepository(Protocol):
    def get(self, customer_id: str) -> Customer:
        """Return the Customer, or raise CustomerNotFound."""
        ...

    def add(self, customer: Customer) -> None:
        """Insert or replace the Customer with the same id."""
        ...


class InMemoryCustomerRepository:
    def __init__(self, *customers: Customer) -> None:
        self._customers = {customer.id: customer for customer in customers}

    def get(self, customer_id: str) -> Customer:
        try:
            return self._customers[customer_id]
        except KeyError:
            raise CustomerNotFound(customer_id) from None

    def add(self, customer: Customer) -> None:
        self._customers[customer.id] = customer
