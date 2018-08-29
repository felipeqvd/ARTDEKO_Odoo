# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleReport(models.Model):
    _inherit = 'sale.report'
    
    @api.model
    def _select(self):
        new_select_str = super(SaleReport, self)._select()
        new_select_str += ",t.l10n_mx_edi_code_sat_id as sat_id, p.image_medium"     
        return new_select_str
    def _group_by(self):
        new_group_by_str = super(SaleReport, self)._group_by()
        new_group_by_str = """
            GROUP BY l.product_id,
                    l.order_id,
                    t.uom_id,
                    t.categ_id,
                    t.l10n_mx_edi_code_sat_id,
                    s.name,
                    s.date_order,
                    s.confirmation_date,
                    s.partner_id,
                    s.user_id,
                    s.state,
                    s.company_id,
                    s.pricelist_id,
                    s.analytic_account_id,
                    s.team_id,
                    p.product_tmpl_id,
                    partner.country_id,
                    partner.commercial_partner_id
        """
        return new_group_by_str
    