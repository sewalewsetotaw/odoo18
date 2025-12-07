from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Enrollment(models.Model):
    _name = 'enrollment.management'
    _description = 'Enrollment'

    student_id = fields.Many2one('student.management', string="Student", required=True)
    course_id = fields.Many2one('course.management', string="Course", required=True)
    section_id = fields.Many2one('section.management', string="Section", required=True)
    academic_year = fields.Many2one('academic.year', string='Academic Year', required=True)
    date_enrolled = fields.Date(string="Date Enrolled", required=True)
    state = fields.Selection([
        ('enrolled', 'Enrolled'),
        ('graduated', 'Graduated'),
        ('dropped', 'Dropped')], string="State", default='enrolled'
    )

    @api.constrains('student_id', 'course_id', 'academic_year')
    def _check_unique_enrollment(self):
        for rec in self:
            duplicate = self.search([
                ('id', '!=', rec.id),
                ('student_id', '=', rec.student_id.id),
                ('course_id', '=', rec.course_id.id),
                ('academic_year', '=', rec.academic_year.id)
            ], limit=1)
            if duplicate:
                raise ValidationError(
                    f"{rec.student_id.name} is already enrolled in {rec.course_id.name} for {rec.academic_year.name}."
                )