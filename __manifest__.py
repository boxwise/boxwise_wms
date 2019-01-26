# -*- coding: utf-8 -*-
{
    'name': "Boxwise Warehouse Management",

    'summary': """
    WMS for inkind-donations
        """,

    'author': "Humanilog",
    'website': "www.humanilog.org",

    'category': 'Uncategorized',
    'version': '11.0.1.0.5',

    'depends': [
	    'stock', 'website'
    ],
    'data': [
        'data/product.category.csv',
        'data/product.template.csv',
	    'data/product.attribute.csv',
	    'data/product.attribute.value.csv',
	    'views/packages.xml',
        'views/edit_package.xml',
        'views/labeling.xml',
        'data/res.partner.csv',
        #'views/generate_qr.xml',
        'views/report_qr_codes.xml'
    ]
}
