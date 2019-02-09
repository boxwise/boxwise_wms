from odoo import models, fields, api
from odoo import exceptions
import logging

_logger = logging.getLogger(__name__)

class GenerateQRCountWizard(models.TransientModel):
    _name = 'boxwise_wms.qr.generate.wizard'
    _description = 'Number of QR codes to be generated'
    number = fields.Char(string='Number of labels', required=True, default=0)

    @api.multi
    def mass_generate(self):
        _logger.debug('Starting batch QR codes generation')

        packageModel = self.env['stock.quant.package']
        number_of_packages = int(self.number)
        createdPackages = []

        for _ in range(number_of_packages):
            createdPackages.append(packageModel.create({}))

        return self.open_packages_list()
        
    def open_packages_list(self):
        return {
            'type':'ir.actions.act_window',
            'res_model':'stock.quant.package',
            'view_type':'list',
            'view_mode':'list',
            'target':'current',
        }