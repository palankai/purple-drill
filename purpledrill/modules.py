

def install_addon(env, addon):
    module = env["ir.module.module"].search([("name", "=", addon)])
    module.button_immediate_install()


def upgrade_addon(env, addon):
    module = env["ir.module.module"].search([("name", "=", addon)])
    module.button_immediate_upgrade()


def uninstall_addon(env, addon):
    module = env["ir.module.module"].search([("name", "=", addon)])
    module.button_immediate_uninstall()
