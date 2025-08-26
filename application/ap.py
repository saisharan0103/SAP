from data.db import get_connection


def record_bill(vendor: str, amount: float) -> None:
    """Record a bill in the ledger as a negative amount."""
    with get_connection() as conn:
        conn.execute(
            'INSERT INTO ledger (name, amount) VALUES (?, ?)',
            (f'AP:{vendor}', -abs(amount)),
        )
        conn.commit()
