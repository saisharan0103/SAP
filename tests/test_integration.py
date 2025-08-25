import unittest

from erp import (
    PurchaseRequisition,
    PurchaseOrder,
    GoodsReceipt,
    Inventory,
)


class TestProcurementLifecycle(unittest.TestCase):
    def test_full_lifecycle(self):
        inventory = Inventory()

        pr = PurchaseRequisition(id="PR1", item="Widget", quantity=10)
        self.assertEqual(len(pr.gl_postings), 1)

        po = PurchaseOrder(
            id="PO1", requisition=pr, vendor="ACME", price=5.0
        )
        self.assertEqual(len(po.gl_postings), 1)

        gr = GoodsReceipt(id="GR1", purchase_order=po, quantity=10, inventory=inventory)
        self.assertEqual(inventory.stock.get("Widget"), 10)
        self.assertIsNotNone(gr.vendor_invoice)
        self.assertEqual(len(gr.gl_postings), 2)

        invoice = gr.vendor_invoice
        self.assertEqual(len(invoice.gl_postings), 2)

        all_entries = (
            pr.gl_postings
            + po.gl_postings
            + gr.gl_postings
            + invoice.gl_postings
        )
        total_debits = sum(e.debit for e in all_entries)
        total_credits = sum(e.credit for e in all_entries)
        self.assertEqual(total_debits, total_credits)


if __name__ == "__main__":
    unittest.main()
