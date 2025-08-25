from data.db import get_connection


def add_entry(name: str, amount: float) -> None:
    """Insert an entry into the general ledger."""
    with get_connection() as conn:
        conn.execute('INSERT INTO ledger (name, amount) VALUES (?, ?)', (name, amount))
        conn.commit()


def summary() -> dict:
    """Return a summary of ledger entries."""
    with get_connection() as conn:
        cursor = conn.execute('SELECT COUNT(*), COALESCE(SUM(amount), 0) FROM ledger')
        count, total = cursor.fetchone()
    return {"entries": count, "total": total}
