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

from apub.output import Output
from apub.errors import OutputNotFoundError

import logging.config
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


def make(project, output=None):
    """

    Args:
        project (apub.project.Project): todo
        output (apub.output.Output): todo
    """

    if output is None:
        make_every_output(project)
        return

    outputs = project.outputs
    book = project.book
    substitutions = project.substitutions

    if isinstance(output, Output):
        output.make(
            book,
            substitutions)
        return

    try:
        output_name = output
        output = find_output(outputs, output_name)
        output.make(
            book,
            substitutions)
    except OutputNotFoundError:
        raise


def make_every_output(project):
    for output in project.outputs:
        output.make(
            project.book,
            project.substitutions)


def find_output(outputs, output_name):
    for output in outputs:
        if output.output_name == output_name:
            return output

    raise OutputNotFoundError("No output using the following name could "
                              "be found: '{0}'".format(output_name))
