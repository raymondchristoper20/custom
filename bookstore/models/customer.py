from odoo import models, fields, api, _

class customer(models.Model):
    _inherit = 'res.partner'

    nik = fields.Char(string='Citizenship ID')
    member = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Member', default='no')