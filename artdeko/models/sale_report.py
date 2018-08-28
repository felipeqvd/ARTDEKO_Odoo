# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleReport(models.Model):
    _inherit = 'sale.report'
    
    @api.model
    def _select(self):
        new_select_str = super(SaleReport, self)._select()
        new_select_str += ",t.l10n_mx_edi_code_sat_id"        
        return new_select_str
    