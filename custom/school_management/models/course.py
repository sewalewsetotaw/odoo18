from odoo import models,fields,api

class Course(models.Model):
    _name = 'course.management'
    _rec_name = 'code'

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    description = fields.Text(string="Description")
    student_ids=fields.Many2many('student.management',string="Students")
    # teacher_ids=fields.Many2many('teacher.management',string="Teachers")
    teacher_ids=fields.Many2many('hr.employee',string="Assigned Teachers",domain=[('is_teacher','=',True)])
    section_ids=fields.Many2many('section.management',string="Sections")