from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _order= 'name'

    name = fields.Char(required=True)
    _check_name = models.Constraint('UNIQUE(name)', 'The name of a tag must be unique')

    color = fields.Integer()
