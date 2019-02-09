from odoo import models, fields, api
from odoo import exceptions
import logging

_logger = logging.getLogger(__name__)

# Wizard used to get input from user to generate set number of packages
class GenerateQrInBulk(models.TransientModel):
    _name = 'boxwise_wms.qr.generate.wizard'
    _description = 'Number of QR codes to be generated'
    number = fields.Char(string='Number of labels', required=True, default=0)

    @api.multi
    def mass_generate(self):
        _logger.debug('Starting batch QR codes generation')

        package_model = self.env['stock.quant.package']
        number_of_packages = int(self.number)
        created_packages = []  #TODO: pass these into the automatically downloaded report

        for _ in range(number_of_packages):
            created_packages.append(package_model.create({}))

        _logger.debug('Successfully generated %s new packages', self.number, exc_info=1)
        return self.open_packages_list()
        
    def open_packages_list(self):
        return {
            'type':'ir.actions.act_window',
            'res_model':'stock.quant.package',
            'view_type':'list',
            'view_mode':'list',
            'target':'current',
        }