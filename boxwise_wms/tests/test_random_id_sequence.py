from odoo.tests import common
from odoo.exceptions import Warning as UserWarning
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
        sequence_model.write({'prefix': 'prefix-'})
        sequence_model.write({'suffix': '-suffix'})
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
        sequence_model.write({'implementation': 'random_id'})
        sequence_model.write({'padding': 5})
        generatedSequence = sequence_model.next_by_code('stock.quant.package')
        sequence_model.write({'padding': 7})
        generatedSequence2 = sequence_model.next_by_code('stock.quant.package')
        self.assertEqual(len(generatedSequence)<len(generatedSequence2), True)

    @common.post_install(True)
    def test_random_id_sequence_is_unique(self):
        #creates 9 packages with IDs from 0 to 9 to ensure random ID with only one digit can't be generated anymore
        package_model = self.env['stock.quant.package']
        for i in range(10):
            package_model.create({'name': str(i)})

        #set lenght of sequence to 1 (enabling only IDs from 0 to 9, which are already taken)
        sequence_model = self.env.ref("stock.seq_quant_package")
        sequence_model.write({'implementation': 'random_id'})
        sequence_model.write({'padding': 1})
        try:
            sequence_model.next_by_code('stock.quant.package')
        #if the warning is published, one digit random_id sequence could not be generated (because all IDs are already taken)
        except UserWarning:
            self.assertTrue(True)
            return
        self.assertTrue(False)

        