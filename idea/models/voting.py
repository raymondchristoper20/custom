from odoo import models, fields, api, _
# _ untuk translate

class voting(models.Model):
    _name = 'idea.voting'
    _description = 'class untuk berlatih tentang voting'
    _rec_name = 'name'
    _order = 'date desc' # defaultnya adalah id, pengaruhnya saat list view

    # _order = 'date desc'
    # id = fields.Integer() ini otomatis ada di odoo, akan jadi PK
    # membuat attribute field. Field ini punya common parameter
    name = fields.Char('Number', size=64, required=True, index=True, readonly=True, default='New', states={})
    date = fields.Date('Date Release', default=fields.Date.context_today, readonly=True,states={'draft': [('readonly', False)]})
    # att pertama selalu String shg tdk perlu ditulis nama parameter-nya
    state = fields.Selection([('draft', 'Draft'),
                              ('voted', 'Voted'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True,
                             default='draft')
    # Description is read-only when not draft!
    vote = fields.Selection([('yes', 'Yes'),
                             ('no', 'No'),
                             ('abstain', 'Abstain')], 'Vote', required=True, readonly=True, states={'draft': [('readonly', False)]})

    voter_id = fields.Many2one('res.users', 'Voted By', readonly=True, ondelete="cascade", default=lambda self: self.env.user)
    idea_id = fields.Many2one('idea.idea', string='Idea', readonly=True, ondelete="cascade", states={'draft': [('readonly', False)]},  domain="[('state', '=', 'done'),('active','=','True')]")

    idea_date = fields.Date('Idea Date', related='idea_id.date', store=True)

    def action_voted(self):
        self.state = 'voted'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'

    @api.model_create_multi
    def create(self, vals_list):
            seq = self.env['ir.sequence'].search([("code", "=", "idea.voting")])
            if not seq:
                raise UserError(_("idea.voting sequence not found, please create idea.voting sequence"))
            for val in vals_list:
                val['name'] = seq.next_by_id(sequence_date=val['date'])

            return super(voting, self).create(vals_list)
