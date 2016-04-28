# -*- coding: utf-8 -*-
# © 2015 AvanzOSC
# © 2015-2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Stock Inventory Import from CSV file",
    "version": "1.0",
    "category": "Generic Modules",
    "author": "OdooMRP team, "
              "AvanzOSC, "
              "Tecnativa, "
              "Odoo Community Association (OCA)",
    'license': 'AGPL-3',
    "website": "http://www.odoomrp.com",
    "depends": [
        "stock",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizard/import_inventory_view.xml",
        "views/inventory_view.xml",
    ],
    "installable": True,
}
