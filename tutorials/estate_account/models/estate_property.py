from odoo import models, Command
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = ['estate.property']

    def action_sell_property(self):
        for record in self:
            self.env['account.move'].create(
                {'name': record.name,
                 'move_type': 'out_invoice',
                 'line_ids': [
                     Command.create({'name': 'Selling Price', 'price_unit': record.selling_price}),
                     Command.create({'name': 'Commission', 'price_unit': 100}),
                     Command.create(
                         {'name': 'Administrative Fees', 'price_unit': record.selling_price * 0.06}), ]})

        return super().action_sell_property()
