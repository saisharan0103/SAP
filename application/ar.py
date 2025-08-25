from data.db import get_connection


def record_invoice(customer: str, amount: float) -> None:
    """Record an invoice in the ledger as a positive amount."""
    with get_connection() as conn:
        conn.execute(
            'INSERT INTO ledger (name, amount) VALUES (?, ?)',
            (f'AR:{customer}', abs(amount)),
        )
        conn.commit()
