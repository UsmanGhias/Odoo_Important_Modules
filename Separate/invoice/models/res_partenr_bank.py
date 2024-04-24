# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    custom_iban = fields.Char(string="IBAN")
