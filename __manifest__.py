# -*- coding: utf-8 -*-
{
    'name': "Boxwise Warehouse Management",

    'summary': "WMS for inkind-donations",

    'author': "Humanilog",
    'website': "www.humanilog.org",

    'category': 'Uncategorized',
    'version': '11.0.1.0.5',

    'depends': ['stock', 'website_menu_by_user_status'],

    'data': [
        'data/product.category.csv',
        'data/product_category.xml',
        'data/product.attribute.csv',
        'data/product.attribute.value.csv',
        'data/product.template.csv',
        'data/main_partner.xml',
        'data/report.paperformat.csv',
        'data/res.partner.csv',
        'data/website_menu.xml',
        'data/website_page.xml',
        'data/website_settings.xml',
        # 'data/website_redirect.xml',
        'data/user_groups.xml',
        'views/packages.xml',
        'views/edit_package.xml',
        'views/find_package.xml',
        'views/show_package.xml',
        'views/generate_qr.xml',
        'views/report_qr_codes.xml',
        'views/report_qr_codes_alt.xml',
        'templates/layout.xml',
        'templates/assets.xml',
        # demo data
        # 'demo/stock.move.csv',
        # 'demo/stock.picking.csv'
    ],
}
