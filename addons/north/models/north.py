from openerp import models, fields


class Step(models.Model):
    _name = 'north.step'

    name = fields.Char(string="Name", size=250, required=True)
