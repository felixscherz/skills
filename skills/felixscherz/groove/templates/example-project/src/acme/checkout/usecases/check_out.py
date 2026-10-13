"""Use case: issue an Invoice and charge the Customer, all or nothing.

Decide first, then do: every rule runs on loaded values before the first
write, and the unit of work makes the writes commit together.
"""

from acme.checkout.usecases.ports import CheckoutUnitOfWork
from acme.clock import Clock
from acme.customers import charge
from acme.ids import IdGenerator
from acme.invoicing import Invoice, InvoiceId, LineItem, draft, issue, total


def check_out(
    uow: CheckoutUnitOfWork,
    clock: Clock,
    ids: IdGenerator,
    customer_id: str,
    line_items: tuple[LineItem, ...],
) -> Invoice:
    with uow:
        customer = uow.customers.get(customer_id)
        invoice = issue(draft(InvoiceId(ids.new_id()), customer.id, line_items), now=clock.now())
        charged = charge(customer, total(invoice))
        uow.invoices.add(invoice)
        uow.customers.add(charged)
        uow.commit()
    return invoice
