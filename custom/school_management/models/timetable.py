from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class Timetable(models.Model):
    _name = 'timetable.management'
    # _description = 'Timetable'

    section_id = fields.Many2one('section.management', string="Section", required=True)
    course_id = fields.Many2one('course.management', string="Course", required=True)
    teacher_id = fields.Many2one('hr.employee', string="Teacher", domain=[('is_teacher', '=', True)], required=True)

    day_of_week = fields.Selection([
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ], string="Day of Week", required=True)

    start_time = fields.Float(string="Start Time (Hours)", required=True)
    end_time = fields.Float(string="End Time (Hours)", required=True)

    @api.constrains('section_id',  'teacher_id', 'day_of_week', 'start_time', 'end_time')
    def _check_time_range(self):
        for record in self:
            if record.start_time >= record.end_time:
                raise ValidationError("Start time must be less than end time.")

            overlapping_records = [
                ('id', '!=', record.id),
                ('day_of_week', '=', record.day_of_week),
                ('start_time', '<=', record.start_time),
                ('end_time', '>=', record.start_time),
            ]
            # Check teacher conflict
            teacher_conflict = self.env['timetable.management'].search(
                overlapping_records + [('teacher_id', '=', record.teacher_id.id)]
            )

            # Check section conflict
            section_conflict = self.env['timetable.management'].search(
                overlapping_records + [('section_id', '=', record.section_id.id)]
            )

            if teacher_conflict:
                raise ValidationError(
                    f"Teacher {record.teacher_id.name} already has a class "
                    f"at this time on {record.day_of_week.capitalize()}."
                )

            if section_conflict:
                raise ValidationError(
                    f"Section {record.section_id.name} already has a class "
                    f"at this time on {record.day_of_week.capitalize()}."
                )

            _logger.info("Validated timetable: %s", record)