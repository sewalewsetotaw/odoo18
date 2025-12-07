from odoo import models,fields, api

class Section(models.Model):
    _name = 'section.management'
    # _description = 'Section'

    name = fields.Char(string='Section Name', required=True)
    academic_year_id = fields.Many2one(
        'academic.year',
        string='Academic Year',
        domain=[('state', '=', 'active')]  # Only show active academic years
    )
    course_ids = fields.Many2many('course.management', string='Course')
    student_ids = fields.One2many('student.management', 'section_id', string='Students')
    teacher_ids = fields.Many2many('hr.employee', string='Teachers',domain=[('is_teacher', '=', True)])
    timetable_ids = fields.One2many('timetable.management', 'section_id', string='Timetables')