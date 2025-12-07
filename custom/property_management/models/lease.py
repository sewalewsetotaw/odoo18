from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta
import logging

_logger = logging.getLogger(__name__)


class Lease(models.Model):
    _name = 'lease.management'
    _description = 'Lease'

    name = fields.Char(string='Lease Name', compute='_compute_lease_name', store=True)
    tenant_id = fields.Many2one('tenant.management', string='Tenant', required=True)
    property_id = fields.Many2one('property.management', string='Property', required=True)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    monthly_rent = fields.Float(string='Monthly Rent', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('expired', 'Expired')
    ], string='Status', default='draft')
    payment_ids = fields.One2many('rent.payment', 'lease_id', string='Payments')
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)

    total_days = fields.Float(string="Total Days", compute="_compute_total_rent", store=True)
    total_months = fields.Float(string="Total Months", compute="_compute_total_rent", store=True)
    total_rent = fields.Float(string="Total Rent", compute="_compute_total_rent", store=True)

    @api.depends('start_date', 'end_date', 'monthly_rent')
    def _compute_total_rent(self):

        for rec in self:
            if rec.start_date and rec.end_date:
                rec.total_days = (rec.end_date - rec.start_date).days + 1  # Include the start date in the total days
                rec.total_months = rec.total_days / 30
                rec.total_rent = rec.total_months * rec.monthly_rent
            else:
                rec.total_days = 0
                rec.total_months = 0
                rec.total_rent = 0

    @api.depends('tenant_id', 'property_id')
    def _compute_lease_name(self):
        for lease in self:
            lease.name = f"Lease {lease.tenant_id.name} - {lease.property_id.name}"

    def action_active(self):
        self._check_double_leasing()
        self.state = 'active'
        self.property_id.status = 'rented'

    def action_expired(self):
        self.state = 'expired'
        self.property_id.status = 'available'

    @api.onchange('property_id')
    def _onchange_property(self):
        if self.property_id:
            self.monthly_rent = self.property_id.price_per_month

            # today class • Filter records in relational fields.

    @api.constrains('property_id', 'start_date', 'end_date')
    def _check_double_leasing(self):
        for record in self:
            overlapping_leases = self.env['lease.management'].search([
                ('property_id', '=', record.property_id.id),
                ('id', '!=', record.id),
                ('state', 'in', ['draft', 'active']),
                '|',
                '&', ('start_date', '>=', record.start_date), ('start_date', '<=', record.end_date),
                # The start date of the other lease is within the current lease's date range.
                '&', ('end_date', '>=', record.start_date), ('end_date', '<=', record.end_date)
                # The end date of the other lease is within the current lease's date range.

            ])
            if overlapping_leases:
                raise ValidationError('This property is already leased for the selected period.')

    @api.model
    def check_lease_expiry(self):
        leases = self.search([
            ('end_date', '<=', fields.Date.today() + timedelta(days=30)),
            ('state', '=', 'active')
        ])

        # Get manager group and emails
        manager_group = self.env.ref('property_management.group_property_manager')
        if not manager_group:
            _logger.warning("Manager group not found, cannot send expiration notifications")
            return

        manager_emails = manager_group.users.mapped('partner_id.email')
        if not manager_emails:
            _logger.warning("No email addresses found in manager group")
            return

        for lease in leases:
            if lease.end_date <= fields.Date.today():
                lease.action_expired()
            self._send_expiry_notification(lease, manager_emails)

    @api.model
    def _send_expiry_notification(self, lease, recipient_emails):
        """Send expiration notification to legal team members"""
        template = self.env.ref('property_management.email_lease_expire', raise_if_not_found=False)

        try:
            for email in recipient_emails:
                template.with_context(
                    lease_name=lease.name,
                    end_date=lease.end_date,
                    tenant_name=lease.tenant_id.name
                ).send_mail(
                    lease.id,
                    force_send=True,
                    email_values={'email_to': email}
                )
            _logger.info(f"Sent expiration notice for lease {lease.name} to {recipient_emails}")
            return True
        except Exception as e:
            _logger.error(f"Failed to send expiration notice for lease {lease.name}: {str(e)}")
            return False
