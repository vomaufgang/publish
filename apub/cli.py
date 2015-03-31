#!/usr/bin/python
# -*- coding: utf-8 -*-

# taken from
# http://chase-seibert.github.io/blog/2014/03/21/python-multilevel-argparse.html

import argparse
import sys
from apub import make as make_

make_description = 'Make the configured outputs.'
make_usage = '''apub make [<output>]

Examples:
    apub make            Make all configured outputs.
    apub make my_output  Make the specified output.
'''


class CommandLineInterface():
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Pretends to be apub',
            usage='''apub <command> [<args>]''')
        parser.add_argument('command', help='Subcommand to run')

        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        getattr(self, args.command)()

    def make(self):
        parser = argparse.ArgumentParser(description=make_description,
                                         usage=make_usage)
        parser.add_argument('output')
        args = parser.parse_args(sys.argv[2:])
        make_(None, args.output)

    def push(self):
        pass

    def quickstart(self):
        pass


if __name__ == '__main__':
    CommandLineInterface()