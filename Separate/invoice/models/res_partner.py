# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    arabic_partner_name = fields.Char(string="Arabic Name")
    additional_number = fields.Char(string="Additional No")
    arabic_additional_number = fields.Char(string="Arabic Additional No")
    vendor_no = fields.Char(string="Vendor No")
    arabic_vendor_no = fields.Char(string="Arabic Vendor No")

    # address fields
    arabic_custom_street = fields.Char(string="Street")
    arabic_custom_street2 = fields.Char(string="Street2")
    arabic_custom_zip = fields.Char(change_default=True, string="ZIP")
    arabic_custom_city = fields.Char(string="City")
    arabic_custom_state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict',
                                             domain="[('country_id', '=?', arabic_custom_country_id)]")
    arabic_custom_country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    arabic_custom_vat = fields.Char(string="Arabic Tax ID")
    arabic_custom_telephone = fields.Char(string="Arabic Phone")
    arabic_custom_mobile = fields.Char(string="Arabic Mobile")
    arabic_custom_email = fields.Char(string="Arabic Email")
    arabic_website = fields.Char(string="Arabic Website", readonly=False)
    building = fields.Char(string='Building')
    arabic_building = fields.Char(string='Arabic Building')
    cr_number = fields.Char(string='CR Number', readonly=False)

    partner_code = fields.Char(string="Partner Code", default='0000', required=True)
    display_name_partner_code = fields.Text(string="Display-Name", readonly=True,
                                            compute='_compute_display_name_partner_code', store=True, )

    @api.depends('partner_code', 'name')
    def _compute_display_name_partner_code(self):
        for record in self:
            if record.partner_code and record.name:
                record.display_name_partner_code = record.partner_code + '-' + record.name
            else:
                record.display_name_partner_code = False

    def name_get(self):
        res = []
        for rec in self:
            if rec.partner_code:
                res.append((rec.id, "%s-%s" % (rec.partner_code, rec.name)))
            else:
                res.append((rec.id, "%s" % rec.name))
        return res
