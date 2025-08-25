import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from erp.inventory import Inventory, InventoryError


def test_negative_stock():
    inv = Inventory()
    inv.add_item('ITEM1', 'Cat', 'Nos')
    inv.receive('ITEM1', 10, 5)
    with pytest.raises(InventoryError):
        inv.issue('ITEM1', 15)


def test_fifo_costing():
    inv = Inventory()
    inv.add_item('ITEM1', 'Cat', 'Nos')
    inv.receive('ITEM1', 10, 5)
    inv.receive('ITEM1', 5, 6)
    cost = inv.issue('ITEM1', 12)
    assert cost == pytest.approx(62)
    valuation = inv.stock_valuation()['ITEM1']
    assert valuation['qty'] == pytest.approx(3)
    assert valuation['value'] == pytest.approx(18)
