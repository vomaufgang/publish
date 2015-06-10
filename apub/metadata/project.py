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

from os import linesep

from ..errors import MalformedProjectJsonError
from .chapter import Chapter
from ..output import Output
from ..substitution import Substitution


class Project:
    default_file_name = '.apub.json'

    def __init__(self):
        super().__init__()
        self.metadata = {}
        self.chapters = []
        self.outputs = []
        self.substitutions = []

    @classmethod
    def from_directory(cls, path):
        import os

        full_path = os.path.join(path, Project.default_file_name)

        return Project.from_file(full_path)

    @classmethod
    def from_file(cls, path):
        """Creates a new Project object from a apub project file.

        The file at the provided path must be an apub project file and the
        contents must be a json object following the apub project structure.

        :param path: Path to the apub project file.
        :type path: str
        :returns: A new project created from the apub project file.
        """
        with open(path) as file:
            json = file.read()

        return Project.from_json(json)

    @classmethod
    def from_json(cls, json_):
        """Creates a new Project object from the provided JSON string.

        The JSON string must follow the apub project format.

        :param json_: The JSON string to translate into a Project object.
        :type json_: str
        :returns: A new Project created from the json string.
        :rtype: Project
        """
        import json

        try:
            dict_ = json.loads(json_)
        except ValueError as error:
            raise MalformedProjectJsonError(
                "The provided project json contained malformed data. "
                "Excpected a valid json object, got{0}'{1}'{0}"
                "Take a look at the enclosed ValueError for more information."
                .format(linesep, json_)) from error

        return Project.from_dict(dict_)

    @classmethod
    def from_dict(cls, dict_):
        """Creates a new Project object from the provided python dictionary.

        The structure and contents of the dictionary must be equivalent to
        the apub JSON project format.

        :param dict_: The dictionary to translate into a Project object.
        :type dict_: A standard python dictionary. The inner structure must
                     mirror the apub JSON project format.
        """
        project = Project()

        project.metadata = Project._get_metadata_from_dict(dict_)
        project.chapters = Project._get_chapters_from_dict(dict_)
        project.outputs = Project._get_outputs_from_dict(dict_)
        project.substitutions = Project._get_substitutions_from_dict(dict_)

        return project

    @classmethod
    def _get_metadata_from_dict(cls, project_dict):
        """Returns the metadata dictionary contained in the project dictionary.

        :param project_dict: The project dictionary.
          The inner structure of the dictionary must
          mirror the apub JSON project format.
        :type project_dict: dict
        :returns: A dictionary containing the project metadata.
        :rtype: dict of [str, str]
        """
        if 'metadata' in project_dict:
            return project_dict['metadata']

        return {}

    @classmethod
    def _get_chapters_from_dict(cls, project_dict):
        """Returns the chapters contained in the project dictionary as  a list
        of Chapter objects.

        :param project_dict: The project dictionary.
          The inner structure of the dictionary must
          mirror the apub JSON project format.
        :type project_dict: dict
        :returns: A list of Chapter objects or an empty list.
        :rtype: list of [Chapter]
        """
        if 'chapters' in project_dict:
            chapters = []
            for chapter_dict in project_dict['chapters']:
                chapters.append(Chapter.from_dict(chapter_dict))
            return chapters

        return []

    @classmethod
    def _get_outputs_from_dict(cls, project_dict):
        """Returns the outputs contained in the project dictionary as  a list
        of Output objects.

        :param project_dict: The project dictionary.
          The inner structure of the dictionary must
          mirror the apub JSON project format.
        :type project_dict: dict
        :returns: A list of Output objects or an empty list.
        :rtype: list of [Output]
        """
        if 'outputs' in project_dict:
            outputs = []
            for output_dict in project_dict['outputs']:
                outputs.append(Output.from_dict(output_dict))
            return outputs

        return []

    @classmethod
    def _get_substitutions_from_dict(cls, project_dict):
        """Returns the substitutions contained in the project dictionary as a
        list of Substitution objects.

        :param project_dict: The project dictionary.
          The inner structure of the dictionary must
          mirror the apub JSON project format.
        :type project_dict: dict
        :returns: A list of Substitution objects or an empty list.
        :rtype: list of [Substitution]
        """
        if 'substitutions' in project_dict:
            substitutions = []
            for substitution_dict in project_dict['substitutions']:
                substitutions.append(Substitution.from_dict(substitution_dict))
            return substitutions

        return []

