# -*- coding: utf-8 -*-
{
    'name': "Artdeko",

    'summary': """
        Modificaciones requeridas para la operación de ARTDEKO""",

    'description': """
        La instalación de este módulo realiza los siguientes cambios:
            -Modificación de pdf de cotización
            -Modificación de pdf de orden de compra
            -Modificación de pdf de factura
    """,

    'author': "Exion SAS",
    'website': "http://www.exion.com.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Personalización',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}