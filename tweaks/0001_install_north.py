import purpledrill

def main():
    with purpledrill.openerp_env() as e:
        purpledrill.install_addon(e, 'north')
    with purpledrill.openerp_env() as e:
        print(e['north.step'].search([]))
