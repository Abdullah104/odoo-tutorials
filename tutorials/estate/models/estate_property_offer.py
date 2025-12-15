from dateutil.relativedelta import relativedelta

from odoo import api, models, fields
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(string='Validity (days)')
    create_date = fields.Date()
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    property_type_id = fields.Many2one(related='property_id.property_type_id')

    _check_price = models.Constraint('CHECK(price > 0)',
                                     'The price of an offer should be strictly positive (larger than zero)')

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            property = self.env['estate.property'].browse(vals['property_id'])

            if property.state == 'new':
                property.state = 'offer_received'

        return super().create(vals_list)

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = record.create_date if record.create_date else fields.Date.today() + relativedelta(
                days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (
                record.date_deadline - record.create_date if record.create_date else fields.Date.today()).days

    def action_accept_offer(self):
        accepted_offer_exists = self.property_id.state == 'offer_accepted'

        if accepted_offer_exists:
            raise UserError('An accepted offer already exists')

        for record in self:
            record.property_id.selling_price = self.price
            record.property_id.state = 'offer_accepted'

            record.status = 'accepted'

        return True

    def action_refuse_offer(self):
        for record in self:
            record.status = 'refused'

        return True
