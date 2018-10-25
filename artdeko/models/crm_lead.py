# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.tools.misc import formatLang
from odoo.addons import decimal_precision as dp

class Lead(models.Model):
    _inherit = 'crm.lead'
    @api.multi
    def action_new_quotation_request(self):
        """
        Request quotation.
        """
        quotation_request = {}        
        quotation_request = {
            'type': 'ir.actions.act_window',
            'res_model': 'mail.activity',
            'view_mode': 'form',
            'view_type': 'form',
            'views': [[False, 'form']],
            'target': 'new',
            'context': {
                'default_activity_type_id': 7,
                'default_res_id': self.id,
                'default_res_model': 'crm.lead',
                'default_summary': 'Solicitud de Cotización',
                'default_note': 'Por favor realizar cotización de esta oportunidad, con los siguientes productos:',
            },
        }        
        return quotation_request
    