# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleReport(models.Model):
    _inherit = 'sale.report'
    
    @api.model
    def _select(self,values):
        record = super(sale.report, self)._select(values)
        record['_select_str'] += ", p.l10n_mx_edi_code_sat_id"        
        return record
    