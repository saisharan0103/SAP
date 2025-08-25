from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List, Dict


@dataclass
class Customer:
    name: str
    credit_limit: float
    balance: float = 0.0


@dataclass
class SalesOrder:
    id: int
    customer: Customer
    amount_total: float
    delivered_amount: float = 0.0


@dataclass
class Delivery:
    id: int
    sales_order: SalesOrder
    amount: float
    date: date


@dataclass
class Invoice:
    id: int
    customer: Customer
    amount: float
    date: date
    due_date: date
    discount_rate: float = 0.0
    discount_days: int = 0
    open_amount: float = field(init=False)
    status: str = field(default="open")  # open, paid, written_off, disputed

    def __post_init__(self) -> None:
        self.open_amount = self.amount


class ARLedger:
    """Simple AR ledger handling order to cash flow."""

    def __init__(self) -> None:
        self.customers: Dict[str, Customer] = {}
        self.orders: List[SalesOrder] = []
        self.deliveries: List[Delivery] = []
        self.invoices: List[Invoice] = []
        self._order_seq = 1
        self._delivery_seq = 1
        self._invoice_seq = 1

    # Customer management
    def add_customer(self, name: str, credit_limit: float) -> Customer:
        customer = Customer(name=name, credit_limit=credit_limit)
        self.customers[name] = customer
        return customer

    # Sales order
    def create_sales_order(self, customer: Customer, amount_total: float) -> SalesOrder:
        if customer.balance + amount_total > customer.credit_limit:
            raise ValueError("Credit limit exceeded")
        order = SalesOrder(id=self._order_seq, customer=customer, amount_total=amount_total)
        self._order_seq += 1
        self.orders.append(order)
        return order

    # Delivery confirmation and invoice generation
    def confirm_delivery(self, sales_order: SalesOrder, amount: float, delivery_date: date) -> Invoice:
        if sales_order.delivered_amount + amount > sales_order.amount_total:
            raise ValueError("Cannot deliver more than ordered")
        delivery = Delivery(id=self._delivery_seq, sales_order=sales_order, amount=amount, date=delivery_date)
        self._delivery_seq += 1
        self.deliveries.append(delivery)
        sales_order.delivered_amount += amount
        invoice = self._generate_invoice(sales_order.customer, amount, delivery_date)
        return invoice

    def _generate_invoice(self, customer: Customer, amount: float, inv_date: date) -> Invoice:
        due = inv_date + timedelta(days=30)
        invoice = Invoice(
            id=self._invoice_seq,
            customer=customer,
            amount=amount,
            date=inv_date,
            due_date=due,
            discount_rate=0.02,
            discount_days=10,
        )
        self._invoice_seq += 1
        self.invoices.append(invoice)
        customer.balance += amount
        return invoice

    # Receipt posting
    def post_receipt(self, invoice: Invoice, amount: float, pay_date: date) -> None:
        if invoice.status != "open":
            raise ValueError("Cannot post receipt to closed invoice")
        discount = 0.0
        if (pay_date - invoice.date).days <= invoice.discount_days:
            discount = invoice.amount * invoice.discount_rate
        invoice.open_amount -= amount + discount
        invoice.customer.balance -= amount + discount
        if invoice.open_amount <= 0:
            invoice.status = "paid"
            invoice.open_amount = 0.0

    # Write-off and dispute handling
    def write_off(self, invoice: Invoice) -> None:
        if invoice.status != "open":
            raise ValueError("Only open invoices can be written off")
        invoice.status = "written_off"
        invoice.customer.balance -= invoice.open_amount
        invoice.open_amount = 0.0

    def dispute(self, invoice: Invoice) -> None:
        if invoice.status != "open":
            raise ValueError("Only open invoices can be disputed")
        invoice.status = "disputed"

    # AR aging report
    def aging_report(self, as_of: date) -> Dict[str, float]:
        buckets = {"0-30": 0.0, "31-60": 0.0, "61-90": 0.0, "90+": 0.0}
        for inv in self.invoices:
            if inv.status not in {"open", "disputed"} or inv.open_amount == 0:
                continue
            age = (as_of - inv.date).days
            amt = inv.open_amount
            if age <= 30:
                buckets["0-30"] += amt
            elif age <= 60:
                buckets["31-60"] += amt
            elif age <= 90:
                buckets["61-90"] += amt
            else:
                buckets["90+"] += amt
        return buckets
