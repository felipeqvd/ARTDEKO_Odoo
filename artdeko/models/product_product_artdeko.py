# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ProductProductArtdeko(models.Model):
    _inherit = 'product.product'

    @api.multi
    def _sales_product_attributes(self):
        r = {}       
        domain = [
            ('state', 'in', ['sale', 'done']),
            ('product_id', 'in', self.ids),
        ]
        for group in self.env['sale.report'].read_group(domain, ['product_id', 'product_uom_qty', 'l10n_mx_edi_code_sat_id'], ['product_id']):
            r[group['product_id'][0]] = group['l10n_mx_edi_code_sat_id']        
        return r