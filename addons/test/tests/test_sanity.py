import unittest


from purpledrill import odoo_test_env
import openerp


class SanityTest(unittest.TestCase):

    def test_sanity(self):
        self.assertEqual(1, 1)

    def test_odoo(self):
        with odoo_test_env() as env:
            self.assertEqual(env.user.id, 2)
