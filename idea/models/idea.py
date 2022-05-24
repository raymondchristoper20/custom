from odoo import models, fields, api, _
# _ untuk translate

class idea(models.Model):
    _name = 'idea.idea'
    _description = 'class untuk berlatih tentang idea'
    _rec_name = 'name'
    _order = 'date desc' # defaultnya adalah id, pengaruhnya saat list view

    # _order = 'date desc'
    # id = fields.Integer() ini otomatis ada di odoo, akan jadi PK
    # membuat attribute field. Field ini punya common parameter
    name = fields.Char('Number', size=64, required=True, index=True, readonly=True, default='New', states={})
    date = fields.Date('Date Release', default=fields.Date.context_today, readonly=True,states={'draft': [('readonly', False)]})
    # att pertama selalu String shg tdk perlu ditulis nama parameter-nya
    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True,
                             default='draft')
    # Description is read-only when not draft!
    description = fields.Text('Description', readonly=True, states={'draft': [('readonly', False)]})
    active = fields.Boolean('Active', default=True, readonly=True, states={'draft': [('readonly', False)]})
    confirm_date = fields.Date('Confirm date')
    # by convention, many2one fields end with '_id'
    confirm_partner_id = fields.Many2one('res.partner', 'Confirm By', readonly=True, states={'draft': [('readonly', False)]})
    # sponsor_ids = fields.Many2many('res.partner', 'idea_idea_res_partner_rel', 'idea_idea_id', 'res_partner_id','Sponsors')
    sponsor_ids = fields.Many2many('res.partner', string='Sponsors')
    score = fields.Integer('Score', default=0, readonly=True)
    owner = fields.Many2one('res.partner', 'Owner', index=True, readonly=True,states={'draft': [('readonly', False)]})
    voting_ids = fields.One2many('idea.voting', 'idea_id', string='Votes', default=0)
    total_yes = fields.Integer("Yes", compute="_compute_vote", store=True, default=0)
    total_no = fields.Integer("No", compute="_compute_vote", store=True, default=0)
    total_abstain = fields.Integer("Abstain", compute="_compute_vote", store=True)
    _sql_constraints = [('name_unik', 'unique(name)', _('Ideas must be unique!'))]

    @api.depends("voting_ids", "voting_ids.vote", "voting_ids.state")

    def _compute_vote(self):
        for idea in self.filtered(lambda s:s.state=='done'):
            val = {
                "total_yes" : 0,
                "total_no" : 0,
                "total_abstain" : 0
            }
            for rec in idea.voting_ids.filtered(lambda s:s.state=='voted'):
                if rec.vote == 'yes':
                    val["total_yes"] += 1
                elif rec.vote == 'no':
                    val["total_no"] += 1
                else:
                    val["total_abstain"] += 1
            idea.update(val)

    def action_done(self):
        self.state ='done'
        t = self.env.context
        print(t.get('keterangan'))

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'

    def action_confirmed(self):
        self.state = 'confirmed'
        if self.name == 'new' or not self.name:
            seq = self.env['ir.sequence'].search([("code", "=", "idea.idea")])
            if not seq:
                raise UserError(_("idea.idea sequence not found, please create idea.idea sequence"))
            self.name = seq.next_by_id(sequence_date=self.date)

    def action_tes(self):
        print(self.env.user.name)
        print(self.env.company.name)
        #contoh common orm method search
        a = self.env["res.partner"].search([('name', 'like', 'Gemini')])
        b = self.env["res.partner"].search([], limit=2)
        for rec in a:
            print(rec.name)
        for rec in b:
            print(rec.name)

        #contoh context
        print(self.env.context.get('lang'))

        t = self.env.context.copy()
        t["keterangan"] = 'Ideaku'
        self.with_context(t).action_done()

        b = self.env["library.transaction"]
        b.with_context(t).tes_transaction()

        # contoh query select
        query = "select name from res_partner order by name desc limit 3"
        self.env.cr.execute(query)
        res = self.env.cr.fetchall()
        for data in res:
            print(data[0])

        # contoh query update
        query = "update idea_idea set state='done' where state in ('confirmed','draft')"
        self.env.cr.execute(query)
        self.env.cr.rollback()

        # contoh query delete
        query = "update idea_idea set state='done' where state in ('confirmed','draft')"
        self.env.cr.execute(query)
        self.env.cr.rollback()
