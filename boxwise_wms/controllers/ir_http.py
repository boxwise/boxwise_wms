# -*- coding: utf-8 -*-
import logging
import werkzeug
import werkzeug.utils
import werkzeug.exceptions
from odoo import http, models
_logger = logging.getLogger(__name__)


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'
    _description = "HTTP routing for Boxwise"

    @classmethod
    def _handle_exception(cls, exception):
        try:
            return super(IrHttp, cls)._handle_exception(exception)
        except (http.SessionExpiredException):
            _logger.info("Redirecting to Login", exc_info=True)
            return werkzeug.utils.redirect('/web/login', 302)

