import sys
from pathlib import Path
from datetime import date

# ensure project root on path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from erp.ar import ARLedger
from reporting.ar import generate_aging_report


def test_partial_delivery_and_payment_workflow():
    ledger = ARLedger()
    cust = ledger.add_customer("ACME", credit_limit=1000)
    order = ledger.create_sales_order(cust, amount_total=800)

    # first partial delivery and early payment with discount
    inv1 = ledger.confirm_delivery(order, amount=400, delivery_date=date(2024, 1, 1))
    ledger.post_receipt(inv1, amount=392, pay_date=date(2024, 1, 6))
    assert inv1.status == "paid"
    # after early payment balance reset
    assert cust.balance == 0

    # second delivery and partial late payment
    inv2 = ledger.confirm_delivery(order, amount=400, delivery_date=date(2024, 1, 10))
    ledger.post_receipt(inv2, amount=200, pay_date=date(2024, 2, 20))
    assert inv2.status == "open"
    assert inv2.open_amount == 200

    # aging report as of payment date (41 days after invoice2)
    report = generate_aging_report(ledger, as_of=date(2024, 2, 20))
    assert report == {"0-30": 0.0, "31-60": 200.0, "61-90": 0.0, "90+": 0.0}
