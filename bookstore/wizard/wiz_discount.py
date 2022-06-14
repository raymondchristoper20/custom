from odoo import models, fields, api, _
# _ untuk translate

class wizbookdiscount(models.TransientModel):
    _name = 'wiz.book.discount'
    _description = 'class untuk menyimpan data diskon buku'

    def get_default_books(self):
        return self.env['bookstore.book'].browse(self.env.context.get('active_ids'))

    book_id = fields.Many2many('bookstore.book', string='Book', default=get_default_books)
    discount = fields.Integer('Discount')
    # add = fields.Integer('Add Quantity')

    def set_book_discount(self):
        for record in self:
            if record.book_id:
                for book in record.book_id:
                    book.discount = self.discount
                    # book.quantity = book.quantity + self.add
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

