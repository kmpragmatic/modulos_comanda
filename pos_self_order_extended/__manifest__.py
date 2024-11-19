{
    'name': 'Adicionales AutoServicio',
    'category': 'Tools',
    'summary': 'AutoServicio Adicionales.',
    'author': 'CTiEG - hola@ctieg.com',
    'depends': ['pos_self_order', 'pos_equipment'],
    'application': False,
    'version': '17.0.0.1',
    'license': 'AGPL-3',
    'support': 'hola@ctieg.com',
    'website': 'https://www.ctieg.com',
    'installable': True,
    'data': [
        'views/por_order.xml',
    ],
    'images': [
        'static/description/icon.png',
    ],
    "assets": {
        "pos_self_order.assets": [
            "pos_self_order_extended/static/src/xml/product_list_page.xml",
        ],
    }
}
