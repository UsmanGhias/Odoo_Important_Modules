# -*- coding: utf-8 -*-
{
    # App information
    'name': 'TUS Tamimi Invoice',
    'category': '',
    'summary': 'Basic module for Custom Invoice',
    'description': 'Basic module for Custom Invoice',
    'version': '17.0.1.9',
    'author': 'TechUltra Solution',
    'license': 'LGPL-3',
    'company': 'TechUltra Solution',
    'website': 'https://www.techultrasolutions.com',

    # Dependencies
    'depends': ['base', 'account', 'contacts', 'product', 'sale', 'purchase', 'stock', ],

    # Data
    'data': [
        'views/res_partner_views_inherited.xml',
        'views/res_partenr_bank_extended.xml',
        'views/base_document_layout_view_extended.xml',
        'views/account_move_views_extended.xml',
        'reports/header_footer_invoice.xml',
        'reports/tus_invoice_report.xml',
        'reports/report_action.xml',
        'reports/tus_proforma_invoice.xml',
    ],

    # Technical
    'installable': True,
    'auto_install': False,
    'application': False,
}
