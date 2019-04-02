from odoo.tests import common
import logging
import re

_logger = logging.getLogger(__name__)

class TestRandomIdSequence(common.TransactionCase):
    def setUp(self):
        super(TestRandomIdSequence, self).setUp()

    #sequence_model = self.env['ir.sequence']
    #generatedSequence = sequence_model.next_by_code('stock.quant.package')
    #_logger.info(generatedSequence)

    @common.post_install(True)
    def test_random_id_sequence(self):
        current_company_id = self.env['res.company']._company_default_get().id
        sequence_model = self.env.ref("stock.seq_quant_package")
        if not sequence_model.implementation == 'random_id':
            sequence_model.write({'implementation': 'random_id'})
        generatedSequence = sequence_model.next_by_code('stock.quant.package')

        regexPattern = "\d{" + str(sequence_model.padding) + "}$"
        matchingSequence = re.findall(regexPattern, generatedSequence)
        self.assertEqual(len(matchingSequence), 1)

    @common.post_install(True)
    def test_random_id_sequence_with_prefix_and_suffix(self):
        sequence_model = self.env.ref("stock.seq_quant_package")
        sequence_model.write({'implementation': 'random_id'})
        sequence_model.prefix = "prefix-"
        sequence_model.suffix = "-suffix"
        generatedSequence = sequence_model.next_by_code('stock.quant.package')

        regexPattern = "prefix-\d{" + str(sequence_model.padding) + "}-suffix"
        matchingSequence = re.findall(regexPattern, generatedSequence)
        self.assertEqual(len(matchingSequence), 1)

    @common.post_install(True)
    def test_random_id_sequence_is_not_standard_or_nogap_sequence(self):
        sequence_model = self.env.ref("stock.seq_quant_package")
        sequence_model.write({'implementation': 'random_id'})
        generatedSequence = sequence_model.next_by_code('stock.quant.package')
        generatedSequence2 = sequence_model.next_by_code('stock.quant.package')
        difference = int(generatedSequence2) - int(generatedSequence)
        self.assertNotEquals(difference, 1)

    @common.post_install(True)
    def test_random_id_sequence_length(self):
        sequence_model = self.env.ref("stock.seq_quant_package")
        sequence_model.padding = 5
        generatedSequence = sequence_model.next_by_code('stock.quant.package')
        sequence_model.padding = 7
        generatedSequence2 = sequence_model.next_by_code('stock.quant.package')
        self.assertEqual(len(generatedSequence)<len(generatedSequence2), True)


        