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
from apub.fromdict import FromDict

states = ['ongoing', 'finished', 'on hiatus']


class Book(FromDict):
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
        self.isbn = ""  # todo ignore in json and html outputs - nah, keep it for when someone wants to look a book up
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

        # todo validate mandatory attributes in output classes according to
        #      the needs of the concrete output
        book.author_sort = cls.get_attribute_from_dict('author_sort', dict_)
        book.authors = cls.get_attribute_from_dict('authors', dict_)
        book.book_producer = cls.get_attribute_from_dict('book_producer', dict_)
        book.comments = cls.get_attribute_from_dict('comments', dict_)
        book.cover = cls.get_attribute_from_dict('cover', dict_)
        book.isbn = cls.get_attribute_from_dict('isbn', dict_)
        book.language = cls.get_attribute_from_dict('language', dict_)
        book.pubdate = cls.get_attribute_from_dict('pubdate', dict_)
        book.publisher = cls.get_attribute_from_dict('publisher', dict_)
        book.rating = cls.get_attribute_from_dict('rating', dict_)
        book.series = cls.get_attribute_from_dict('series', dict_)
        book.series_index = cls.get_attribute_from_dict('series_index', dict_)
        book.tags = cls.get_attribute_from_dict('tags', dict_)
        book.title = cls.get_attribute_from_dict('title', dict_)

        book.genres = cls.get_attribute_from_dict('genres', dict_)
        book.state = cls.get_attribute_from_dict('state', dict_)

        book.chapters = Book._get_chapters_from_dict(dict_)

        return book

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


class Chapter(FromDict):
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
        title = cls.get_attribute_from_dict('title', dict_)
        source = cls.get_attribute_from_dict('source', dict_)

        chapter = Chapter(title=title,
                          source=source)

        chapter.publish = cls.get_attribute_from_dict(
                'publish', dict_, default=True)
        chapter.url_friendly_title = cls.get_attribute_from_dict(
                'url_friendly_title', dict_)

        return chapter
