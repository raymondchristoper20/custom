from odoo import models, fields, api, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    total_disc = fields.Monetary(string="Total Disc 1")

class SaleOrderLines(models.Model):
    _inherit = 'sale.order.line'

    #Attribute
    disc2 = fields.Float(string="Disc 2 (%)", digits='Discount', default=0.0)

    # @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id', 'disc2')
    # def _compute_amount(self):