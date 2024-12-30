{
    'name': 'Adicionales AutoServicio',
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
        'views/por_order.xml',
    ],
    'images': [
        'static/description/icon.png',
    ],
    "assets": {
        "pos_self_order.assets": [
            'pos_self_order_extended/static/src/app/pages/category_list_page/category_list_page.js',
            'pos_self_order_extended/static/src/app/pages/product_list_page/product_list_page.js',
            'pos_self_order_extended/static/src/app/pages/product_list_page/product_list_page.xml',
            'pos_self_order_extended/static/src/app/pages/category_list_page/category_list_page.xml',
            'pos_self_order_extended/static/src/app/pages/category_list_page/category_list_page.scss',
            'pos_self_order_extended/static/src/app/self_order_index_patch.js',
            'pos_self_order_extended/static/src/app/self_order_index.xml',
        ],
    }
}
