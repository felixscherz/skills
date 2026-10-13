"""Functional core: Customer values and the rules for changing them."""

from dataclasses import dataclass, replace
from decimal import Decimal


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
