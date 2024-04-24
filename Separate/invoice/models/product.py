# -*- coding: utf-8 -*-
from odoo import fields, api, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_arabic_name = fields.Char('')


class ProductProductInherit(models.Model):
    _inherit = 'product.product'

    product_arabic_name = fields.Char('')
