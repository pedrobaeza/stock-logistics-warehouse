# -*- coding: utf-8 -*-
# © 2015 AvanzOSC
# © 2015-2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, exceptions, _


class StockInventory(models.Model):
    _inherit = "stock.inventory"

    @api.model
    def _get_available_filters(self):
        res = super(StockInventory, self)._get_available_filters()
        res.append(('file', _('By File')))
        return res

    @api.depends('import_lines')
    def _file_lines_processed(self):
        processed = True
        if self.import_lines:
            processed = any((not line.fail or
                             (line.fail and
                              line.fail_reason != _('No processed')))
                            for line in self.import_lines)
        self.processed = processed

    imported = fields.Boolean('Imported')
    import_lines = fields.One2many('stock.inventory.import.line',
                                   'inventory_id', string='Imported Lines')
    filter = fields.Selection(_get_available_filters,
                              string='Selection Filter',
                              required=True)
    processed = fields.Boolean(string='Has been processed at least once?',
                               compute='_file_lines_processed')

    @api.one
    def process_import_lines(self):
        """Process Inventory Load lines."""
        if not self.import_lines:
            raise exceptions.Warning(_("There must be one line at least to "
                                       "process"))
        stk_lot_obj = self.env['stock.production.lot']
        for line in self.import_lines.filtered('fail'):
            if not line.product:
                line.product = self.env['product.product'].search(
                    [('default_code', '=', line.code)], limit=1)
                if not line.product:
                    line.fail_reason = _('No product code found')
                    continue
            line.fail = False
        for line in self.import_lines.filtered(lambda x: not x.fail):
            lot = stk_lot_obj
            if line.lot:
                lot = stk_lot_obj.search([('name', '=', line.lot)], limit=1)
                if not lot:
                    lot = stk_lot_obj.create({
                        'name': line.lot,
                        'product_id': line.product.id,
                    })
            self.env['stock.inventory.line'].create({
                'product_id': line.product.id,
                'product_uom_id': line.product.uom_id.id,
                'product_qty': line.quantity,
                'inventory_id': self.id,
                'location_id': line.location_id.id,
                'prod_lot_id': lot.id,
            })
            line.fail_reason = _('Processed')
        return True

    @api.multi
    def action_done(self):
        for inventory in self:
            if not inventory.processed:
                raise exceptions.Warning(
                    _("Loaded lines must be processed at least one time for "
                      "inventory : %s") % (inventory.name))
            super(StockInventory, inventory).action_done()
