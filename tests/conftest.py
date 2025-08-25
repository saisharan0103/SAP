import os
import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from erp.database import DB_PATH, init_db
from erp.gl import seed_chart_of_accounts


@pytest.fixture(autouse=True)
def _init_db():
    if DB_PATH.exists():
        os.remove(DB_PATH)
    init_db()
    seed_chart_of_accounts()
    yield
    if DB_PATH.exists():
        os.remove(DB_PATH)
