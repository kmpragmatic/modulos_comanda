{
    'name': 'Pago con GETNET AutoServicio',
    'category': 'Tools',
    'summary': 'AutoServicio Adicionales.',
    'author': 'KTM - kelvinthony@gmail.com',
    'depends': ['pos_self_order', 'pos_equipment'],
    'application': False,
    'version': '17.0.0.1',
    'license': 'AGPL-3',
    'support': 'kelvinthony@gmail.com',
    'website': '',
    'installable': True,
    'data': [

    ],
    'images': [
        'static/description/icon.png',
    ],
    "assets": {
        "pos_self_order.assets": [
            'pos_self_order_getnet/static/src/app/pages/payment_page/payment_page.js',
            # 'pos_self_order_getnet/static/src/app/pages/payment_page/payment_page.xml',
        ],
    }
}
