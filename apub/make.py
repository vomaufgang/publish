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
from typing import List

from apub.errors import OutputNotFoundError
from apub.output import Output
from apub.project import Project

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


def make(project, output=None):
    """

    Args:
        project (Project):
        output (apub.output.Output or str):

    Raises:
        TypeError:
        OutputNotFoundError:

    """
    # todo document make.make
    if output is None:
        make_every_output(project)
        return

    book = project.book
    substitutions = project.substitutions

    if isinstance(output, Output):
        output.make(
            book,
            substitutions)
        return

    try:
        make_output_by_name(project, str(output))
    except OutputNotFoundError:
        raise


def make_output_by_name(project, output_name):
    """

    Args:
        project (Project):
        output_name (str):

    Raises:
        OutputNotFoundError
    """
    # todo document make.make_output_by_name
    outputs = project.outputs
    book = project.book
    substitutions = project.substitutions

    try:
        output = find_output_by_name(outputs, output_name)
        output.make(
            book,
            substitutions)
    except OutputNotFoundError:
        raise


def make_every_output(project):
    # todo document make.make_every_output
    """

    Args:
        project (Project):
    """
    for output in project.outputs:
        output.make(
            project.book,
            project.substitutions)


def find_output_by_name(outputs, output_name):
    """

    Args:
        outputs (list of apub.output.Output):
        output_name (str):

    Returns:
        apub.output.Output: 
    Raises:
        NameError:
        OutputNotFoundError:

    """
    # todo document make.find_output
    for output in outputs:
        if output.name == output_name:
            return output

    raise OutputNotFoundError("No output using the following name could "
                              f"be found: '{output_name}'")
