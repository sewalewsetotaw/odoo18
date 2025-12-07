from odoo import models, fields, api
from datetime import date

class Student(models.Model):
    _name = 'student.management'
    _rec_name = 'admission_no'

    name = fields.Char(string="Full Name", required=True)
    admission_no = fields.Char(string="Admission No",  required=True,  copy=False, readonly=True, index=True,  default=lambda self: 'New')
    date_of_birth = fields.Date(string="Date of Birth", required=True)
    age=fields.Integer(string="Age",compute='_compute_age',store=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string="Gender", required=True,)
    photo = fields.Binary(string="Photo")
    parent_ids = fields.Many2many('parent.management', string="Parent/Guardian")
    join_date = fields.Date(string="Date of joining", required=True)
    section_id = fields.Many2one('section.management', string="Section")
    attendance_ids = fields.One2many('attendance.management', 'student_id', string='Attendances')
    timetable_ids = fields.Many2many('timetable.management',compute='_compute_timetables', string='Timetables',store=True)
    course_id = fields.Many2many('course.management', string="Course")
    enrollment_ids = fields.One2many('enrollment.management','student_id', string="Enrollments"
    )
    user_id = fields.Many2one('res.users', string="Portal User", help="Student login account")
    fee_ids = fields.One2many('fees.fees', 'student_id', string="Fees")
    fees_count = fields.Integer(
        string="Fees Count",
        compute="_compute_fees_count"
    )

    @api.depends('fee_ids')
    def _compute_fees_count(self):
        for student in self:
            student.fees_count = len(student.fee_ids)

    def action_view_fees(self):
        return {
            'name': 'Fees',
            'type': 'ir.actions.act_window',
            'res_model': 'fees.fees',
            'view_mode': 'list,form',
            'domain': [('student_id', '=', self.id)],
            'context': {'default_student_id': self.id}
        }
    @api.model
    def create(self, vals):
        if not vals.get('admission_no') or vals.get('admission_no') == 'New':
            vals['admission_no'] = self.env['ir.sequence'].next_by_code('student.management') or 'New'
        return super(Student, self).create(vals)

    @api.depends('date_of_birth')
    def _compute_age(self):
        today = date.today()
        for record in self:
            if record.date_of_birth:
                age = (today.year - record.date_of_birth.year -
                       ((today.month, today.day) < (record.date_of_birth.month, record.date_of_birth.day)))
                record.age = age
            else:
                record.age = 0
    @api.depends('section_id')
    def _compute_timetables(self):
        for rec in self:
            rec.timetable_ids = rec.section_id.timetable_ids

    def action_enroll_student(self):
        self.ensure_one()
        return {
            'name': 'Enroll Student',
            'type': 'ir.actions.act_window',
            'res_model': 'enrollment.management',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_student_id': self.id,
                'default_section_id': self.section_id.id,
            }
        }
