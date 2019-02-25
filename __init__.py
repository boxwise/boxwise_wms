# -*- coding: utf-8 -*-

from . import controllers
from . import wizards
from . import sequences

from odoo import api, SUPERUSER_ID, fields, models

import wdb
import logging

_logger = logging.getLogger(__name__)

def post_init_hook(cr, registry):
    # this will only run once, when the module is
    # first installed
    # will need to use migrations for subsequent runs
    _logger.info("post_init_hook for boxwise_wms")

    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        run_on_first_install(env)

        
class boxwise_config(models.AbstractModel):
    # hack to call this on every time our module loads (upgrade or not)
    @api.model
    def xml_init(self):
        _logger.info("boxwise_config_xml_init for boxwise_wms")
        run_on_every_install_or_upgrade(self.env)

def run_on_first_install(env):
    _logger.info("Running boxwise_wms steps: first install")
    return

def run_on_every_install_or_upgrade(env):
    # really we should be using the migration features, that
    # are applied for each version (see 'Addon updates and data migration' in Odoo cookbook)
    # but this seems simpler for now
    _logger.info("Running boxwise_wms steps: every install or upgrade")
    #wdb.set_trace()
    # these are created when we install the stock module
    _delete_if_exists(env, "product", "product_category_1")
    # these are created when we install the website module
    # it does however mean we can't ever create something called this...
    _delete_if_exists(env, "website", "homepage_page")
    _delete_if_exists(env, "website", "contactus_page")
    _delete_if_exists(env, "website", "aboutus_page")
    _delete_if_exists(env, "website", "menu_homepage")
    _delete_if_exists(env, "website", "menu_contactus")

    _logger.info("Setting stock sequence to random_id")
    seq = env.ref("stock.seq_quant_package")
    if not seq.implementation == 'random_id':
        seq.write({'implementation': 'random_id'})

def _delete_if_exists(env, module_name, xml_id):
    target_name = module_name + '.' + xml_id
    item_to_delete = env.ref(module_name + '.' + xml_id, raise_if_not_found=False)
    if (item_to_delete):
        _logger.info("Deleting %s" % target_name)
        item_to_delete.unlink()
    else:
        _logger.info("Skipping deletion of %s as it is not present" % target_name)