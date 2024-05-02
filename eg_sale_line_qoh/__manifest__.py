{
    "name": "On Hand Qty on Sale Order",
    "summary": "Display On hand quantity and forecasted qty in sale order line.",
    "version": "17.0",
    "category": "Sales",
    "description": "Display On hand quantity and forecasted qty in sale order line.",
    "author": "Usman Ghias",
    "website": "https://www.codcrafters.org",
    "depends": ['sale_management'],
        
    "data": [
        'views/sale_order_line_view.xml',
        'report/sale_order_report.xml'
    ],

    'installable': True,
    'auto_install': False,
    'application': True,
}
