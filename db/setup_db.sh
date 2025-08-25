#!/usr/bin/env bash
# Initialize SQLite database and load seed data
set -e
DB_FILE=${1:-sap.db}
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Initializing database: $DB_FILE"
sqlite3 "$DB_FILE" < "$SCRIPT_DIR/schema.sql"
sqlite3 "$DB_FILE" < "$SCRIPT_DIR/seed_data.sql"
echo "Seed data loaded into $DB_FILE"
