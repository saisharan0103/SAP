from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).resolve().parent / "sap.db"
MIGRATIONS_PATH = Path(__file__).resolve().parent / "migrations"


def get_connection() -> sqlite3.Connection:
    """Return a connection to the SQLite database."""
    return sqlite3.connect(DB_PATH)


def run_migrations() -> None:
    """Apply SQL migration scripts in order."""
    with get_connection() as conn:
        for migration in sorted(MIGRATIONS_PATH.glob("*.sql")):
            conn.executescript(migration.read_text())
        conn.commit()
