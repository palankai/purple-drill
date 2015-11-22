from __future__ import print_function

import argparse

from openerp.cli import Command
from openerp.tools import config


class North(Command):
    """Continous deployment tool"""

    def run(self, args):
        parser = self.get_parser()
        options = parser.parse_args(args)

        print(options)

    def get_parser(self):
        parser = argparse.ArgumentParser(
            description=self.__doc__,
            prog="odoo-server north"
        )
        parser.add_argument(
            '-d', dest="database", default=config["db_name"],
            help="database name (default=%s)" % config["db_name"]
        )
        return parser
