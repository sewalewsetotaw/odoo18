from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Property(models.Model):
    _name = 'property.management'
    _description = 'Property'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Property Name', required=True)
    property_type = fields.Selection([
        ('apartment', 'Apartment'),
        ('villa', 'Villa'),
        ('office', 'Office'),
        ('commercial', 'Commercial')
    ], string='Type', default='apartment', required=True)
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    price_per_month = fields.Float(string='Price per Month', required=True)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    status = fields.Selection([
        ('available', 'Available'),
        ('rented', 'Rented'),
        ('maintenance', 'Maintenance')
    ], string='Status', default='available', required=True)
    image = fields.Binary(string='Image')
    description = fields.Text(string='Description')
    feature_ids = fields.Many2many('property.feature', string='Features')

    address = fields.Char(string='Address')
    year_built = fields.Integer(string='Year Built')
    area_sqft = fields.Float(string='Area (sqft)')

    num_bedrooms = fields.Integer(string="Bedrooms", help="Only for Apartments/Villas", required=True)
    num_floors = fields.Integer(string="Floors", help="Mainly for Villas/Commercial")
    license_number = fields.Char(string="Business License", help="Required for Commercial")

    price_per_year = fields.Float(string='Price per Year', compute='_compute_price_per_year', store=True)
    discount_percent = fields.Float(string='Discount (%)')
    discounted_price = fields.Float(string='Discounted Price')

    def action_available(self):
        self.ensure_one()  # Ensures this method works on single records
        self.status = 'available'

        # Create corresponding product
        product = self.env['product.product'].create({
            'name': self.name,
            'list_price': self.price_per_month,
            'type': 'service',
            'default_code': f'PROP-{self.id}',  # Adding unique identifier
            'property_management_id': self.id,
        })

        return True

    def action_maintenance(self):
        self.status = 'maintenance'

    @api.constrains('property_type', 'num_bedrooms')
    def _validate_bedrooms(self):
        for record in self:
            if record.property_type in ['apartment', 'villa'] and not record.num_bedrooms:
                raise ValidationError("Bedrooms are required for Apartments and Villas!")

    @api.depends('price_per_month')
    def _compute_price_per_year(self):
        for rec in self:
            rec.price_per_year = rec.price_per_month * 12

    @api.onchange('discount_percent', 'price_per_month')
    def _onchange_discount(self):
        for rec in self:
            if rec.discount_percent < 0 or rec.discount_percent > 100:
                return {
                    'warning': {
                        'title': 'Invalid Discount',
                        'message': 'Discount percent must be between 0 and 100.'
                    }
                }
            rec.discounted_price = rec.price_per_month * (1 - rec.discount_percent / 100) if rec.price_per_month else 0


class PropertyFeature(models.Model):
    _name = 'property.feature'
    _description = 'Property Feature'

    name = fields.Char(string='Feature', required=True)
    color = fields.Integer(string='Color Index')
