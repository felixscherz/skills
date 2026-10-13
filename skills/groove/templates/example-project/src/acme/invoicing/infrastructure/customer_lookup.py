"""Answers invoicing's CustomerLookup from the customers module.

The only file in invoicing that imports another context, through its public
API. It translates customers' model into what invoicing needs, so a change in
customers stops here. The import is a declared exception in the layers
contract in pyproject.toml.
"""

from acme.customers import CustomerNotFound, CustomerRepository


class CustomerRepositoryLookup:
    def __init__(self, customers: CustomerRepository) -> None:
        self._customers = customers

    def exists(self, customer_id: str) -> bool:
        try:
            self._customers.get(customer_id)
        except CustomerNotFound:
            return False
        return True
