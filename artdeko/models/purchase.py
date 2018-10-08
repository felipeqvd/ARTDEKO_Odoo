# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class PurchaseOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def purchase_amount_to_text(self):        
        purchase_order_words = 'Valor en letras'
        return purchase_order_words