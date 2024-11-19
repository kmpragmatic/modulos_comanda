# -*- coding: utf-8 -*-
{
    'name': 'Odoo REST API',
    'version': '17.0.1.14.8',
    'category': 'Extra Tools',
    'author': "CTiEG'",
    'license': 'OPL-1',
    'website': 'https://www.ctieg.com',
    'summary': """Enhanced RESTful API access to Odoo resources with (optional) predefined and tree-like schema of response Odoo fields
        ============================
        Tags: restapi, connector, connection, integration, endpoint, endpoints, route, routes, call method, calling method, openapi, oauth, swagger, webhook, webhooks, report, reports
        """,
    'external_dependencies': {
        'python': ['simplejson'],
    },
    'depends': [
        'base',
        'web',
    ],
    'data': [
        'data/ir_configparameter_data.xml',
        'data/ir_cron_data.xml',
        'security/ir.model.access.csv',
        'views/ir_model_view.xml',
    ],
    'images': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
