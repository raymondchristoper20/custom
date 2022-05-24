from odoo import models, fields, api, _
# _ untuk translate

class mahasiswa(models.Model):
    _name = 'library.book'
    _description = 'data master of books'
    _rec_name = 'code'
    _order = 'title asc'

    code = fields.Char('Book Code', size=64, required=True, index=True, readonly=True,
                       states={'draft': [('readonly', False)]})
    title = fields.Char('Title', size=64, required=True, index=True, readonly=True,
                      states={'draft': [('readonly', False)]})
    publisher = fields.Char('Publisher', size=64, required=True, index=True, readonly=True,
                       states={'draft': [('readonly', False)]})
    author = fields.Char('Author', size=64, required=True, index=True, readonly=True,
                            states={'draft': [('readonly', False)]})
    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),], 'State', required=True, readonly=True,
                             default='draft')
    status = fields.Selection([('available', 'Available'),
                             ('borrowed', 'Borrowed'),], 'Status', required=True, readonly=True,
                              default='available', states={'draft': [('readonly', False)]})

    #transaction_ids = fields.One2many('library.transaction', 'book_id', string='Transaction', default=0)

    _sql_constraints = [('code_unique', 'unique(code)', _('Book code must be unique!'))]

    # @api.depends("transaction_ids", "transaction_ids.state")
    #
    # def _compute_vote(self):
    #     for book in self.filtered(lambda s:s.state=='confirmed'):
    #         val = {
    #             "status" : 'available',
    #         }
    #         for rec in self.transaction_ids.filtered(lambda s:s.state=='confirmed'):
    #             if rec.vote == 'yes':
    #                 val["status"] += "borrowed"
    #             elif rec.vote == 'no':
    #                 val["total_no"] += 1
    #             else:
    #                 val["total_abstain"] += 1
    #         book.update(val)

    def action_confirmed(self):
        self.state = 'confirmed'

    def action_settodraft(self):
        self.state = 'draft'