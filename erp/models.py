from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class GLPosting:
    """Represents a general ledger posting."""
    account: str
    debit: float = 0.0
    credit: float = 0.0
    description: str = ""


@dataclass
class PurchaseRequisition:
    """Request to purchase goods or services."""
    id: str
    item: str
    quantity: int
    gl_postings: List[GLPosting] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.gl_postings.append(
            GLPosting(
                account="Commitment",
                description=f"Purchase requisition {self.id} created",
            )
        )


@dataclass
class PurchaseOrder:
    """Order placed with a vendor to fulfill a requisition."""
    id: str
    requisition: PurchaseRequisition
    vendor: str
    price: float
    gl_postings: List[GLPosting] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.gl_postings.append(
            GLPosting(
                account="PO Commitment",
                description=f"Purchase order {self.id} created",
            )
        )


@dataclass
class Inventory:
    """Simple in-memory inventory tracker."""
    stock: Dict[str, int] = field(default_factory=dict)

    def add(self, item: str, quantity: int) -> None:
        self.stock[item] = self.stock.get(item, 0) + quantity


@dataclass
class GoodsReceipt:
    """Receipt of goods against a purchase order."""
    id: str
    purchase_order: PurchaseOrder
    quantity: int
    inventory: Inventory
    gl_postings: List[GLPosting] = field(default_factory=list)
    vendor_invoice: VendorInvoice | None = None

    def __post_init__(self) -> None:
        # Update inventory
        self.inventory.add(self.purchase_order.requisition.item, self.quantity)

        amount = self.purchase_order.price * self.quantity
        # GL posting for inventory increase
        self.gl_postings.append(
            GLPosting(
                account="Inventory",
                debit=amount,
                description=f"Goods receipt {self.id}",
            )
        )
        # GL posting for GR/IR liability
        self.gl_postings.append(
            GLPosting(
                account="GR/IR",
                credit=amount,
                description=f"Goods receipt {self.id}",
            )
        )

        # Automatically generate vendor invoice
        self.vendor_invoice = VendorInvoice(goods_receipt=self, amount=amount)


@dataclass
class VendorInvoice:
    """Invoice received from vendor after goods receipt."""
    goods_receipt: GoodsReceipt
    amount: float
    gl_postings: List[GLPosting] = field(default_factory=list)

    def __post_init__(self) -> None:
        # Clear GR/IR liability
        self.gl_postings.append(
            GLPosting(
                account="GR/IR",
                debit=self.amount,
                description=f"Invoice for GR {self.goods_receipt.id}",
            )
        )
        # Record accounts payable
        self.gl_postings.append(
            GLPosting(
                account="Accounts Payable",
                credit=self.amount,
                description=f"Invoice for GR {self.goods_receipt.id}",
            )
        )
