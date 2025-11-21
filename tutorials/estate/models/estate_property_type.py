from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'

    name = fields.Char(required=True)
    _check_name = models.Constraint('UNIQUE(name)', 'The name of a property type must be unique')
