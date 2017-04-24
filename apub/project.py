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
from typing import List, Dict

from apub.book import Book
from apub.errors import MalformedProjectJsonError
from apub.fromdict import FromDict
from apub.output import Output
from apub.substitution import Substitution

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class Project(FromDict):
    # todo document Project

    def __init__(self):
        self.book = None
        self.outputs = []
        self.substitutions = []

    # todo Ich sehe ja ein, dass from_dict Teil der Project-Klasse ist.
    #      Aber get_book_from_dict? Warum packe ich das nichts ins Buch-Modul
    #      usw?

    @classmethod
    def from_dict(cls, dict_: Dict) -> 'Project':
        """Creates a new Project object from a dictionary.

        The structure and contents of the dictionary must follow the apub 
        JSON project format.

        :param dict_: The dictionary to translate into a Project object.

        :returns: A new Project created from the dictionary.
        """
        # todo unit test Project.from_dict
        project = Project()

        project.book = Book.from_dict(dict_)
        project.outputs = cls._get_outputs_from_dict(dict_)
        project.substitutions = cls._get_substitutions_from_dict(dict_)

        return project

    @classmethod
    def _get_outputs_from_dict(cls, dict_: Dict):
        """Returns the outputs contained in the project dictionary.

        Args:
            dict_ (Dict): The project dictionary.

        Returns:
            A list of Output objects or an empty list.
        """
        # todo unit test Project._get_outputs_from_dict
        if 'outputs' in dict_:
            outputs = []
            for output_dict in dict_['outputs']:
                outputs.append(Output.from_dict(output_dict))
            return outputs

        return []

    @classmethod
    def _get_substitutions_from_dict(cls,
                                     dict_: Dict) -> List[Substitution]:
        """Returns the substitutions contained in the project dictionary as
        a list of Output objects.

        Args:
            dict_ (Dict): The project dictionary.

        Returns:
            List[Substitution]: A list of Substitution objects or an empty
                list.
        """
        # todo unit test Project._get_substitutions_from_dict
        if 'substitutions' in dict_:
            substitutions = []
            for substitution_dict in dict_['substitutions']:
                substitutions.append(Substitution.from_dict(substitution_dict))
            return substitutions

        return []


def read_project(path: str = None) -> Project:
    # todo document project.read_project
    # todo unit test read_project
    log.debug('start read_project')
    log.debug('path = {}'.format(path))

    project_file_path = _get_project_file_path(path)

    log.debug('reading {}'.format(project_file_path))
    with open(project_file_path) as project_file:
        data = project_file.read()
        log.debug("{0} read containing {1}".format(project_file_path, data))
    try:
        dict_ = json.loads(data)
    except ValueError as value_error:
        raise MalformedProjectJsonError(
            "The provided project json contained malformed data. "
            "Expected a valid json object, got\n'{}'\n"
            "Inspect the enclosed ValueError for more "
            "information.".format(data)) from value_error

    # todo: validate the data before calling the factory chain

    log.debug('end read_project')
    return Project.from_dict(dict_)


def _get_project_file_path(path: str) -> str:
    # todo document project._get_project_file_path
    # todo unit test _get_project_file_path
    default_project_file_name = '.apub.json'
    cwd = os.getcwd()

    if not path:
        log.debug(
            'path is None, look for {0} in cwd {1}'.format(
                default_project_file_name, cwd))
        return os.path.join(
            cwd,
            default_project_file_name)

    elif os.path.isdir(os.path.join(cwd, path)):
        log.debug(
            'path is {0}, look for {1}'.format(
                os.path.join(cwd, path),
                default_project_file_name))
        return os.path.join(
            path,
            default_project_file_name)

    elif os.path.isfile(os.path.join(cwd, path)):
        log.debug('file at {} exists, use it'.format(os.path.join(cwd, path)))
        return path
