from odoo import models, fields, api

class TeacherEmployee(models.Model):
    _inherit = 'hr.employee'

    is_teacher = fields.Boolean(string="Is a Teacher", default=False)
    qualification = fields.Text(string="Qualification")
    course_ids = fields.Many2many('course.management',  string="Courses")
    section_ids = fields.Many2many('section.management', string="Sections")
    timetable_ids = fields.One2many('timetable.management', 'teacher_id',  string='Attendances')

    joining_date = fields.Date(string="Joining Date")