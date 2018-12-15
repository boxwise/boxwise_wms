# -*- coding: utf-8 -*-
from odoo import http

class LabelingController(http.Controller):
    @http.route('/boxwise/labeling/', auth='user')
    def index(self, **kw):
        packages = http.request.env['stock.quant.package']
        return http.request.render('boxwise_WMS.labeling', {
            'packages': packages.search([])
        })

    @http.route('/boxwise/labeling/<model("stock.quant.package"):package>/', auth='user')
    def edit_package(self, package):
        return http.request.render('boxwise_WMS.edit_package', {
            'package': package
        })
