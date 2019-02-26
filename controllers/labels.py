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
