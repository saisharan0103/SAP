from .database import get_connection
from .gl import post_journal_entry

AR_ACCOUNT = "3000"
CASH_ACCOUNT = "1000"
REVENUE_ACCOUNT = "4000"


def add_customer(name: str, credit_limit: float | None = 0) -> int:
    conn = get_connection()
    with conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO customers(name, credit_limit) VALUES (?, ?)", (name, credit_limit)
        )
        return cur.lastrowid


def record_invoice(customer_id: int, amount: float, date: str) -> int:
    entry_id = post_journal_entry(
        date,
        f"Customer invoice {customer_id}",
        [
            {"account": AR_ACCOUNT, "debit": amount},
            {"account": REVENUE_ACCOUNT, "credit": amount},
        ],
    )
    conn = get_connection()
    with conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO customer_invoices(customer_id, amount, status, gl_entry_id) VALUES (?, ?, ?, ?)",
            (customer_id, amount, "open", entry_id),
        )
        return cur.lastrowid


def receive_payment(invoice_id: int, amount: float, date: str) -> int:
    entry_id = post_journal_entry(
        date,
        f"Receipt for customer invoice {invoice_id}",
        [
            {"account": CASH_ACCOUNT, "debit": amount},
            {"account": AR_ACCOUNT, "credit": amount},
        ],
    )
    conn = get_connection()
    with conn:
        cur = conn.cursor()
        cur.execute(
            "UPDATE customer_invoices SET status=? WHERE id=?", ("paid", invoice_id)
        )
        cur.execute(
            "INSERT INTO payments(invoice_id, amount, gl_entry_id) VALUES (?, ?, ?)",
            (invoice_id, amount, entry_id),
        )
        return cur.lastrowid
