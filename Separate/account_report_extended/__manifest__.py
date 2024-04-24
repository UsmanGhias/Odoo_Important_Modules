# -*- coding: utf-8 -*-
{
    # App information
    'name': 'TUS Account Report Extended',
    'category': '',
    'summary': 'Basic module for Custom Account Report',
    'description': 'Basic module for Custom Account Report',
    'version': '17.0.1.9',
    'author': 'TechUltra Solution',
    'license': 'LGPL-3',
    'company': 'TechUltra Solution',
    'website': 'https://www.techultrasolutions.com',

    # Dependencies
    'depends': ['base', 'account', 'account_reports'],

    # Data
    'data': [
        'data/aged_partner_balance.xml',
        'data/partner_ledger.xml',
    ],

    # Technical
    'installable': True,
    'auto_install': False,
    'application': False,
}
