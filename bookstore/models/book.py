from odoo import models, fields, api, exceptions, _
# _ untuk translate

class book(models.Model):
    _name = 'bookstore.book'
    _description = 'data master of books'
    _rec_name = 'title'
    _order = 'title asc'

    code = fields.Char('Book Code', size=64, required=True, index=True, readonly=True, default="New Book")
    title = fields.Char('Title', size=64, required=True, index=True, readonly=True,
                      states={'draft': [('readonly', False)]})
    author = fields.Many2one('bookstore.author', string='Author', required=True, index=True, readonly=True,
                          states={'draft': [('readonly', False)]}, ondelete="cascade")
    publisher = fields.Many2one('bookstore.publisher', string='Publisher', required=True, index=True, readonly=True,
                          states={'draft': [('readonly', False)]}, ondelete="cascade")
    price = fields.Integer('Price (Rp)', required=True, index=True, readonly=True,
                      states={'draft': [('readonly', False)]})
    discount = fields.Integer('Discount (%)', required=True, index=True, readonly=True, default=0,
                           states={'draft': [('readonly', False)]})
    quantity = fields.Integer('Quantity', required=True, index=True, readonly=True, default=0,
                              states={'draft': [('readonly', False)]})
    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),], 'State', required=True, readonly=True,
                             default='draft')

    _sql_constraints = [('code_unique', 'unique(code)', _('Book code must be unique!'))]

    @api.model_create_multi
    def create(self, vals_list):
        seq = self.env['ir.sequence'].search([("code", "=", "bookstore.book")])
        if not seq:
            raise exceptions.UserError(_("bookstore.book sequence not found, please create bookstore.book sequence"))
        for val in vals_list:
            val['code'] = seq.next_by_id()

        return super(book, self).create(vals_list)

    def action_wiz_book(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Wizard Diskon Buku'),
            'res_model': 'wiz.book.discount',
            'view_mode': 'form',
            'target': 'new',
            'context': {'active_id': self.id},
        }

    def action_confirmed(self):
        self.state = 'confirmed'

    def action_settodraft(self):
        self.state = 'draft'