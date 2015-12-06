import purpledrill

def apply_tweaks():
    with purpledrill.openerp_env() as env:
        purpledrill.install_addon(env, 'north')
        env.cr.commit()
