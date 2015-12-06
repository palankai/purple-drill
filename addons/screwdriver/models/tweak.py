from openerp import models, fields


class Tweak(models.Model):
    _name = 'screwdriver.tweak'

    name = fields.Char(string="Name", size=250, required=True)
