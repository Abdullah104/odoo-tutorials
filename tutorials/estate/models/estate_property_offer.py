from dateutil.relativedelta import relativedelta

from odoo import api, models, fields


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'

    price = fields.Float()
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(string='Validity (days)')
    create_date = fields.Date()
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = self.create_date if self.create_date else fields.Date.today() + relativedelta(
                days=self.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (
                record.date_deadline - record.create_date if record.create_date else fields.Date.today()).days
