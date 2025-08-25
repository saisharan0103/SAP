from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from collections import deque
from typing import Deque, Dict, List, Optional


@dataclass
class Item:
    """Item master record."""

    code: str
    category: str
    uom: str
    costing_method: str = "FIFO"


class InventoryError(Exception):
    """Raised when inventory operations fail."""


@dataclass
class LedgerEntry:
    date: datetime
    item_code: str
    tran_type: str
    qty: float
    rate: float
    balance_qty: float
    balance_value: float


class Inventory:
    """Inventory management with FIFO costing and simple GL posting."""

    def __init__(self) -> None:
        self.items: Dict[str, Item] = {}
        # FIFO layers per item: deque of (qty, rate)
        self.layers: Dict[str, Deque[List[float]]] = {}
        # stock ledger entries per item
        self.ledger: Dict[str, List[LedgerEntry]] = {}
        # Simple general ledger
        self.gl: Dict[str, float] = {"Inventory": 0.0, "COGS": 0.0}

    # ------------------------------------------------------------------
    # Item master
    # ------------------------------------------------------------------
    def add_item(
        self,
        code: str,
        category: str,
        uom: str,
        costing_method: str = "FIFO",
    ) -> None:
        if code in self.items:
            raise InventoryError(f"Item {code} already exists")
        self.items[code] = Item(code, category, uom, costing_method)
        self.layers[code] = deque()
        self.ledger[code] = []

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _current_balance(self, item_code: str) -> (float, float):
        layers = self.layers[item_code]
        qty = sum(q for q, _ in layers)
        value = sum(q * r for q, r in layers)
        return qty, value

    def _add_ledger_entry(
        self,
        item_code: str,
        tran_type: str,
        qty: float,
        rate: float,
        date: Optional[datetime] = None,
    ) -> None:
        bal_qty, bal_val = self._current_balance(item_code)
        entry = LedgerEntry(
            date=date or datetime.now(),
            item_code=item_code,
            tran_type=tran_type,
            qty=qty,
            rate=rate,
            balance_qty=bal_qty,
            balance_value=bal_val,
        )
        self.ledger[item_code].append(entry)

    # ------------------------------------------------------------------
    # Transactions
    # ------------------------------------------------------------------
    def receive(
        self, item_code: str, qty: float, rate: float, date: Optional[datetime] = None
    ) -> float:
        if item_code not in self.items:
            raise InventoryError(f"Unknown item {item_code}")
        if qty <= 0:
            raise InventoryError("Quantity must be positive")
        self.layers[item_code].append([qty, rate])
        # GL posting: debit inventory
        self.gl["Inventory"] += qty * rate
        self._add_ledger_entry(item_code, "GR", qty, rate, date)
        return qty * rate

    def issue(
        self, item_code: str, qty: float, date: Optional[datetime] = None
    ) -> float:
        if item_code not in self.items:
            raise InventoryError(f"Unknown item {item_code}")
        if qty <= 0:
            raise InventoryError("Quantity must be positive")
        layers = self.layers[item_code]
        remaining = qty
        cost = 0.0
        while remaining > 0 and layers:
            layer_qty, layer_rate = layers[0]
            if layer_qty <= remaining:
                cost += layer_qty * layer_rate
                remaining -= layer_qty
                layers.popleft()
            else:
                cost += remaining * layer_rate
                layers[0][0] = layer_qty - remaining
                remaining = 0
        if remaining > 0:
            raise InventoryError("Insufficient stock")
        avg_rate = cost / qty
        # GL posting: credit inventory, debit COGS
        self.gl["Inventory"] -= cost
        self.gl["COGS"] += cost
        self._add_ledger_entry(item_code, "GI", -qty, avg_rate, date)
        return cost

    def transfer(
        self,
        item_code: str,
        qty: float,
        date: Optional[datetime] = None,
    ) -> None:
        """Record a stock transfer (same warehouse for simplicity)."""
        # For this simplified implementation we just record a ledger entry.
        if item_code not in self.items:
            raise InventoryError(f"Unknown item {item_code}")
        if qty <= 0:
            raise InventoryError("Quantity must be positive")
        bal_qty, bal_val = self._current_balance(item_code)
        if qty > bal_qty:
            raise InventoryError("Insufficient stock for transfer")
        self._add_ledger_entry(item_code, "TR", 0, 0.0, date)

    # ------------------------------------------------------------------
    # Reports
    # ------------------------------------------------------------------
    def stock_valuation(self) -> Dict[str, Dict[str, float]]:
        report: Dict[str, Dict[str, float]] = {}
        for item_code in self.items:
            qty, value = self._current_balance(item_code)
            report[item_code] = {"qty": qty, "value": value}
        return report

    def stock_ledger(self, item_code: str) -> List[LedgerEntry]:
        if item_code not in self.items:
            raise InventoryError(f"Unknown item {item_code}")
        return list(self.ledger[item_code])

