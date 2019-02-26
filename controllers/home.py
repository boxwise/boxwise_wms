# -*- coding: utf-8 -*-
from odoo import http
import logging
import werkzeug

_logger = logging.getLogger(__name__)


class HomeController(http.Controller):
    # Find box. For now it is our home.
    @http.route('/home', type='http', auth='user', website=True)
    def find_package(self, **kw):
        packages = http.request.env['stock.quant.package'].search([])
        empty, filled = [], []
        for pack in packages:
            if pack.move_line_ids:
                filled.append(pack)
            else:
                empty.append(pack)
        return http.request.render('boxwise_wms.home', {
            'empty_packages': empty,
            'filled_packages': filled
        })

    @http.route('/', type='http', auth="public", website=True)
    def index(self, **kw):
        try:
            return super(BoxwiseWebsite, self).index(**kw)
        except (werkzeug.exceptions.NotFound):
            # we're a public user, and there's no home page
            # so we take people to a login page instead
            _logger.info("Redirecting to Login from Index", exc_info=True)
            return werkzeug.utils.redirect('/web/login', 302)

