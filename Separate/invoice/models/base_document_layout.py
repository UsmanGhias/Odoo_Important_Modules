# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class BaseDocumentLayout(models.TransientModel):
    _inherit = "base.document.layout"

    custom_footer = fields.Binary(string='Custom Footer', readonly=False, related="company_id.custom_footer", )
    custom_header = fields.Binary(string='Custom Header', readonly=False, related="company_id.custom_header", )
