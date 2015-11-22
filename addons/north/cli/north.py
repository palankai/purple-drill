from __future__ import print_function

import argparse

from openerp.cli import Command
from openerp.tools import config


class North(Command):
    """Continous deployment tool"""

    def run(self, args):
        parser = self.get_parser()
        options = parser.parse_args()

        print(options)

    def get_parser(self):
        parser = argparse.ArgumentParser(
            description=self.__doc__
        )
        parser.add_argument(
            '-d', dest="database", default=config["db_name"], required=True,
            help="database name (default=%s)" % config["db_name"]
        )
        return parser
