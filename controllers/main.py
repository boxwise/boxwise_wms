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

    @http.route('/box/generate/', auth='user', methods=['POST'])
    def generate(self, count):

        package_model = http.request.env['stock.quant.package']
        docids = []
        for _ in range(int(count)):
            docids.append(package_model.create({}).id)

        return self._generate_qrcodes_report(docids)

    @http.route('/box/reprint/', auth='user', methods=['POST'])
    def reprint(self):

        packages = http.request.env['stock.quant.package'].search([])
        docids = []
        for pack in packages:
            if not any(pack.move_line_ids):
                docids.append(pack.id)

        return self._generate_qrcodes_report(docids)

    def _generate_qrcodes_report(self, docids):
        report = http.request.env['ir.actions.report']._get_report_from_name('boxwise_wms.report_qr_codes')
        context = dict(http.request.env.context)

        pdf = report.with_context(context).render_qweb_pdf(docids)[0]

        pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
        return http.request.make_response(pdf, headers=pdfhttpheaders)

