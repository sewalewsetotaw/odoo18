from odoo import  fields, models,api


class CrmLeadInherit(models.Model):
    _inherit = 'crm.lead'

    is_tenant_lead = fields.Boolean(string="Tenant Lead")
    property_id = fields.Many2one('property.management', string="Interested Property")
    budget = fields.Float(string="Rental Budget")

