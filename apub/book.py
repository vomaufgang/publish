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

from datetime import date

from typing import Optional, List

from apub.errors import InvalidRatingError, InvalidSeriesIndexError
from apub.fromdict import FromDict

import logging.config
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class Book(FromDict):
    """The book.

    More information on the attributes can be found here:
    http://manual.calibre-ebook.com/cli/ebook-convert.html#metadata

    Attributes:
        chapters (List[Chapter]): The list of chapters.
        title (Optional[str]): The title.
    """

    def __init__(self):
        # todo use None as default for non-mandatory fields
        # todo document attributes class docstring
        # attributes supported as metadata by ebook-convert:
        self.author_sort = None
        self.authors = None
        self.book_producer = None
        self.comments = None
        self.cover = None
        # todo handling ebook-convert vs json - bundle cover as
        #      base64 encoded image into the json via
        #      embed_cover option?
        self.isbn = None
        # todo ignore in json and html outputs - nah, keep it for
        #      when someone wants to look a book up
        self.language = None
        self.pubdate = date.today().isoformat()
        self.publisher = None
        self.series = None
        self.tags = None
        self.title = None

        self.__rating = None
        self.__series_index = None

        self.chapters = []

    @property
    def rating(self):
        return self.__rating

    @rating.setter
    def rating(self, value):
        if value is None:
            self.__rating = None

        try:
            value = int(value)
            if value < 1 or value > 5:
                raise ValueError
        except ValueError:
            raise InvalidRatingError(
                'The rating of a book must be an int or castable to int '
                'with a value >= 1 or <= 5 or None: \'{}\''.format(value))

        self.__rating = value

    @property
    def series_index(self):
        # todo document Book.series_index
        return self.__series_index

    @series_index.setter
    def series_index(self, value):
        if value is None:
            self.__series_index = None

        try:
            value = int(value)
        except ValueError:
            raise InvalidSeriesIndexError(
                'The rating of a book must be an int or castable to int.')

        self.__series_index = value

    @classmethod
    def from_dict(cls, dict_):
        """Creates a new Book object from the provided python dictionary.

        The structure and contents of the dictionary must be equivalent to
        the apub JSON format.

        Args:
            dict_ (dict): The dictionary to translate into a Project object.

        Returns:
            Book: A new Book created from the dictionary.
        """
        book = Book()

        get_value = cls.get_value_from_dict

        book.author_sort = get_value('author_sort', dict_)
        book.authors = get_value('authors', dict_)
        book.book_producer = get_value('book_producer', dict_)
        book.comments = get_value('comments', dict_)
        book.cover = get_value('cover', dict_)
        book.isbn = get_value('isbn', dict_)
        book.language = get_value('language', dict_)
        book.pubdate = get_value(
            'pubdate', dict_, default=date.today().isoformat())
        book.publisher = get_value('publisher', dict_)
        book.rating = get_value('rating', dict_)
        book.series = get_value('series', dict_)
        book.series_index = get_value('series_index', dict_)
        book.tags = get_value('tags', dict_)
        book.title = get_value('title', dict_)

        book.genres = get_value('genres', dict_)
        book.state = get_value('state', dict_)
        book.url_friendly_title = get_value('url_friendly_title', dict_)

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

    def __init__(self):
        self.title = None
        # todo docs: This is what gets displayed in areader - it isn't used
        #      anywhere else
        self.source = None
        self.url_friendly_title = None
        # todo docs This is used in areader (for the url) and html file
        #      names in html multi file mode
        # todo HtmlOutput: additional attribute that determines wether the
        #      url_friendly_title is used as the file name
        # todo HtmlOutput: decide on a file name scheme for multi file
        #      output in abscence of url friendly title
        # todo HtmlOutput: additional attribute to optionally generate
        #      forward and back links in multi file mode
        self.publish = True

    @classmethod
    def from_dict(cls, dict_):
        """Creates a new Chapter object from the provided python dictionary.

        The structure and contents of the dictionary must be equivalent to
        the apub JSON chapter format.

        Args:
            dict_ (dict): The dictionary to translate into a Chapter object.

        Returns:
            Chapter: A new Chapter created from the dictionary.
        """
        chapter = Chapter()

        get_value = cls.get_value_from_dict

        chapter.title = get_value('title', dict_)
        chapter.source = get_value('source', dict_)
        chapter.publish = get_value('publish', dict_, default=True)
        chapter.url_friendly_title = get_value('url_friendly_title', dict_)

        return chapter
