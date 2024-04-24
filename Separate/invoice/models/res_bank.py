# -*- coding: utf-8 -*-

from odoo import fields, models


class ResBank(models.Model):
    _inherit = 'res.bank'

    arabic_bank_name = fields.Char(string="Arabic Bank Name")
