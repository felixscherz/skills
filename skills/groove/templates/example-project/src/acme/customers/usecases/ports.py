"""Protocols through which customers' use cases reach the outside world."""

from typing import Protocol

from acme.customers.domain.model import Customer


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
