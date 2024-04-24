# -*- coding: utf-8 -*-

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    custom_footer = fields.Binary(string='Custom Footer', readonly=False, )
    custom_header = fields.Binary(string='Custom Header', readonly=False, )
    arabic_company_name = fields.Char(string='Arabic Company Name')
