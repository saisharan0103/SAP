from erp import ap, ar, inventory, gl


def test_ap_workflow():
    vendor_id = ap.add_vendor("Acme")
    invoice_id = ap.record_invoice(vendor_id, 100, "2024-01-01")
    ap.pay_invoice(invoice_id, 100, "2024-01-05")
    tb = gl.trial_balance()
    assert tb["5000"] == 100  # expense
    assert tb["2000"] == 0    # AP cleared


def test_ar_workflow():
    cust_id = ar.add_customer("Customer")
    inv_id = ar.record_invoice(cust_id, 200, "2024-02-01")
    ar.receive_payment(inv_id, 200, "2024-02-10")
    tb = gl.trial_balance()
    assert tb["4000"] == -200  # revenue credit
    assert tb["3000"] == 0     # AR cleared
    assert tb["1000"] == 200   # cash


def test_inventory_flow():
    item_id = inventory.add_item("SKU1", "Test Item")
    vendor_id = ap.add_vendor("Supplier")
    invoice_id = inventory.receive_goods(item_id, 5, 10, "2024-03-01", vendor_id)
    # pay vendor to close AP
    ap.pay_invoice(invoice_id, 50, "2024-03-05")
    inventory.issue_goods(item_id, 2, 10, "2024-03-10")
    assert inventory.stock_on_hand(item_id) == 3
    tb = gl.trial_balance()
    assert tb["1200"] == 30  # inventory 3*10
    assert tb["6000"] == 20  # cogs 2*10
