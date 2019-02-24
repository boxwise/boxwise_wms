from odoo import http
import logging
import werkzeug.exceptions
from odoo.addons.website.controllers.main import Website

_logger = logging.getLogger(__name__)


class BoxwiseWebsite(Website):
    @http.route('/', type='http', auth="public", website=True)
    def index(self, **kw):
        try:
            return super(BoxwiseWebsite, self).index(**kw)
        except (werkzeug.exceptions.NotFound):
            # we're a public user, and there's no home page
            # so we take people to a login page instead
            _logger.info("Redirecting to Login from Index", exc_info=True)
            return werkzeug.utils.redirect('/web/login', 302)
