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

import logging

from .output import Output
from .errors import OutputNotFoundError

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler)


def make(project, output=None):
    """

    :param output:
    :type project: :class:`apub.metadata.Book`
    """
    if output is None:
        make_every_output(project)
        return

    if isinstance(output, Output):
        output.make(
            project.metadata,
            project.chapters,
            project.substitutions)
        return

    try:
        output = find_output(project, output)
        output.make(
            project.metadata,
            project.chapters,
            project.substitutions)
    except OutputNotFoundError:
        raise


def make_every_output(project):
    for output in project.outputs:
        output.make(
            project.book,
            project.substitutions)


def find_output(project, output_name):
    for output in project.outputs:
        if output.output_name == output_name:
            return output
    raise OutputNotFoundError("No output using the following name could "
                              "be found: '{0}'".format(output_name))
