from __future__ import print_function

import argparse
import textwrap
import unittest
import sys

from openerp.cli import Command
from openerp.tools import config


class Test(Command):
    """Unittest
       Python unittest with Odoo context

       Examples:
           %(prog)s test_module               - run tests from test_module
           %(prog)s module.TestClass          - run tests from module.TestClass
           %(prog)s module.Class.test_method  - run specified test method

       Test module schema:
           [openerp.addons.]<specific addon>.tests.<specific test module>
    """

    def run(self, args):
        parser = self.get_parser()
        options = parser.parse_args(args)
        suite = unittest.TestSuite()
        loader = unittest.TestLoader()
        if options.tests:
            suite.addTests(loader.loadTestsFromNames(
                [self.ensure_addon_prefix(n) for n in options.tests]
            ))
            if suite.countTestCases() == 0:
                print("There is no tests as specified")
                sys.exit(1)
        if options.addons:
            for addon in options.addons.split(','):
                suite.addTests(loader.discover(
                    start_dir='/mnt/extra-addons/' + addon
                ))
            if suite.countTestCases() == 0:
                print("There is no tests as specified")
                sys.exit(1)
        if suite.countTestCases() == 0:
            suite.addTests(loader.discover(start_dir='/mnt/extra-addons/'))
        runner = unittest.TextTestRunner(
            verbosity=2
        )
        runner.run(suite)

    def ensure_addon_prefix(self, addon_name):
        if not addon_name.startswith('openerp.addons.'):
            return 'openerp.addons.' + addon_name
        return addon_name



    def get_parser(self):
        doc_paras = self.__doc__.split('\n\n')
        parser = argparse.ArgumentParser(
            description=doc_paras[0],
            epilog=textwrap.dedent('\n\n'.join(doc_paras[1:])),
            prog="odoo-server test",
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
        parser.add_argument(
            '-d', dest="database", default=config["db_name"],
            help="database name (default=%s)" % config["db_name"]
        )
        parser.add_argument(
            'tests', nargs="*",
            help="can be a list of any number of test modules, classes and test \
            methods."
        )
        parser.add_argument(
            '--addons',
            help="Test a complete addon"
        )
        return parser
