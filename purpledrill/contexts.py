import contextlib

import openerp


@contextlib.contextmanager
def odoo_env():
    openerp.tools.config.parse_config([])
    openerp.cli.server.report_configuration()
    openerp.service.server.start(preload=[], stop=True)
    with openerp.api.Environment.manage():
        registry = openerp.modules.registry.RegistryManager.get(
            openerp.tools.config["db_name"]
        )
        with registry.cursor() as cr:
            uid = openerp.SUPERUSER_ID
            ctx = openerp.api.Environment(cr, uid, {})['res.users'].context_get()
            yield openerp.api.Environment(cr, uid, ctx)


def get_odoo_env():
    registry = openerp.modules.registry.RegistryManager.get(
        openerp.tools.config["db_name"]
    )
    openerp.api.Environment.reset()
    cr = registry.cursor()
    uid = openerp.SUPERUSER_ID
    ctx = openerp.api.Environment(cr, uid, {})['res.users'].context_get()
    return openerp.api.Environment(cr, uid, ctx)

