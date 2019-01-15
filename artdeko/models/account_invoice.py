# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.addons import decimal_precision as dp
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.tools.misc import formatLang

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'    
    # Adicionar campo de cliente de referencia
    ref_partner_id = fields.Many2one('res.partner', string='Cliente referencia', change_default=True, readonly=True, states={'draft': [('readonly', False)]}, track_visibility='always')
    
    @api.multi
    def _l10n_mx_edi_get_payment_policy(self):
        '''Esta función inhabilita el automatismo del método de pago de la localización Mexicana.
        Se evita que la factura quede con método PUE si está antes del 17 del siguiente mes. 
        '''
        super(AccountInvoice, self)._l10n_mx_edi_get_payment_policy()
        self.ensure_one()
        version = self.l10n_mx_edi_get_pac_version()
        term_ids = self.payment_term_id.line_ids
        if version == '3.2':
            if len(term_ids.ids) > 1:
                return 'Pago en parcialidades'
            else:
                return 'Pago en una sola exhibición'
        elif version == '3.3':            
            if len(term_ids.ids) > 1:
                return 'PPD'
            else:
                return 'PUE'
        return ''