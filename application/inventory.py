from data.db import get_connection


def add_item(name: str, quantity: int) -> None:
    """Add an item to inventory."""
    with get_connection() as conn:
        conn.execute(
            'INSERT INTO inventory (name, quantity) VALUES (?, ?)',
            (name, quantity),
        )
        conn.commit()
