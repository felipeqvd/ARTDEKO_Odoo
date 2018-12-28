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