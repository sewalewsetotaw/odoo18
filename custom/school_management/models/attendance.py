from odoo import models, fields, api
import logging
from datetime import date

_logger = logging.getLogger(__name__)

class Attendance(models.Model):
    _name = 'attendance.management'
    _description = 'Attendance Management'

    date = fields.Date(string="Date", required=True)
    section_id = fields.Many2one('section.management', string="Section", required=True)
    student_id = fields.Many2one('student.management', string="Student", required=True)
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    status = fields.Selection([
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused')
    ], string="Status", required=True)
    teacher_id = fields.Many2one('hr.employee', string="Teacher", required=True,domain=[('is_teacher', '=', True)])
    alert_sent = fields.Boolean(string="Absent Alert Sent", default=False)

    @api.model
    def send_absent_alerts_cron(self):
        """Send email to parents if student absent 3 consecutive times and not alerted yet"""
        today = date.today()

        # Only consider absences today that haven't triggered an alert
        recent_absences = self.search([
            ('status', '=', 'absent'),
            ('date', '=', today),
            ('alert_sent', '=', False)
        ])
        students = recent_absences.mapped('student_id')

        for student in students:
            last_attendances = self.search(
                [('student_id', '=', student.id)],
                order='date desc',
                limit=3
            )

            if len(last_attendances) == 3 and all(a.status == 'absent' for a in last_attendances):
                template = self.env.ref('school_management.email_template_attendance_absent', raise_if_not_found=False)
                if not template:
                    _logger.error("Email template not found")
                    continue

                # Use student.parent_id Many2many relation
                for parent in student.parent_id:
                    if parent.email:
                        try:
                            template.with_context(
                                student_name=student.name,
                                student_code=student.admission_no,
                                section_name=last_attendances[0].section_id.name,
                                date=last_attendances[0].date
                            ).send_mail(
                                last_attendances[0].id,
                                force_send=True,
                                email_values={'email_to': parent.email}
                            )
                            _logger.info(f"Email sent to parent: {parent.email} for student: {student.name}")
                        except Exception as e:
                            _logger.error(f"Failed to send email to {parent.email}: {str(e)}")

                # Mark all 3 attendances as alerted
                last_attendances.write({'alert_sent': True})
