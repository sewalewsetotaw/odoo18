from odoo import models, fields, api


class Tenant(models.Model):
    _name = 'tenant.management'
    _description = 'Tenant'

    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    id_number = fields.Char(
        string='ID Number',
        required=True,
        copy=False,
        readonly=True,
        default='New'
    )
    lease_ids = fields.One2many('lease.management', 'tenant_id', string='Leases')  # one tenant can have multiple leases

    @api.model
    def create(self, vals):
        if vals.get('id_number', 'New') == 'New':
            vals['id_number'] = self.env['ir.sequence'].next_by_code('tenant.management') or 'New'
        return super(Tenant, self).create(vals)
