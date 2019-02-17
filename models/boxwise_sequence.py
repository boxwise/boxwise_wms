from odoo import api, fields, models, _
from odoo.exceptions import Warning as UserWarning
import random
import string
import wdb

class CustomPackageSequence(models.Model):
    """ Boxwise sequence.

    Extended ir.sequence defined in ir_sequence.py. Random ID option has been added to allow random Id generation

    """    
    _inherit = 'ir.sequence'
    implementation = fields.Selection([('standard', 'Standard'), ('no_gap', 'No gap'), ('random_id', 'Random ID')],
                                      string='Implementation', required=True, default='standard',
                                      help="Two sequence object implementations are offered: Standard "
                                           "and 'No gap'. The later is slower than the former but forbids any "
                                           "gap in the sequence (while they are possible in the former).")
        
    #overriding default _next() sequence method
    def _next(self):
        if self.implementation == 'random_id':
            return self.generate_random_id()    #generate our own random ID
        else:
            return super(CustomPackageSequence, self)._next() #fallback to superclass sequence logic

    def generate_random_id(self):
        tries = 0
        max_tries = 50
        while tries < max_tries:
            package_number = ''.join(random.SystemRandom().choice(string.digits) for _ in range(8))
            if not self.env['stock.quant.package'].search_count([('display_name','=',package_number)]):
                break
            tries += 1
        if tries == max_tries:
            raise UserWarning(_('Unable to generate an Employee ID number that is unique.'))
        return package_number