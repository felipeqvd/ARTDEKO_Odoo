# -*- coding: utf-8 -*-
from odoo import http

# class Artdeko(http.Controller):
#     @http.route('/artdeko/artdeko/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/artdeko/artdeko/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('artdeko.listing', {
#             'root': '/artdeko/artdeko',
#             'objects': http.request.env['artdeko.artdeko'].search([]),
#         })

#     @http.route('/artdeko/artdeko/objects/<model("artdeko.artdeko"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('artdeko.object', {
#             'object': obj
#         })