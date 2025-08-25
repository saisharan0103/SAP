from dataclasses import dataclass
from typing import Dict, List, Tuple


class Inventory:
    """Simple in-memory inventory of items and prices."""

    def __init__(self):
        self.stock: Dict[str, int] = {}
        self.prices: Dict[str, float] = {}

    def add_item(self, item: str, quantity: int, price: float) -> None:
        self.stock[item] = self.stock.get(item, 0) + quantity
        self.prices[item] = price

    def remove_item(self, item: str, quantity: int) -> None:
        available = self.stock.get(item, 0)
        if quantity > available:
            raise ValueError("Insufficient inventory for item %s" % item)
        self.stock[item] = available - quantity


@dataclass
class SalesOrderLine:
    item: str
    quantity: int


class SalesOrder:
    """Represents a customer order which can be partially delivered."""

    def __init__(self, order_id: str, customer: str, inventory: Inventory):
        self.order_id = order_id
        self.customer = customer
        self.inventory = inventory
        self.lines: List[SalesOrderLine] = []
        # Track delivered quantity for each item
        self.delivered: Dict[str, int] = {}

    def add_line(self, item: str, quantity: int) -> None:
        self.lines.append(SalesOrderLine(item, quantity))
        self.delivered.setdefault(item, 0)

    def deliver(self, delivery_id: str, items: Dict[str, int]) -> "DeliveryNote":
        """Deliver specified quantities and create a delivery note."""
        return DeliveryNote(delivery_id, self, items)


class ARInvoice:
    """Accounts receivable invoice generated from a delivery."""

    _next_id = 1

    def __init__(self, customer: str, lines: List[Tuple[str, int, float]]):
        self.invoice_id = ARInvoice._next_id
        ARInvoice._next_id += 1
        self.customer = customer
        self.lines = lines
        self.amount = sum(qty * price for _, qty, price in lines)
        self.balance = self.amount

    def apply_receipt(self, amount: float) -> None:
        if amount < 0:
            raise ValueError("Amount must be positive")
        if amount > self.balance:
            raise ValueError("Receipt exceeds outstanding balance")
        self.balance -= amount


class Receipt:
    """Customer receipt applied to an invoice."""

    def __init__(self, invoice: ARInvoice, amount: float):
        self.invoice = invoice
        self.amount = amount
        invoice.apply_receipt(amount)


class DeliveryNote:
    """Represents delivery of items from a sales order.

    Reduces inventory and automatically creates an AR invoice for the
    delivered goods."""

    def __init__(self, delivery_id: str, order: SalesOrder, items: Dict[str, int]):
        self.delivery_id = delivery_id
        self.order = order
        self.items = items
        self.inventory = order.inventory
        self.invoice = self._process()

    def _process(self) -> ARInvoice:
        invoice_lines: List[Tuple[str, int, float]] = []
        for item, qty in self.items.items():
            # Validate quantity
            ordered = next((line.quantity for line in self.order.lines if line.item == item), 0)
            delivered = self.order.delivered.get(item, 0)
            remaining = ordered - delivered
            if qty > remaining:
                raise ValueError("Cannot deliver more than ordered for %s" % item)
            # Reduce inventory
            self.inventory.remove_item(item, qty)
            # Update delivered quantity on order
            self.order.delivered[item] = delivered + qty
            # Prepare invoice line
            price = self.inventory.prices[item]
            invoice_lines.append((item, qty, price))
        return ARInvoice(self.order.customer, invoice_lines)
