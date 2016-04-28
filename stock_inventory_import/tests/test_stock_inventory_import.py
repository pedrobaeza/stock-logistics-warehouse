# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests import common
from openerp import tools
import base64


class TestStockInventoryImport(common.TransactionCase):
    def setUp(self):
        super(TestStockInventoryImport, self).setUp()
        self.product = self.env['product.product'].create({
            'name': 'Test product',
            'default_code': 'TEST001',
        })
        self.warehouse = self.env['stock.warehouse'].create({
            'name': 'Test Warehouse',
            'code': 'TESTW',
        })
        self.inventory = self.env['stock.inventory'].create({
            'name': 'Test inventory',
            'location_id': self.warehouse.lot_stock_id.id,
        })
        f = tools.file_open('stock_inventory_import/tests/sample.csv')
        self.wizard = self.env['import.inventory'].create({
            'data': base64.b64encode(f.read()),
            'name': 'sample.csv',
            'location': self.inventory.location_id.id,
        })
        f.close()

    def test_import(self):
        self.wizard.with_context(active_id=self.inventory.id).action_import()
        self.assertEqual(len(self.inventory.import_lines), 2)
        self.inventory.process_import_lines()
        self.assertEqual(len(self.inventory.line_ids), 2)
        self.assertEqual(self.inventory.line_ids[0].product_qty, 2.5)
        self.assertEqual(self.inventory.line_ids[0].prod_lot_id.name, 'LOT001')
        self.assertEqual(self.inventory.line_ids[1].product_qty, 5)
        self.assertEqual(self.inventory.line_ids[1].prod_lot_id.name, 'LOT002')
