from odoo import models, fields, api


class AttendanceSummaryWizard(models.TransientModel):
    _name = 'attendance.summary.wizard'
    _description = 'Attendance Summary Wizard'

    date_from = fields.Date()
    date_to = fields.Date()
    status = fields.Selection([
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused')], string="Status")

    def action_print_report(self):
        # Apply filters only if provided
        domain = []
        if self.date_from:
            domain.append(('date', '>=', self.date_from))
        if self.date_to:
            domain.append(('date', '<=', self.date_to))
        if self.status:
            domain.append(('status', '=', self.status))

        # If no filters are set, domain remains empty → returns all attendances

        attendances = self.env['attendance.management'].search(domain)
        data = {
            'docs': attendances, # always pass list, even if empty
            'date_from': self.date_from,
            'date_to': self.date_to,
            'status': self.status,
        }

        # If there are attendances, pass recordset
        # If none, pass None with data
        if attendances:
            return self.env.ref('school_management.action_attendance_summary_report').report_action(attendances)
        else:
            return self.env.ref('school_management.action_attendance_summary_report').report_action(None, data=data)
