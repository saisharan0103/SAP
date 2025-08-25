from datetime import date
from typing import Dict

from erp.ar import ARLedger


def generate_aging_report(ledger: ARLedger, as_of: date) -> Dict[str, float]:
    """Proxy to ledger aging report for reporting layer."""
    return ledger.aging_report(as_of)
