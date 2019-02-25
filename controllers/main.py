# -*- coding: utf-8 -*-
from odoo import http
import logging
import werkzeug
from odoo.addons.http_routing.models.ir_http import slug
_logger = logging.getLogger(__name__)


class LabelingController(http.Controller):
    @http.route('/findbox', type='http', auth='user', website=True)
    def find_package(self, **kw):
        packages = http.request.env['stock.quant.package'].search([])
        empty, filled = [], []
        for pack in packages:
            if pack.move_line_ids:
                filled.append(pack)
            else:
                empty.append(pack)
        return http.request.render('boxwise_wms.find_package', {
            'empty_packages': empty,
            'filled_packages': filled
        })

    @http.route('/box/<model("stock.quant.package"):package>/', type='http', auth='user', website=True)
    def show_package(self, package):
        return http.request.render('boxwise_wms.show_package', {
            'package': package
        })

    @http.route('/box/edit/<model("stock.quant.package"):package>/', type='http', auth='user', website=True)
    def edit_package(self, package):
        return http.request.render('boxwise_wms.edit_package', {
            'package': package
        })

    @http.route('/box/submit', type='http', auth='user', website=True)
    def write_package(self, **kw):
        attribute_ids = [att[9:] for att in kw.keys() if 'Attribute' in att]
        attribute_value_ids = [kw['Attribute'+att] for att in attribute_ids]
        search_string = [('product_tmpl_id', '=', int(kw['ProductTemplate']))]
        for att_val in attribute_value_ids:
            search_string.append(('attribute_value_ids', '=', int(att_val)))
        product = http.request.env['product.product'].search(search_string)
        product_uom_id = http.request.env.ref(
            'product.product_uom_unit').id
        location_dest_id = http.request.env.ref(
            'stock.stock_location_stock').id
        location_id = http.request.env.ref(
            'stock.stock_location_suppliers').id
        partner_id = http.request.env.ref(
            'boxwise_wms.res_partner_donor').id
        picking_type_id = http.request.env.ref(
            'stock.picking_type_in').id

        stock_picking = http.request.env['stock.picking'].create({
            'partner_id': partner_id,
            'location_id': location_id,
            'location_dest_id': location_dest_id,
            'picking_type_id': picking_type_id,
            'move_lines': [[0, 0, {'product_id': product.id,
                                   'name': product.name,
                                   'product_uom': product_uom_id
                                   }]]
        })
        _logger.debug(stock_picking)
        stock_picking.move_lines.ensure_one().write({
            'move_line_ids':
            [[0, 0,
              {'location_dest_id':	stock_picking.location_dest_id.id,
               'location_id':	stock_picking.location_id.id,
               'picking_id': stock_picking.id,
               'product_id':	product.id,
               'product_uom_id':	product_uom_id,
               'qty_done':	int(kw['items']),
               'result_package_id': int(kw['package']),
               }
              ]]})
        stock_picking.button_validate()

        return werkzeug.utils.redirect('/box/%s' % slug(stock_picking.move_line_ids.result_package_id))
