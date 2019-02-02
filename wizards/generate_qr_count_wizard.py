from odoo import models, fields, api
from odoo import exceptions
import logging

_logger = logging.getLogger(__name__)

class GenerateQRCountWizard(models.TransientModel):
    _name = 'boxwise.qr.generate.wizard'
    _description = 'Number of QR codes to be generated'
    number = fields.Char(string='Number of labels', required=True)
    create_uids = fields.Many2many('res.users', string='Created by')
    make_big_labels = fields.Boolean('Make big labels including fields for box number and contents', default=False)

    @api.multi
    def mass_generate(self):
        _logger.debug('Starting batch QR codes generation')
        self.ensure_one()
        vals = {}
        
        if not (self.number or self.create_uids):
            raise exceptions.ValidationError('No data to update!')
            _logger.debug('Mass generate failed')
        if self.number:
            vals['number'] = self.number
        if self.create_uids:
            vals['user_id'] = self.create_uids
