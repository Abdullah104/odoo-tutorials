from dateutil.relativedelta import relativedelta

from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_utils


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real estate property'

    name = fields.Char(required=True, string="Title")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.today() + relativedelta(months=3),
                                    string="Available From")
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'),
                   ('sold', 'Sold'), ('cancelled', 'Cancelled')], copy=False, default='new')
    property_type_id = fields.Many2one('estate.property.type')
    buyer_id = fields.Many2one('res.partner', copy=False)
    salesperson_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    total_area = fields.Integer(compute='_compute_total_area', string='Total Area (sqm)')
    best_price = fields.Float(compute='_compute_best_price')
    line_ids = fields.One2many('estate.property.line', 'property_id')
    _check_expected_price = models.Constraint('CHECK(expected_price > 0)',
                                              'The expected price of a property should be strictly positive (larger than zero)')
    _check_selling_price = models.Constraint('CHECK(selling_price >= 0)',
                                             'The selling price of a property should be positive (larger than or equal to zero)')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price')) if record.offer_ids else 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'

            return {'warning': {'title': 'Garden', 'message': 'Garden area and orientation have changed'}}
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def action_sell_property(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError('A cancelled property cannot be set as sold')

            record.state = 'sold'

        return True

    def action_cancel_property(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('A sold property cannot be set as cancelled')

            record.state = 'cancelled'

        return True

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if float_utils.float_is_zero(record.selling_price, precision_rounding=2):
                continue

            if float_utils.float_compare(record.selling_price, record.expected_price * .9, precision_rounding=2) == -1:
                raise ValidationError('The selling price cannot be less than 90% of the expected price')


class EstatePropertyLine(models.Model):
    _name = 'estate.property.line'
    _description = 'Estate property line'

    property_id = fields.Many2one('estate.property')
    name = fields.Char()
    expected_price = fields.Char()
    state = fields.Char()
