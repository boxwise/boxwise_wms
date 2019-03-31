from odoo.tests import common
import logging

_logger = logging.getLogger(__name__)

class TestRandomIdSequence(common.TransactionCase):
    #at_install = True
    #post_install = True

    def setUp(self):
        package_model = self.env['stock.quant.package']
        sequence_model = self.env['ir.sequence']
        super(TestRandomIdSequence, self).setUp()

    @common.post_install(True)
    #@common.at_install(True)
    def test_random_id_sequence(self):
        response = "x"
        self.assertEqual(response, 'hallo')