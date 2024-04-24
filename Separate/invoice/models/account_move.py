# -*- coding: utf-8 -*-
from num2words import num2words
from odoo.exceptions import UserError
from odoo.tools import float_repr
import base64

from odoo import api, fields, models, tools, _
import logging


class AccountMove(models.Model):
    _inherit = 'account.move'

    affiliates = fields.Char(string='Affiliates')
    arabic_affiliates = fields.Char(string='Arabic Affiliates')
    contract_no = fields.Char(string='Contract No')
    arabic_contract_no = fields.Char(string='Arabic Contract No')
    client_reference = fields.Char(string='Client Reference')
    arabic_client_reference = fields.Char(string='Arabic Client Reference')
    ses_no = fields.Char(string='SES No')
    arabic_ses_no = fields.Char(string='Arabic SES No')

    po_number = fields.Char('PO Number')
    arabic_po_number = fields.Char('Arabic PO Number')
    received_by = fields.Many2one('res.users', string='Received By')
    po_date = fields.Date(string="PO Date")
    cr = fields.Char(string="CR")
    location = fields.Many2one(comodel_name="stock.location", string="Location")
    service_period = fields.Char(string="Serices Period")
    arabic_service_period = fields.Char(string="Arabic Serices Period")

    l10n_sa_qr_code_str_cs = fields.Char(string='Zatka QR Code', compute='_compute_qr_code_str_cs')
    l10n_sa_confirmation_datetime_cs = fields.Datetime(string='Confirmation Date', readonly=True, copy=False)

    @api.depends('country_code', 'move_type')
    def _compute_show_delivery_date(self):
        # EXTENDS 'account'
        super()._compute_show_delivery_date()
        for move in self:
            if move.country_code == 'SA':
                move.show_delivery_date = move.is_sale_document()

    @api.depends('amount_total_signed', 'amount_tax_signed', 'l10n_sa_confirmation_datetime_cs', 'company_id',
                 'company_id.vat')
    def _compute_qr_code_str_cs(self):
        """ Generate the qr code for Saudi e-invoicing. Specs are available at the following link at page 23
        https://zatca.gov.sa/ar/E-Invoicing/SystemsDevelopers/Documents/20210528_ZATCA_Electronic_Invoice_Security_Features_Implementation_Standards_vShared.pdf
        """

        def get_qr_encoding_cs(tag, field):
            company_name_byte_array = field.encode()
            company_name_tag_encoding = tag.to_bytes(length=1, byteorder='big')
            company_name_length_encoding = len(company_name_byte_array).to_bytes(length=1, byteorder='big')
            return company_name_tag_encoding + company_name_length_encoding + company_name_byte_array

        for record in self:
            qr_code_str = ''
            if record.company_id.vat:
                seller_name_enc = get_qr_encoding_cs(1, record.company_id.display_name)
                company_vat_enc = get_qr_encoding_cs(2, record.company_id.vat)
                invoice_total_enc = get_qr_encoding_cs(4, float_repr(abs(record.amount_total_signed), 2))
                total_vat_enc = get_qr_encoding_cs(5, float_repr(abs(record.amount_tax_signed), 2))

                str_to_encode = seller_name_enc + company_vat_enc + invoice_total_enc + total_vat_enc
                qr_code_str = base64.b64encode(str_to_encode).decode()
            record.l10n_sa_qr_code_str_cs = qr_code_str

    @api.model
    def to_arabic_numerals(self, number):
        arabic_numerals_map = str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩')
        return str(number).translate(arabic_numerals_map)

    @api.depends('amount_total')
    def _convert_amount_to_text_arabic(self):
        for rec in self:
            def _num2words(number, lang):
                try:
                    return num2words(number, lang=lang).title()
                except NotImplementedError:
                    return num2words(number, lang='ar_001').title()

            if num2words is None:
                logging.getLogger(__name__).warning(
                    "The library 'num2words' is missing, cannot render textual amounts.")
                return ""
            amt_word = []
            formatted = "%.{0}f".format(rec.currency_id.decimal_places) % rec.amount_total
            parts = formatted.partition('.')
            integer_value = int(parts[0])
            fractional_value = int(parts[2] or 0)
            if rec.currency_id.currency_unit_label == 'Saudi Riyal,':
                amt_word = rec.currency_id.currency_unit_label.replace('Saudi Riyal,', 'ريال سعودي')
            amount_words = tools.ustr('{amt_word} {amt_value}').format(
                amt_word=amt_word or '',
                amt_value=_num2words(integer_value, lang='ar_001'),

            )
            currency_subunit = []
            if not rec.currency_id.is_zero(rec.amount_total - integer_value):
                if rec.currency_id.currency_subunit_label == 'Halala':
                    currency_subunit = rec.currency_id.currency_subunit_label.replace('Halala', 'هللة')
                amount_words += ' ' + tools.ustr(' {amt_value} {amt_word} ').format(
                    amt_word=currency_subunit or '',
                    amt_value=_num2words(fractional_value, lang='ar_001'),
                )
            return amount_words

    # @api.depends('amount_total')
    # def _convert_amount_to_text(self):
    #     for rec in self:
    #         def _num2words(number, lang):
    #             try:
    #                 return num2words(number, lang=lang).title()
    #             except NotImplementedError:
    #                 return num2words(number, lang='en').title()
    #
    #         if num2words is None:
    #             logging.getLogger(__name__).warning(
    #                 "The library 'num2words' is missing, cannot render textual amounts.")
    #             return ""
    #
    #         formatted = "%.{0}f".format(rec.currency_id.decimal_places) % rec.amount_total
    #         parts = formatted.partition('.')
    #         integer_value = int(parts[0])
    #         fractional_value = int(parts[2] or 0)
    #
            # amount_words = tools.ustr('{amt_word} {amt_value}').format(
            #     amt_word=rec.currency_id.currency_unit_label,
            #     amt_value=_num2words(integer_value, lang='en'),
            #
            # )
    #         if not rec.currency_id.is_zero(rec.amount_total - integer_value):
    #             amount_words += ' ' + tools.ustr(' {amt_value} {amt_word} ').format(
    #                 amt_word=rec.currency_id.currency_subunit_label,
    #                 amt_value=_num2words(fractional_value, lang='en'),
    #             )
    #         return amount_words

    @api.depends('amount_total')
    def _convert_amount_to_text(self):
        for rec in self:
            def number_to_words(num):
                units = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']
                teens = ['Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen',
                         'Eighteen', 'Nineteen']
                tens = ['', 'Ten', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']

                if num < 10:
                    return units[num]
                elif num < 20:
                    return teens[num - 10]
                elif num < 100:
                    return tens[num // 10] + ('' if num % 10 == 0 else ' ' + units[num % 10])
                elif num < 1000:
                    return units[num // 100] + ' Hundred' + ('' if num % 100 == 0 else ' ' + number_to_words(num % 100))
                elif num < 1000000:
                    return number_to_words(num // 1000) + ' Thousand' + (
                        '' if num % 1000 == 0 else ' ' + number_to_words(num % 1000))
                elif num < 1000000000:
                    return number_to_words(num // 1000000) + ' Million' + (
                        '' if num % 1000000 == 0 else ' ' + number_to_words(num % 1000000))
                else:
                    return number_to_words(num // 1000000000) + ' Billion' + (
                        '' if num % 1000000000 == 0 else ' ' + number_to_words(num % 1000000000))

            formatted = "%.{0}f".format(rec.currency_id.decimal_places) % rec.amount_total
            integer_part, fractional_part = formatted.split('.')
            integer_value = int(integer_part)
            fractional_value = int(fractional_part)

            amount_words = rec.currency_id.currency_unit_label + ' ' + number_to_words(integer_value)

            if fractional_value:
                amount_words += ' And ' + number_to_words(fractional_value) + ' ' + rec.currency_id.currency_subunit_label

            return amount_words


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def get_tax_info(self, tax_ids, amount):
        tax_percentage = 0
        for tax in tax_ids:
            tax_percentage += tax.amount
        tax_amount = (amount * tax_percentage / 100)
        return {'tax_percentage': tax_percentage,
                'tax_amount': tax_amount}

    def get_discount_amount(self, qty, unit_price, discount_percentage):
        if discount_percentage > 0:
            return round(((qty * unit_price) * discount_percentage) / 100, 2)
        else:
            return 0
