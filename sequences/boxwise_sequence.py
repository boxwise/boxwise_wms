from odoo import fields, models, api, _
from odoo.exceptions import Warning as UserWarning
import random, wdb
import string
import logging

_logger = logging.getLogger(__name__)

class CustomPackageSequence(models.Model):
    """ Boxwise sequence.

    Extended ir.sequence defined in ir_sequence.py. Random ID option has been added to allow random Id generation

    """
    _inherit = 'ir.sequence'
    implementation = fields.Selection([('standard', 'Standard'), ('no_gap', 'No gap'), ('random_id', 'Random ID')],
                                      string = 'Implementation', required=True, default='standard',
                                      help = "Three sequence object implementations are offered: Standard, "
                                           "'No gap' and 'Random ID'. 'No gap' is slower than the 'sequence' but forbids any "
                                           "gap in the sequence (while they are possible in the 'sequence'). Random ID generates random sequence of characters")

    #overriding _next() method of ir.sequence
    def _next(self):
        if self.implementation == 'random_id':
            return self._generate_random_id()    #generate our own random ID
        else:
            return super(CustomPackageSequence, self)._next() #superclass sequence logic

    @api.model
    def _generate_random_id(self):
        _logger.debug('Starting creation of random box number')

        current_company_id = self.env['res.company']._company_default_get().id
        tries = 0
        max_tries = 50
        while tries < max_tries:
            random_sequence = ''.join(random.SystemRandom().choice(string.digits) for _ in range(self.padding))
            package_number = self._append_prefix_and_suffix(random_sequence)

            #check if this box number already exists (in current company only!)
            if not self.env['stock.quant.package'].search_count([('name','=',package_number),('company_id','=',current_company_id)]):
                break
            tries += 1
        if tries == max_tries:
            raise UserWarning(_('Unable to generate an unique package box name'))

        _logger.debug('Random box number successfully created')
        return package_number

    @api.model
    def _append_prefix_and_suffix(self, random_sequence):
        _logger.debug('Adding prefix and suffix to random requence to create random box number')
        if (self.prefix):
            random_sequence = self.prefix + random_sequence
        if (self.suffix):
            random_sequence = random_sequence + self.suffix
        return random_sequence
