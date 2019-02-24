# -*- coding: utf-8 -*-
from odoo import http
import wdb


import werkzeug
from odoo.addons.http_routing.models.ir_http import slug

class LabelingController(http.Controller):
    @http.route('/findbox', type='http', auth='user', website=True)
    def find_package(self, **kw):
        #wdb.set_trace()
        packages = http.request.env['stock.quant.package'].search([])
        empty, filled = [], []
        for pack in packages:
            if pack.move_line_ids:
                filled.append(pack)
            else:
                empty.append(pack)
        return http.request.render('boxwise_wms.find_package', {
            'empty_packages': empty,
            'filled_packages': filled
        })

    @http.route('/box/<model("stock.quant.package"):package>/', type='http', auth='user', website=True)
    def show_package(self, package):
        #wdb.set_trace()
        return http.request.render('boxwise_wms.show_package', {
            'package': package
        })

    @http.route('/box/edit/<model("stock.quant.package"):package>/', type='http', auth='user', website=True)
    def edit_package(self, package):
        return http.request.render('boxwise_wms.edit_package', {
            'package': package
        })

    @http.route('/qrcode/<tenant>/<model("stock.quant.package"):package>/', auth='user')
    def qrcode(self, tenant, package):
        return werkzeug.utils.redirect('/boxwise/labeling/%s' % slug(package))

