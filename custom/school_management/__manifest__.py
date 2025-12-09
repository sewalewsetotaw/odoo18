{
    'name': 'School Management System',
    'version': '1.0',
    'summary': "Comprehensive School Management System for Odoo 18",
    'description': """
School Management System for Odoo 18
====================================

This module provides a complete solution for managing school operations, including:
- Students & Guardians
- Teachers & Staff
- Courses, Sections & Enrollments
- Attendance Tracking
- Exams & Report Cards
- Fees, Invoices & Scholarships
- Dashboards & Reports
- Student/Guardian Portal Access
    """,
    'category': 'Education',
    'author': 'Sewalew Setotaw',
    'maintainer': 'Sewalew Setotaw',
    'website': 'https://github.com/sewalew-setotaw',
    'depends': ['base', 'mail', 'hr', 'web'],
    'data': [
        'security/school_management_security.xml',
        'security/school_record_rules.xml',
        'security/ir.model.access.csv',

        'views/parent_views.xml',
        'views/student_views.xml',
        'views/section_views.xml',
        'views/timetable_views.xml',
        'views/course_views.xml',
        'views/exam_result_views.xml',
        'views/fee_views.xml',
        'views/attendance_views.xml',
        'views/academic_year_views.xml',
        'views/menus.xml',
        'views/teacher_employee_views.xml',
        'views/enrollment_views.xml',
        'views/fee_structure_views.xml',
        'views/school_dashboard_action.xml',
        # 'views/assets.xml',

        'report/attendance_summary_template.xml',

        'wizard/attendance_summary_wizard_views.xml',
        'wizard/fee_payment_excel_wizard.xml',

        'data/student_admission_seq.xml',
        'data/email_cron.xml',
        'data/email_template.xml',
        'data/school_management_demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'school_management/static/src/js/school_dashboard.js',
            'school_management/static/src/xml/school_dashboard.xml',
        ],
    },
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
