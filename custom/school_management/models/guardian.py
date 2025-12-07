from odoo import models, fields, api

class Parent(models.Model):
    _name = 'parent.management'
    _description = 'Parent/Guardian'

    name = fields.Char(string="Name", required=True)
    phone_number = fields.Char(string="Phone Number")
    email = fields.Char(string="Email")
    user_id = fields.Many2one('res.users', string="Portal User", help="Guardian login account")
    relation = fields.Selection([
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('guardian', 'Guardian'),
    ], string="Relation", required=True)
    partner_id = fields.Many2one('res.partner', string="Linked Partner", ondelete="cascade")
    students = fields.Many2many('student.management',string="Children")

    @api.model
    def create(self, vals):
        guardian = super().create(vals)

        # Auto-create partner if not linked
        if not guardian.partner_id:
            partner = self.env['res.partner'].create({
                'name': guardian.name,
                'phone': guardian.phone_number,
                'email': guardian.email,
                'type': 'contact',
            })
            guardian.partner_id = partner.id

        return guardian

    def write(self, vals):
        res = super().write(vals)

        # Keep partner updated if details change
        for guardian in self:
            if guardian.partner_id:
                guardian.partner_id.write({
                    'name': guardian.name,
                    'phone': guardian.phone_number,
                    'email': guardian.email,
                })
        return res
