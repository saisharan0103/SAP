from __future__ import annotations
from typing import Iterable, Dict
from .database import get_connection, init_db

# account types: Asset, Liability, Equity, Revenue, Expense

def create_account(code: str, name: str, type_: str, parent_code: str | None = None) -> None:
    conn = get_connection()
    with conn:
        conn.execute(
            "INSERT INTO accounts(code, name, type, parent_code) VALUES (?, ?, ?, ?)",
            (code, name, type_, parent_code),
        )


def post_journal_entry(date: str, description: str, lines: Iterable[Dict], created_by: str = "system") -> int:
    total_debit = sum(line.get("debit", 0) for line in lines)
    total_credit = sum(line.get("credit", 0) for line in lines)
    if round(total_debit - total_credit, 2) != 0:
        raise ValueError("Journal entry is not balanced")

    conn = get_connection()
    with conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO journal_entries(date, description, created_by) VALUES (?, ?, ?)",
            (date, description, created_by),
        )
        entry_id = cur.lastrowid
        for line in lines:
            cur.execute(
                "INSERT INTO journal_lines(entry_id, account_code, debit, credit) VALUES (?, ?, ?, ?)",
                (
                    entry_id,
                    line["account"],
                    line.get("debit", 0),
                    line.get("credit", 0),
                ),
            )
    return entry_id


def trial_balance() -> Dict[str, float]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT account_code, SUM(debit) as debit, SUM(credit) as credit FROM journal_lines GROUP BY account_code"
    )
    rows = cur.fetchall()
    tb = {}
    for row in rows:
        tb[row["account_code"]] = row["debit"] - row["credit"]
    return tb


# convenience function to bootstrap minimal chart of accounts

def seed_chart_of_accounts():
    accounts = [
        ("1000", "Cash", "Asset", None),
        ("2000", "Accounts Payable", "Liability", None),
        ("3000", "Accounts Receivable", "Asset", None),
        ("4000", "Revenue", "Revenue", None),
        ("5000", "Expense", "Expense", None),
        ("1200", "Inventory", "Asset", None),
        ("6000", "Cost of Goods Sold", "Expense", None),
    ]
    for acc in accounts:
        try:
            create_account(*acc)
        except Exception:
            pass


if __name__ == "__main__":
    init_db()
    seed_chart_of_accounts()
