import sqlite3
from pathlib import Path

DB_PATH = Path('erp.db')

SCHEMA = [
    """
    CREATE TABLE IF NOT EXISTS accounts (
        code TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT NOT NULL,
        parent_code TEXT REFERENCES accounts(code)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS journal_entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        description TEXT,
        created_by TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS journal_lines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entry_id INTEGER NOT NULL REFERENCES journal_entries(id),
        account_code TEXT NOT NULL REFERENCES accounts(code),
        debit REAL NOT NULL DEFAULT 0,
        credit REAL NOT NULL DEFAULT 0
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS vendors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        terms TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        credit_limit REAL DEFAULT 0
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS vendor_invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vendor_id INTEGER NOT NULL REFERENCES vendors(id),
        amount REAL NOT NULL,
        status TEXT NOT NULL,
        gl_entry_id INTEGER REFERENCES journal_entries(id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS customer_invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL REFERENCES customers(id),
        amount REAL NOT NULL,
        status TEXT NOT NULL,
        gl_entry_id INTEGER REFERENCES journal_entries(id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        gl_entry_id INTEGER REFERENCES journal_entries(id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sku TEXT NOT NULL UNIQUE,
        description TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS stock_moves (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER NOT NULL REFERENCES items(id),
        quantity REAL NOT NULL,
        cost REAL NOT NULL,
        direction TEXT NOT NULL,
        date TEXT NOT NULL,
        gl_entry_id INTEGER REFERENCES journal_entries(id)
    )
    """,
]

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    for stmt in SCHEMA:
        cur.execute(stmt)
    conn.commit()
    conn.close()
