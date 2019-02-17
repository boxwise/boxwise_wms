from odoo import fields, models, _
from odoo.exceptions import Warning as UserWarning
import random
import string

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
        
    #overriding default _next() sequence method
    def _next(self):
        if self.implementation == 'random_id':
            return self.generate_random_id()    #generate our own random ID
        else:
            return super(CustomPackageSequence, self)._next() #superclass sequence logic

    def generate_random_id(self):
        tries = 0
        max_tries = 50
        while tries < max_tries:
            random_sequence = ''.join(random.SystemRandom().choice(string.digits) for _ in range(self.padding))
            package_number = self.append_prefix_and_suffix(random_sequence)
            if not self.env['stock.quant.package'].search_count([('name','=',package_number)]):
                break
            tries += 1
        if tries == max_tries:
            raise UserWarning(_('Unable to generate an unique package box name'))
        return package_number

    def append_prefix_and_suffix(self, random_sequence):
        if (self.prefix):
            random_sequence = self.prefix + random_sequence
        if (self.suffix):
            random_sequence = random_sequence + self.suffix
        return random_sequence