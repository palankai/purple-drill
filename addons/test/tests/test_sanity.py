import unittest
import logging

_logger = logging.getLogger(__name__)


#from purpledrill import odoo_test_env
from openerp.tests.common import TransactionCase


#class SanityTest(unittest.TestCase):

#    def test_sanity(self):
#        self.assertEqual(1, 1)

#    def test_odoo(self):
#        with odoo_test_env() as env:
#            self.assertEqual(env.user.id, 2)


class OdooTest(TransactionCase):

    def setUp(self):
        super(OdooTest, self).setUp()

    def test_odoo_sanity(self):
        _logger.info("logging from the test")
        self.assertEqual(self.env.user.id, 1)

    def test_odoo_sanity_installed(self):
        north = self.env['ir.module.module'].search([('name', '=', 'north')])
        self.assertEqual(north.state, 'installed')
