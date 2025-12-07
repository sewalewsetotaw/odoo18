from odoo import fields, models, api


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    is_lease_agreement = fields.Boolean(string="Lease Agreement")
    lease_id = fields.Many2one('lease.management', string="Related Lease")


class ProductProduct(models.Model):
    _inherit = 'product.product'

    property_management_id = fields.Many2one(
        'property.management',
        string="Property"
    )
