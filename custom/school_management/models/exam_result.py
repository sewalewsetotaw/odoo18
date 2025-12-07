from odoo import models, fields, api

class Exam(models.Model):
    _name = 'exam.management'
    _description = 'Exam Management'

    name = fields.Char(string="Name", required=True)
    course_id = fields.Many2one('course.management', string="Course", required=True,ondelete='cascade')
    section_id = fields.Many2one('section.management', string="Section", required=True, ondelete='cascade')
    academic_year = fields.Many2one(
        'academic.year',
        string='Academic Year',
        domain=[('state', '=', 'active')]  # Only show active academic years
    )
    exam_date = fields.Date(string="Exam Date", required=True)
    max_marks = fields.Integer(string="Max Marks", required=True)
    passing_marks = fields.Integer(string="Passing Marks", required=True)

class Result(models.Model):
    _name = 'result.management'
    _description = 'Result Management'

    name = fields.Char(compute="_compute_name", string="Name",store=True)
    exam_id = fields.Many2one('exam.management', string="Exam", required=True,ondelete='cascade')
    student_id = fields.Many2one('student.management', string="Student", required=True,ondelete='cascade')
    marks_obtained = fields.Float(string="Marks Obtained", required=True)
    grade = fields.Char(string="Grade", required=True)
    status = fields.Selection(
        [('pass', 'Pass'), ('fail', 'Fail')],
        string="Status",
        compute="_compute_status",
        store=True
    )

    @api.depends("marks_obtained", "exam_id.passing_marks")
    def _compute_status(self):
        for rec in self:
            rec.status = "pass" if rec.marks_obtained >= rec.exam_id.passing_marks else "fail"

    @api.depends("student_id.name", "exam_id.name")
    def _compute_name(self):
        for rec in self:
            rec.name = f"{rec.student_id.name} - {rec.exam_id.name}" if rec.student_id and rec.exam_id else "Result"
