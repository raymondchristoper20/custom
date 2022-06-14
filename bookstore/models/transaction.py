from odoo import models, fields, api, _
# _ untuk translate
from server.odoo import exceptions


class transaction(models.Model):
    _name = 'bookstore.transaction'
    _description = 'data of bookstore transaction'
    _rec_name = 'date'
    _order = 'date desc'

    number = fields.Char('Transaction Number', size=64, index=True, readonly=True, default='New Number',
                          states={'draft': [('readonly', False)]})
    nik = fields.Many2one('res.partner', string='Customer', required=True, index=True, readonly=True,
                       states={'draft': [('readonly', False)]}, ondelete="cascade")
    date = fields.Date('Date', required=True, index=True, default=fields.Date.context_today, readonly=True,
                      states={'draft': [('readonly', False)]})

    total = fields.Integer('Total(Rp)', compute="_compute_total", store=True, default=0)

    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),], 'State', required=True, readonly=True,
                             default='draft')
    dTransaction_ids = fields.One2many('bookstore.dtransaction', 'transaction_id', string='Detail of Transaction(s)',
                                        default=0)

    @api.depends('dTransaction_ids', 'nik')
    def _compute_total(self):
        for x in self:
            x.total = sum(x.dTransaction_ids.mapped('subtotal'))
            if x.nik.member == 'yes':
                x.total = x.total * 90 / 100

    def action_settodraft(self):
        self.state = 'draft'
        self.update_stock('add')

    def action_confirmed(self):
        self.state = 'confirmed'
        self.update_stock('minus')

    def update_stock(self, mode):
        if mode == 'minus':
            for x in self.dTransaction_ids:
                y = self.env['bookstore.book'].search([('id', '=', x.title.id)])
                if y.quantity - x.quantity < 0:
                    raise exceptions.UserError(_("Some of the book is not available, please try again"))

        for x in self.dTransaction_ids:
            y = self.env['bookstore.book'].search([('id', '=', x.title.id)])
            if mode == 'add':
                z = y.quantity + x.quantity
            else:
                z = y.quantity - x.quantity
            y.write({'quantity': z})