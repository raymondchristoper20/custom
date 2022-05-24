from odoo import models, fields, api, _
# _ untuk translate

class transaction(models.Model):
    _name = 'library.transaction'
    _description = 'data of library transaction'
    _rec_name = 'code'
    _order = 'code asc'

    code = fields.Many2one('library.book', string='Book Code', required=True, index=True, readonly=True,
                        states={'draft': [('readonly', False)]}, ondelete="cascade", domain="[('state', '=', 'confirmed'),('status','=','available')]")
    nik = fields.Many2one('library.member', string='Citizenship ID', required=True, index=True, readonly=True,
                       states={'draft': [('readonly', False)]}, ondelete="cascade")
    borrowDate = fields.Date('Borrow Date', required=True, index=True, readonly=True,
                      states={'draft': [('readonly', False)]})
    returnDate = fields.Date('Return Date', required=True, index=True, readonly=True,
                             states={'draft': [('readonly', False)]})
    cost = fields.Integer('Cost (Rp)', compute="_compute_cost", store=True, default=0)
    returnedOn = fields.Date('Returned On', index=True, readonly=True,
                             states={'returned': [('readonly', False)]})
    fine = fields.Integer('Fine (Rp)', compute="_compute_fine", store=True, default=0)
    total = fields.Integer('Total (Rp)', compute="_compute_total", store=True, default=0)

    state = fields.Selection([('draft', 'Draft'),
                              ('borrowed', 'Borrowed'),
                              ('returned', 'Returned'),
                              ('done', 'Done'),], 'State', required=True, readonly=True,
                             default='draft')

    @api.depends('returnDate', 'borrowDate')
    def _compute_cost(self):
        #for x in self.filtered(lambda s:s.state=='borrowed'):
        #    x.cost = (x.returnDate - x.borrowDate).days
        if self.returnDate and self.borrowDate:
            self.cost = 1000 * (self.returnDate - self.borrowDate).days

    @api.depends('returnDate', 'borrowDate', 'returnedOn')
    def _compute_fine(self):
        if self.returnedOn:
            if (self.returnDate - self.borrowDate).days < (self.returnedOn - self.borrowDate).days:
                self.fine = 2000 * (self.returnedOn - self.returnDate).days
            else:
                self.fine = 0

    @api.depends('returnedOn', 'cost', 'fine')
    def _compute_total(self):
        if self.returnedOn:
            if (self.returnDate - self.borrowDate).days < (self.returnedOn - self.borrowDate).days:
                self.total = self.cost + self.fine
            else:
                self.total = self.cost


    def action_borrowed(self):
        self.state = 'borrowed'
        self.code.status = 'borrowed'

    def action_settodraft(self):
        self.state = 'draft'

    def action_returned(self):
        self.state = 'returned'
        self.code.status = 'available'

    def action_done(self):
        self.state = 'done'

    def tes_transaction(self):
        print("ini di transaction")
        t = self.env.context
        print(t.keterangan)