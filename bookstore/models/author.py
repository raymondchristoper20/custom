from odoo import models, fields, api, exceptions, _
# _ untuk translate

class author(models.Model):
    _name = 'bookstore.author'
    _description = 'data master of authors'
    _rec_name = 'name'
    _order = 'name asc'

    name = fields.Char('Name', size=64, required=True, index=True, readonly=True,
                      states={'draft': [('readonly', False)]})
    number = fields.Char('Number', size=64, required=True, index=True, readonly=True,
                       states={'draft': [('readonly', False)]})
    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),], 'State', required=True, readonly=True,
                             default='draft')

    def action_confirmed(self):
        self.state = 'confirmed'

    def action_settodraft(self):
        self.state = 'draft'