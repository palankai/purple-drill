from __future__ import print_function

import argparse
import glob
import importlib
import logging
import os
import sys
import textwrap

from openerp.cli import Command
from openerp.tools import config
import openerp.release

import purpledrill
from .. import api

_logger = logging.getLogger(__name__)

class Screwdriver(Command):
    """Continous deployment tool"""
    epilog="""
    """

    def run(self, args):
        options = self.parse_args(args)
        path, tweaks = self.get_tweaks()
        init = {}
        update = {}
        if options.scratch:
            purpledrill.drop_database(options.database)
            init['screwdriver'] = 1
        else:
            update['screwdriver'] = 1

        # First round, gather data, mark modules
        with purpledrill.openerp_env(
            db_name=options.database,
            without_demo=options.without_demo,
            init=init,
            update=update
        ) as env:
            addons = config.misc['addons']
            modules = env['ir.module.module'].search([('name', 'in', addons.keys())])
            for m in modules:
                odoover = openerp.release.major_version
                expected_version = api.get_version(odoover, addons[m.name])
                # Field names are incorrect in the field definition of
                # it.module.module.
                installed_version = api.get_version(odoover, m.latest_version)
                available_version = api.get_version(
                    odoover, m.installed_version
                )
                action = api.get_action(
                    expected_version=expected_version,
                    available_version=available_version,
                    installed_version=installed_version,
                    state=m.state
                )
                if action:
                    m.state_update(action, [m.state])
                    _logger.info('Module %s marked %s', m.name, action)
            env.cr.commit()
            openerp.api.Environment.reset()
            openerp.modules.registry.RegistryManager.new(
                env.cr.dbname, update_module=True
            )

            _logger.info('Changes applied')

    def get_applied_tweaks(self, env, forced):
        Tweak = env["screwdriver.tweak"]
        return [
            tweak.name for tweak in Tweak.search([('name','not in', forced)])
        ]

    def get_parser(self):
        doc_paras = self.__doc__.split('\n\n')
        parser = argparse.ArgumentParser(
            description=doc_paras[0],
            epilog=textwrap.dedent(self.epilog),
            prog="odoo-server screwdriver",
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
        parser.add_argument(
            '-d', '--database', dest='database', default=config['db_name'],
            help="Build test database (default: %s)" % config['db_name']
        )
        parser.add_argument(
            '--scratch', dest='scratch', action='store_true',
            help="Recreate database before test"
        )
        parser.add_argument(
            '--without-demo', dest='without_demo',
            default='all',
            help="""disable loading demo data for modules to be installed
                (comma-separated, use "all" for all modules)
                By default loads demo data """
        )
        parser.add_argument(
            'forced', nargs="*",
            help="Force tweak to execute"
        )
        return parser

    def parse_args(self, args):
        parser = self.get_parser()
        options = parser.parse_args(args)
        return options

    def get_tweaks(self):
        path = self._get_tweaks_path()
        tweaks = []
        for filepath in glob.glob(os.path.join(path, "*.py")):
            fn = os.path.basename(filepath)
            if fn != "__init__.py":
                mod, _ = os.path.splitext(fn)
                tweaks.append(mod)
        return path, sorted(tweaks)

    def _get_tweaks_path(self):
        path = config.get("tweaks", None)
        if not path:
            print(
                "Setup 'tweaks' in config file, it should be"
                " the absoulte path of tweaks directory"
            )
            sys.exit(1)
        return path

    def apply(self, env, tweaks, exclude):
        todo = []
        for name in tweaks:
            if not name in exclude:
                todo.append(name)
        if not todo:
            _logger.info('Nothing to do')
        for name in todo:
            self.apply_tweak(env, name)

    def apply_tweak(self, env, name, store=True):
        mod = importlib.import_module(name)
        _logger.info('Apply: %s', name)
        mod.main()
        if store:
            self.store_applied(env, name)

    def store_applied(self, env, name):
        Tweak = env["screwdriver.tweak"]
        Tweak.create({"name": name})
