#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# anited. publish - Python package with cli to turn markdown files into ebooks
# Copyright (c) 2014 Christopher Knörndel
#
# Distributed under the MIT License
# (license terms are at http://opensource.org/licenses/MIT).

"""CLI entry point for the publish command and the yaml project format.
"""

import logging

from publish.yaml import load_project

LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())


def main():
    """Main CLI entry point for anited. publish.

    Looks for a file .publish.yml in the current working directory, calls load_yaml on
    its content and then runs each output defined in the project file.
    """
    logging.basicConfig(format='%(message)s', level=logging.INFO)

    with open('.publish.yml') as publish_yaml:
        yaml = publish_yaml.read()

    book, substitutions, outputs = load_project(str(yaml))

    for output in outputs:
        output.make(book, substitutions)


if __name__ == '__main__':
    main()
