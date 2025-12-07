from odoo import models, api
from collections import Counter
from datetime import date, timedelta

class SchoolOverview(models.Model):
    _name = 'school.dashboard'
    _description = 'School Overview Dashboard'

    @api.model
    def get_dashboard_data(self):
        # Students
        students = self.env['student.management'].search([])
        student_count = len(students)

        # Enrollments
        enrollments = self.env['enrollment.management'].search([])
        enrollment_count = len(enrollments)

        # Fees
        fees = self.env['fees.fees'].search([])
        total_fees = sum(f.amount_paid for f in fees)

        # Attendance
        attendance = self.env['attendance.management'].search([])
        attendance_count = len(attendance)

        # Courses
        courses = self.env['course.management'].search([])
        courses_count = len(courses)

        # Teachers
        teachers = self.env['hr.employee'].search([('is_teacher', '=', True)])
        teachers_count = len(teachers)

        # Sections
        sections = self.env['section.management'].search([])
        sections_count = len(sections)

        # Exams
        exams = self.env['exam.management'].search([])
        exams_count = len(exams)

        return {
            "students": student_count,
            "enrollments": enrollment_count,
            "fees": total_fees,
            "attendance": attendance_count,
            "courses": courses_count,
            "teachers": teachers_count,
            "sections": sections_count,
            "exams": exams_count,
        }
