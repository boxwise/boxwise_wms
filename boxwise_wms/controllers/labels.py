# -*- coding: utf-8 -*-
from odoo import http
import logging
import werkzeug
from odoo.addons.http_routing.models.ir_http import slug
_logger = logging.getLogger(__name__)


class LabelController(http.Controller):
    
    # Do not change this route. All created boxes are pointing to this one
    @http.route('/qrcode/<tenant>/<model("stock.quant.package"):package>/', auth='user')
    def qrcode(self, tenant, package):
        if not any(package.move_line_ids):
            return werkzeug.utils.redirect('/box/%s/edit' % slug(package))
        else:
            return werkzeug.utils.redirect('/box/%s' % slug(package))

    @http.route('/labels/generate/', auth='user', methods=['POST'])
    def generate(self, count):

        package_model = http.request.env['stock.quant.package']
        docids = []
        for _ in range(int(count)):
            docids.append(package_model.create({}).id)

        return self._generate_qrcodes_report(docids)

    @http.route('/labels/reprint/', auth='user', methods=['POST'])
    def reprint(self):

        packages = http.request.env['stock.quant.package'].search([])
        docids = []
        for pack in packages:
            if not any(pack.move_line_ids):
                docids.append(pack.id)

        return self._generate_qrcodes_report(docids)

    def _generate_qrcodes_report(self, docids):
        report = http.request.env['ir.actions.report']._get_report_from_name('boxwise_wms.report_qr_codes_template')
        context = dict(http.request.env.context)

        pdf = report.with_context(context).render_qweb_pdf(docids)[0]

        pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
        return http.request.make_response(pdf, headers=pdfhttpheaders)