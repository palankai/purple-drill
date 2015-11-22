import unittest


class SanityTest(unittest.TestCase):

    def test_sanity(self):
        self.assertEqual(1, 1)

    def test_odoo(self):
        self.fail('Not implemented yet')
        pass
