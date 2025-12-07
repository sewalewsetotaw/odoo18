{
    'name': "Property Management",
    'version': '18.0',
    'summary': 'Manage properties, tenants, leases, and payments',
    'description': """
        A comprehensive property management system for handling properties, tenants, leases, payments, and analytics.
    """,
    'author': 'Sewalew Setotaw',
    'category': 'Real Estate',
    'depends': ['base', 'mail', 'web', 'crm', 'sale_management', 'product'],
    'sequence': 1,
    'data': [
        'security/ir.model.access.csv',
        'security/property_management_security.xml',

        'views/property_views.xml',
        'views/tenant_views.xml',
        'views/lease_views.xml',
        'views/rent_payment_views.xml',
        'views/menu.xml',
        'views/property_crm_views.xml',
        'views/property_sale_views.xml',
        'report/lease_summary_template.xml',

        'wizard/lease_summarty_wizard_view.xml',
        'wizard/rent_payment_excel_wizard.xml',

        'data/property_management_demo.xml',
        'data/tenant_id.xml',
        'data/payment_sq.xml',
        'data/cron.xml',
        'data/email.xml',
    ],
    'installable': True,
    'application': True,
}
