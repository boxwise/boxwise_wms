from odoo import http
import logging
import werkzeug.exceptions
from odoo.addons.http_routing.models.ir_http import slug

_logger = logging.getLogger(__name__)

class BoxController(http.Controller):
    # Box info screen
    @http.route('/box/<model("stock.quant.package"):package>/', type='http', auth='user', website=True)
    def view(self, package):
        return http.request.render('boxwise_wms.box_view', {
            'package': package
        })

    # Update or put new content into a box
    @http.route('/box/<model("stock.quant.package"):package>/edit', type='http', auth='user', website=True)
    def edit(self, package):
        return http.request.render('boxwise_wms.box_edit', {
            'package': package
        })

    # Box form submit
    @http.route('/box/submit', type='http', auth='user', website=True, methods=['POST'])
    def submit(self, **kw):
        # Parsing form input
        attribute_ids = [att[9:] for att in kw.keys() if 'Attribute' in att]
        attribute_value_ids = [kw['Attribute'+att] for att in attribute_ids]
        # find related product variant (product.product)
        search_string = [('product_tmpl_id', '=', int(kw['ProductTemplate']))]
        for att_val in attribute_value_ids:
            search_string.append(('attribute_value_ids', '=', int(att_val)))
        product = http.request.env['product.product'].search(search_string)
        # data to pass for stock.picking, stock.move, stock.move.line
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
        # Create a new receipt (stock.picking) with corresponding stock.move
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
        # write to stock.move and create linked stock.move.line
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
        # validate stock.picking
        stock_picking.button_validate()
        # redirect to infoscreen
        return werkzeug.utils.redirect('/box/%s' % slug(stock_picking.move_line_ids.result_package_id))

