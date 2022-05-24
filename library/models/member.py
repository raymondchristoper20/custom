from odoo import models, fields, api, _
# _ untuk translate

class member(models.Model):
    _name = 'library.member'
    _description = 'data of library members'
    _rec_name = 'nik'
    _order = 'name asc'

    name = fields.Char('Name', size=64, required=True, index=True, readonly=True,
                         states={'draft': [('readonly', False)]})
    nik = fields.Char('Citizenship ID', size=64, required=True, index=True, readonly=True,
                       states={'draft': [('readonly', False)]})
    email = fields.Char('E-mail', required=True, index=True, readonly=True,
                      states={'draft': [('readonly', False)]})
    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),], 'State', required=True, readonly=True,
                             default='draft')
    _sql_constraints = [('nik_unique', 'unique(nik)', _('Citizenship ID must be unique!'))]


    def action_confirmed(self):
        self.state = 'confirmed'

    def action_settodraft(self):
        self.state = 'draft'