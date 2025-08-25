import sys
from pathlib import Path

# Ensure the package can be imported when running tests directly
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sap.models import Inventory, SalesOrder, Receipt


def test_partial_deliveries_and_receipts():
    inv = Inventory()
    inv.add_item('widget', 10, 5.0)

    order = SalesOrder('SO1', 'Cust', inv)
    order.add_line('widget', 10)

    # First partial delivery
    dn1 = order.deliver('DN1', {'widget': 6})
    assert inv.stock['widget'] == 4
    assert dn1.invoice.amount == 30.0
    assert dn1.invoice.balance == 30.0

    # Second delivery completes the order
    dn2 = order.deliver('DN2', {'widget': 4})
    assert inv.stock['widget'] == 0
    assert dn2.invoice.amount == 20.0
    assert order.delivered['widget'] == 10

    # Partial receipt against first invoice
    Receipt(dn1.invoice, 10.0)
    assert dn1.invoice.balance == 20.0
    Receipt(dn1.invoice, 20.0)
    assert dn1.invoice.balance == 0.0

    # Receipt for second invoice clears it entirely
    Receipt(dn2.invoice, 20.0)
    assert dn2.invoice.balance == 0.0

