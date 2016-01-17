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

import json
import logging
import os

from apub.errors import MalformedProjectJsonError
from apub.errors import NoBookFoundError
from apub.book import Book

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler)


class Project:
    def __init__(self):
        self.book = None
        self.outputs = None
        self.Substitutions = None

    # todo implement factory method from_json, splits the dict accordingly and
    #      calls book, output and substition factory methods

    @classmethod
    def from_dict(cls, dict_):
        """Creates a new Project object from the provided python dictionary.

        The structure and contents of the dictionary must be equivalent to
        the apub JSON project format.

        Args:
            dict_ (dict): The dictionary to translate into a Project object.

        Returns:
            Book: A new Project created from the dictionary.
        """
        project = Project()

        project.book = Project._get_book_from_dict(dict_)
        project.outputs = Project._get_outputs_from_dict(dict_)
        project.substitutions = Project._get_substitutions_from_dict(dict_)

        return project

    @classmethod
    def _get_book_from_dict(cls, project_dict):
        """Returns the metadata dictionary contained in the project dictionary.

        Args:
            project_dict (dict): The project dictionary.

        Returns:
            dict: A dictionary containing the project metadata.
        """
        # todo fix docstring metadata <-> book
        if 'book' in project_dict:
            return Book.from_dict(project_dict['book'])
        else:
            raise NoBookFoundError

    @classmethod
    def _get_outputs_from_dict(cls, project_dict):
        """Returns the outputs contained in the project dictionary as a list
        of Output objects.

        Args:
            project_dict (dict): The project dictionary.

        Returns:
            list[Output]: A list of Output objects or an empty list.
        """
        from apub.output import Output

        if 'outputs' in project_dict:
            outputs = []
            for output_dict in project_dict['outputs']:
                outputs.append(Output.from_dict(output_dict))
            return outputs

        return []

    @classmethod
    def _get_substitutions_from_dict(cls, project_dict):
        """Returns the substitutions contained in the project dictionary as
        a list of Output objects.

        Args:
            project_dict (dict): The project dictionary.

        Returns:
            list[Substitution]: A list of Substitution objects or an empty
                list.
        """
        from apub.substitution import Substitution

        if 'substitutions' in project_dict:
            substitutions = []
            for substitution_dict in project_dict['substitutions']:
                substitutions.append(Substitution.from_dict(substitution_dict))
            return substitutions

        return []


def read_project(path=None):
    """Welp

    Args:
        path (str): Optional

    Returns:
        Something.
    """
    log.debug('start read_project')
    log.debug('path = {0}'.format(path))
    project_file_path = None
    default_project_file_name = '.apub.json'

    if not path:
        log.debug('path is None, look for {0} in cwd {1}'.format(
                default_project_file_name,
                os.getcwd()))
        project_file_path = os.path.join(
                os.getcwd(),
                default_project_file_name)
    elif os.path.isdir(os.path.join(os.getcwd(), path)):
        log.debug('path is {0}, look for {1}'.format(
                os.path.join(os.getcwd(), path),
                default_project_file_name))
        project_file_path = os.path.join(
                path,
                default_project_file_name)
    elif os.path.isfile(os.path.join(os.getcwd(), path)):
        project_file_path = path
        log.debug('path is {0}, use it')

    log.debug('reading {0}'.format(project_file_path))
    with open(project_file_path) as project_file:
        data = project_file.read()
        log.debug('{0} read containing {1}'.format(project_file_path,
                                                   data))
    try:
        dict_ = json.loads(data)
    except ValueError as value_error:
        raise MalformedProjectJsonError(
                "The provided project json contained malformed data. "
                "Expected a valid json object, got{0}'{1}'{0}"
                "Inspect the enclosed ValueError for more information."
                .format(os.linesep, data)) from value_error

    # todo: validate the data before calling the factory chain

    log.debug('end read_project')
    return Project.from_dict(dict_)
