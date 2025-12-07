from odoo import models, fields, api


class LeaseSummaryWizard(models.TransientModel):
    _name = 'lease.summary.wizard'
    _description = 'Lease Summary Wizard'

    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date To")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('expired', 'Expired')
    ], string="Status")

    def action_print_report(self):
        domain = []
        # Apply filters only if provided
        if self.date_from:
            domain.append(('start_date', '>=', self.date_from))
        if self.date_to:
            domain.append(('end_date', '<=', self.date_to))
        if self.state:
            domain.append(('state', '=', self.state))

        # If no filters are set, domain remains empty → returns all leases
        leases = self.env['lease.management'].search(domain)
        data = {
            'docs': leases,  # always pass list, even if empty
            'date_from': self.date_from,
            'date_to': self.date_to,
            'state': self.state or '',
        }
        # If there are leases, pass recordset
        # If none, pass None with data
        if leases:
            return self.env.ref('property_management.action_lease_summary_report').report_action(leases)
        else:
            return self.env.ref('property_management.action_lease_summary_report').report_action(None, data=data)
