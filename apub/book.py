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


# todo the following states are recognized and localized by areader,
#      others are possible but will be displayed by areader as-is
states = ['ongoing', 'finished', 'on hiatus']


class Book:
    """The book.

    Attributes:
        chapters (list[Chapter]): The list of chapters.
    """
    def __init__(self):
        # todo document attributes class docstring
        # todo reference http://manual.calibre-ebook.com/cli/ebook-convert.html#metadata as source for metadata attribute documentation
        # attributes supported as metadata by ebook-convert:
        self.author_sort = ""
        self.authors = ""
        self.book_producer = ""
        self.comments = ""
        self.cover = ""  # todo handling ebook-convert vs json - bundle cover as
        #                      base64 encoded image into the json via
        #                      embed_cover option?
        self.isbn = ""  # todo ignore in json and html outputs
        self.language = ""
        self.pubdate = ""  # todo set to current date if not specified?
        #                    todo find out what ebook-convert defaults this to and implement it accordingly for areader
        #                    todo expects ISO 8601 YYYY-MM-DD
        self.publisher = ""
        self.rating = ""  # todo numeric between 1 and 5
        self.series = ""
        self.series_index = ""
        self.tags = ""
        self.title = ""

        # additional attributes supported by areader:
        # todo document attributes and allowed values in class docstring
        self.genres = ""  # todo use in JsonOutput
        self.state = ""  # todo use in JsonOutput

        # todo get rid of metadata
        self.metadata = {}
        self.chapters = []
        # self.outputs = []
        # self.substitutions = []
        # todo remove dependency on outputs and substitutions
        # todo input.py will return the project, the outputs and the
        #      substitutions as seperate entities / as a tuple
        # todo refactor this into input.py as factory methods
        # todo decision: metadata dict vs attributes

    @classmethod
    def from_dict(cls, dict_):
        """Creates a new Book object from the provided python dictionary.

        The structure and contents of the dictionary must be equivalent to
        the apub JSON format.

        Args:
            dict_ (dict): The dictionary to translate into a Project object.

        Returns:
            Book: A new Project created from the dictionary.
        """
        book = Book()

        # todo implement all attributes
        # todo basic validation of mandatory attributes
        book.title = dict_['title']
        book.series = dict_['series']
        book.series_index = dict_['series_index']
        book.authors = dict_['authors']
        book.author_sort = dict_['author_sort']
        book.publisher = dict_['publisher']
        book.language = dict_['language']
        book.tags = dict_['tags']

        book.chapters = Book._get_chapters_from_dict(dict_)

        return book

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

        self.title = title  # todo docs: This is what gets displayed in areader - it isn't used anywhere else
        self.source = source
        self.url_friendly_title = None  # todo docs This is used in areader (for the url) and html file names in html multi file mode
        #                                 todo HtmlOutput: additional attribute that determines wether the url_friendly_title is used as the file name
        #                                 todo HtmlOutput: decide on a file name scheme for multi file output in abscence of url friendly title
        #                                 todo HtmlOutput: additional attribute to optionally generate forward and back links in multi file mode
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
