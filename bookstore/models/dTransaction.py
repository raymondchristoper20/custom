from odoo import models, fields, api, _
# _ untuk translate

class dTransaction(models.Model):
    _name = 'bookstore.dtransaction'
    _description = 'data of bookstore dTransaction'
    _rec_name = 'code'
    _order = 'code desc'

    title = fields.Many2one('bookstore.book', string='Title', required=True, index=True, readonly=True,
                states={'draft': [('readonly', False)]}, domain="[('state', '=', 'confirmed')]", ondelete="cascade")
    code = fields.Char('Book Code', related='title.code', store=True)
    price = fields.Integer('Price(Rp)', related='title.price', store=True)
    discount = fields.Integer('Discount(%)', related='title.discount', store=True)
    quantity = fields.Integer('Quantity', required=True, index=True, readonly=True,
                           states={'draft': [('readonly', False)]})
    subtotal = fields.Integer('Subtotal(Rp)', compute="_compute_subtotal", store=True, default=0)
    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),], 'State', required=True, readonly=True,
                             default='draft')
    transaction_id = fields.Many2one('bookstore.transaction', string='Transaction ID', index=True, readonly=True,
                            ondelete="cascade")

    @api.depends('price', 'quantity', 'discount')
    def _compute_subtotal(self):
        if self.quantity:
            self.subtotal = self.quantity * self.price * (100 - self.discount) / 100

    def action_settodraft(self):
        self.state = 'draft'

    def action_confirmed(self):
        self.state = 'confirmed'