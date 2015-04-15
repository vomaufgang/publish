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


class CommandLineInterface():
    def __init__(self, args):

        # todo self.quickstart_ = quickstart_

        # todo implement the commands as callbacks instead of class methods
        parser = argparse.ArgumentParser(
            description='Pretends to be apub',
            usage='''apub <command> [<args>]''')
        parser.add_argument('command', help='Subcommand to run')

        command = parser.parse_args(args[1:2]).command
        if not hasattr(self, command):
            print('Unrecognized command')
            parser.print_help()
            return
        getattr(self, command)(args)

    def make(self, args):
        from .make import make
        from .input import read_project

        parser = argparse.ArgumentParser(description=make_description,
                                         usage=make_usage)

        parser.add_argument('--project_path', default=None)
        parser.add_argument('--output', default=None)
        args = parser.parse_args(args[2:])

        project = read_project(args.project_path)

        set_cwd(args.project_path)

        make(project=project, output=args.output)

    def quickstart(self, args):
        pass


def set_cwd(project_path=None):
    if not project_path:
        return
    else:
        os.chdir(project_path)

if __name__ == '__main__':
    CommandLineInterface(args=sys.argv)
