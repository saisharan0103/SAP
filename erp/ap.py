from .database import get_connection
from .gl import post_journal_entry

AP_ACCOUNT = "2000"
CASH_ACCOUNT = "1000"
EXPENSE_ACCOUNT = "5000"


def add_vendor(name: str, terms: str | None = None) -> int:
    conn = get_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO vendors(name, terms) VALUES (?, ?)", (name, terms))
        return cur.lastrowid


def record_invoice(vendor_id: int, amount: float, date: str) -> int:
    entry_id = post_journal_entry(
        date,
        f"Vendor invoice {vendor_id}",
        [
            {"account": EXPENSE_ACCOUNT, "debit": amount},
            {"account": AP_ACCOUNT, "credit": amount},
        ],
    )
    conn = get_connection()
    with conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO vendor_invoices(vendor_id, amount, status, gl_entry_id) VALUES (?, ?, ?, ?)",
            (vendor_id, amount, "open", entry_id),
        )
        return cur.lastrowid


def pay_invoice(invoice_id: int, amount: float, date: str) -> int:
    entry_id = post_journal_entry(
        date,
        f"Payment for vendor invoice {invoice_id}",
        [
            {"account": AP_ACCOUNT, "debit": amount},
            {"account": CASH_ACCOUNT, "credit": amount},
        ],
    )
    conn = get_connection()
    with conn:
        cur = conn.cursor()
        cur.execute(
            "UPDATE vendor_invoices SET status=? WHERE id=?", ("paid", invoice_id)
        )
        cur.execute(
            "INSERT INTO payments(invoice_id, amount, gl_entry_id) VALUES (?, ?, ?)",
            (invoice_id, amount, entry_id),
        )
        return cur.lastrowid
