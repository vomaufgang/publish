#!/usr/bin/env python3
# coding: utf8
#
# apub - Python package with cli to turn markdown files into ebooks
# Copyright (C) 2015  Christopher Knörndel
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# taken from
# http://chase-seibert.github.io/blog/2014/03/21/python-multilevel-argparse.html

import os
import sys
import argparse
import json

import logging
import logging.config
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

make_description = 'Make the configured outputs.'
make_usage = '''apub make [--project-path] [--output=<output_name>]

Important:
    apub defaults to the current directory as the
    current working directory. If your project
    resides in a different directory than the one
    you are calling the command line interface from,
    use the --project-path parameter.

Examples:
    apub make                      Make all configured outputs.
    apub make --output=my_output   Make the specified output.
'''


class _CommandLineInterface:
    def __init__(self, args=None):
        log.debug('starting command line interface')

        if args is None:
            args = sys.argv

        parser = argparse.ArgumentParser(
            description='Pretends to be apub',
            usage='''apub <command> [<args>]''')
        parser.add_argument('command', help='Subcommand to run')

        command = parser.parse_args(args[1:2]).command
        if not hasattr(self, command) or command == '__init__':
            print('Unrecognized command')
            parser.print_help()
            return
        getattr(self, command)(args)

    def make(self, args):
        """Welp.

        Args:
            args:
        """
        from .make import make
        from .input import read_project

        parser = argparse.ArgumentParser(description=make_description,
                                         usage=make_usage)

        parser.add_argument('--project_path', default=None)
        parser.add_argument('--output', default=None)
        _add_log_level_argument(parser)

        args = parser.parse_args(args[2:])

        _setup_logging(args.log_level)

        project = read_project(args.project_path)

        previous_cwd = os.getcwd()
        _set_cwd(args.project_path)
        try:
            make(project=project, output=args.output)
        finally:
            _set_cwd(previous_cwd)

    def quickstart(self, args):
        """Welp.

        Args:
            args: list
        """
        from .quickstart import quickstart
        from .input import read_project

        if read_project(None):
            # todo a project of this name already exists
            raise NotImplementedError

        quickstart()


def _set_cwd(project_path=None):
    """Sets the current working directory if the provided project_path is
    not none.

    :param project_path:
    """
    if not project_path:
        return
    else:
        os.chdir(project_path)


def _add_log_level_argument(argument_parser):
    """Adds the log_level argument to an ArgumentParser instance.

    :param argument_parser:
    """
    argument_parser.add_argument('--log_level',
                                 type=str,
                                 default='INFO',
                                 choices=['DEBUG',
                                          'INFO',
                                          'WARNING',
                                          'ERROR',
                                          'CRITICAL'])


def _setup_logging(log_level=logging.INFO):
    """Sets up the python logging block using logging.basiConfig and the
    provided log_level.

    Can be overridden by a more finely tuned logging output to various logging
    channels by placing a standard python logging.ini inside the cwd. Please
    take a look at the chapter [Overriding the default logging configuration]
    on how to achieve this.

    :param log_level:
    :return:
    """
    # todo Link to the chapter in the documentation.
    logging_config = 'logging.json'
    if os.path.isfile(logging_config):
        if os.path.exists(logging_config):
            with open(logging_config, 'rt') as f:
                config = json.load(f)
            logging.config.dictConfig(config)
        logging.getLogger().setLevel()
    else:
        logging.basicConfig(level=log_level)


def main(args=None):
    _CommandLineInterface(args)


if __name__ == '__main__':
    main()
