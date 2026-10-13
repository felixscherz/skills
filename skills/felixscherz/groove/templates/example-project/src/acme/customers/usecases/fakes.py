"""Fakes for customers' ports. Tests in every module use these, not mocks."""

from acme.customers.domain.model import Customer
from acme.customers.usecases.ports import CustomerNotFound


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
