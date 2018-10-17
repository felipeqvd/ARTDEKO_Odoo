# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def sale_amount_to_text(self):
        """Method to transform a float amount to text words
        E.g. 100 - ONE HUNDRED
        :returns: Amount transformed to words mexican format for invoices
        :rtype: str
        """
        self.ensure_one()
        currency = self.currency_id.name.upper()
        # M.N. = Moneda Nacional (National Currency)
        # M.E. = Moneda Extranjera (Foreign Currency)
        currency_type = 'M.N' if currency == 'MXN' else 'M.E.'
        # Split integer and decimal part
        amount_i, amount_d = divmod(self.amount_total, 1)
        amount_d = round(amount_d, 2)
        amount_d = int(round(amount_d * 100, 2))
        words = self.currency_id.with_context(lang=self.partner_id.lang or 'es_ES').amount_to_text(amount_i).upper()
        sale_order_words = '%(words)s %(amount_d)02d/100 %(curr_t)s' % dict(
            words=words, amount_d=amount_d, curr_t=currency_type)
        return sale_order_words
    
    @api.multi
    def prepare_purchase_lines_from_sale_order(self):
        """
        Prepare the dict of values to create the new purchase line from sales order line.
        """
        purchase_lines = {}        
        purchase_lines = {
            'name': 'Orden de compra',
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order',
            'view_mode': 'form,tree,graph',            
        }
        self.ensure_one()       
        line3 = []
        for line in self.order_line:
            line1 = {'price_unit': line.price_unit,'product_qty': line.product_uom_qty,}            
            line2 = (0,0,line1)
            line3.append(line2)        
        purchase_lines['context'] = {'default_order_line': line3,}
        return purchase_lines
    