# -*- coding: utf-8 -*-
{
    'name': "Boxwise Warehouse Management",

    'summary': """
    WMS for inkind-donations
        """,

    'author': "Humanilog",
    'website': "www.humanilog.org",

    'category': 'Uncategorized',
    'version': '11.0.1.0.1',

    'depends': [
	    'stock', 
	    'stock_picking_barcode'
    ],
    'data': [
        'data/product.category.csv',
        'data/product.template.csv',
	'data/product.attribute.csv',
	#'data/product.attribute.value.csv',
    ],
}
