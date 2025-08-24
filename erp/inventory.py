from .database import get_connection
from .gl import post_journal_entry

INVENTORY_ACCOUNT = "1200"
COGS_ACCOUNT = "6000"
AP_ACCOUNT = "2000"


def add_item(sku: str, description: str | None = None) -> int:
    conn = get_connection()
    with conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO items(sku, description) VALUES (?, ?)", (sku, description)
        )
        return cur.lastrowid


def receive_goods(item_id: int, quantity: float, cost: float, date: str, vendor_id: int):
    total = quantity * cost
    entry_id = post_journal_entry(
        date,
        f"Goods receipt for item {item_id}",
        [
            {"account": INVENTORY_ACCOUNT, "debit": total},
            {"account": AP_ACCOUNT, "credit": total},
        ],
    )
    conn = get_connection()
    with conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO stock_moves(item_id, quantity, cost, direction, date, gl_entry_id) VALUES (?, ?, ?, ?, ?, ?)",
            (item_id, quantity, cost, "in", date, entry_id),
        )
        cur.execute(
            "INSERT INTO vendor_invoices(vendor_id, amount, status, gl_entry_id) VALUES (?, ?, ?, ?)",
            (vendor_id, total, "open", entry_id),
        )
        return cur.lastrowid


def issue_goods(item_id: int, quantity: float, cost: float, date: str, customer_invoice_id: int | None = None):
    total = quantity * cost
    entry_id = post_journal_entry(
        date,
        f"Goods issue for item {item_id}",
        [
            {"account": COGS_ACCOUNT, "debit": total},
            {"account": INVENTORY_ACCOUNT, "credit": total},
        ],
    )
    conn = get_connection()
    with conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO stock_moves(item_id, quantity, cost, direction, date, gl_entry_id) VALUES (?, ?, ?, ?, ?, ?)",
            (item_id, quantity, cost, "out", date, entry_id),
        )
        return cur.lastrowid


def stock_on_hand(item_id: int) -> float:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT SUM(CASE WHEN direction='in' THEN quantity ELSE -quantity END) FROM stock_moves WHERE item_id=?",
        (item_id,),
    )
    result = cur.fetchone()[0]
    return result or 0.0
