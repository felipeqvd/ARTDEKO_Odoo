# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.addons import decimal_precision as dp
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.tools.misc import formatLang

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.multi
    def purchase_amount_to_text(self):
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
        purchase_order_words = '%(words)s %(amount_d)02d/100 %(curr_t)s' % dict(
            words=words, amount_d=amount_d, curr_t=currency_type)
        return purchase_order_words
    # Adicionar campo para descuentos
    # amount_discounted 
    amount_discounted = fields.Monetary(string='Descuentos', store=True, readonly=True, compute='_amount_all')
    # Incluir descuentos en los cálculos
    @api.model
    def _amount_all(self):
        super(PurchaseOrder, self)._amount_all()
        for order in self:
            amount_discounted = 0.0
            for line in order.order_line:
                amount_discounted += line.amount_discount_line
            order.update({
                'amount_discounted': order.currency_id.round(amount_discounted),                
            })
    # Poner los precios del proveedor
    @api.model
    @api.onchange('partner_id', 'company_id')
    def onchange_partner_id(self):
        super(PurchaseOrder, self).onchange_partner_id()
        for order in self:            
            for line in order.order_line:
                seller = line.product_id._select_seller(
                    partner_id=line.partner_id,
                    quantity=line.product_qty,
                    date=line.order_id.date_order and line.order_id.date_order[:10],
                    uom_id=line.product_uom)

                if seller or not line.date_planned:
                    line.date_planned = line._get_date_planned(seller).strftime(DEFAULT_SERVER_DATETIME_FORMAT)

                price_unit = line.env['account.tax']._fix_tax_included_price_company(seller.price, line.product_id.supplier_taxes_id, line.taxes_id, line.company_id) if seller else 0.0
                if price_unit and seller and line.order_id.currency_id and seller.currency_id != line.order_id.currency_id:
                    price_unit = seller.currency_id.compute(price_unit, line.order_id.currency_id)

                if seller and line.product_uom and seller.product_uom != line.product_uom:
                    price_unit = seller.product_uom._compute_price(price_unit, line.product_uom)

                line.price_unit = price_unit
    #Conectar purchase oreder con sale order
    sale_order = fields.Many2one('sale.order', 'Venta')
    
class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    # Adicionar campo para descuentos
    # discount
    discount = fields.Float(string='Descuento (%)', digits=dp.get_precision('Discount'), default=0.0)
    amount_discount_line = fields.Monetary(compute='_compute_amount', string='Importe descuento', store=True)
    # Incluir el descuento en los cálculos
    @api.model
    @api.depends('product_qty', 'price_unit', 'taxes_id', 'discount')
    def _compute_amount(self):
        super(PurchaseOrderLine, self)._compute_amount()
        for line in self:
            amount_discount = (line.discount * line.price_unit)/100
            amount_discount_line = amount_discount * line.product_qty
            taxes = line.taxes_id.compute_all(line.price_unit - amount_discount, line.order_id.currency_id, line.product_qty, product=line.product_id, partner=line.order_id.partner_id)
            line.update({
                'amount_discount_line': amount_discount_line,
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })