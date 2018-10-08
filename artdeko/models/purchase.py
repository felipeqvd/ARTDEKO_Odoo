# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    # Add a new column to the res.partner model, by default partners are not
    # instructors
    instructor = fields.Boolean("Instructor", default=False)