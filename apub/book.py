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


class Book:
    default_file_name = '.apub.json'

    def __init__(self):
        super().__init__()
        self.metadata = {}
        self.chapters = []
        # self.outputs = []
        # self.substitutions = []
        # todo remove dependency on outputs and substitutions
        # todo input.py will return the project, the outputs and the
        #      substitutions as seperate entities / as a tuple


    # todo refactor this into input.py as factory methods

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
        project = Book()

        project.metadata = Book._get_metadata_from_dict(dict_)
        project.chapters = Book._get_chapters_from_dict(dict_)

        return project

    @classmethod
    def _get_metadata_from_dict(cls, project_dict):
        """Returns the metadata dictionary contained in the project dictionary.

        Args:
            project_dict (dict): The project dictionary.

        Returns:
            dict: A dictionary containing the project metadata.
        """
        if 'metadata' in project_dict:
            return project_dict['metadata']

        return {}

    @classmethod
    def _get_chapters_from_dict(cls, project_dict):
        """Returns the chapters contained in the project dictionary as a list
        of Chapter objects.

        Args:
            project_dict (dict): The project dictionary.

        Returns:
            list[Chapter]: A list of Chapter objects or an empty list.
        """
        if 'chapters' in project_dict:
            chapters = []
            for chapter_dict in project_dict['chapters']:
                chapters.append(Chapter.from_dict(chapter_dict))
            return chapters

        return []


class Chapter:
    """Description for class.

    Args:
        title (str): The title
        source (str): File name of the source file

    Attributes:
        title (str): The title
        source (str): File name of the source file
        url_friendly_title(str): Url friendly representation of the title

            Mandatory if you use JsonOutput or HtmlOutput, optional for all
            other outputs.
        publish (bool): Determines wether the chapter will be included
            in the resulting output or not.

            Defaults to True
    """

    def __init__(self, title, source):

        if not title:
            raise AttributeError('title must not be None or empty')

        if not source:
            raise AttributeError('source must not be None or empty')

        self.title = title
        self.source = source
        self.url_friendly_title = None
        self.publish = True

    @classmethod
    def from_dict(cls, dict_):
        """Creates a new Chapter object from the provided python dictionary.

        The structure and contents of the dictionary must be equivalent to
        the apub JSON chapter format.

        Args:
            dict_ (dict): The dictionary to translate into a Chapter object.
        """
        chapter = Chapter(title=dict_['title'],
                          source=dict_['source'])

        if 'url_friendly_title' in dict_:
            chapter.url_friendly_title = dict_['url_friendly_title']

        if 'publish' in dict_ and dict_['publish'] is not None:
            chapter.publish = dict_['publish']

        return chapter
