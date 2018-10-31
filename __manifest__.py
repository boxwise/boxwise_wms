# -*- coding: utf-8 -*-
{
    'name': "Boxwise Products Data",

    'summary': """
    Load all products of Boxwise!
        """,

    'author': "Humanilog",
    'website': "www.humanilog.org",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['stock'],

    'data': [
	    'data/product.template.csv',
	    'data/product.category.csv',
	    'data/product.attribute.csv',
	    'data/product.attribute.value.csv',
    ],
}
