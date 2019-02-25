# -*- coding: utf-8 -*-
{
    'name': "Boxwise Warehouse Management",

    'summary': "WMS for inkind-donations",

    'author': "Humanilog",
    'website': "www.humanilog.org",

    'category': 'Uncategorized',
    'version': '11.0.1.0.5',

    'depends': ['stock', 'website_menu_by_user_status'],
    'post_init_hook': 'post_init_hook',

    'data': [
        'data/main_partner.xml',
        'data/website_menu.xml',
        'data/website_page.xml',
        'data/website_settings.xml',
        'data/inventory_settings.xml',
        'data/user_groups.xml',
        'views/packages.xml',
        'views/edit_package.xml',
        'views/find_package.xml',
        'views/show_package.xml',
        'templates/layout.xml',
        'templates/assets.xml',

        'qrcodes/generate_qr.xml',
        'qrcodes/report.paperformat.csv',
        'qrcodes/report_qr_codes.xml',
        'qrcodes/report_qr_codes_alt.xml',
        'qrcodes/report_qr_codes_alt2.xml',

        # leave at bottom
        'data/init.xml',
    ],
}
