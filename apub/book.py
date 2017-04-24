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
from datetime import date
from typing import List, Dict

from apub.errors import InvalidRatingError, InvalidSeriesIndexError, \
    NoBookFoundError
from apub.fromdict import FromDict

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class Book(FromDict):
    """The Book class is used to define the attributes and metadata
    required for creating a book via ebook-convert.

    It is one of the four integral parts of the project structure, the others
    being Project, Chapter, outputs and substitutions.

    See the users guide for more extensive documentation on how they fit
    together or the respective docs on info for the individual parts.

    More information on the attributes can be found here:
    http://manual.calibre-ebook.com/cli/ebook-convert.html#metadata
    """

    def __init__(self):
        self.__chapters = []

        # attributes supported as metadata by ebook-convert:
        self.__author_sort = None
        self.__authors = None
        self.__book_producer = None
        self.__comments = None
        self.__cover = None
        self.__isbn = None
        self.__language = 'und'
        self.__pubdate = date.today()
        self.__publisher = None
        self.__rating = None
        self.__series = None
        self.__series_index = None
        self.__tags = None
        self.__title = None
        self.__title_sort = None

    @property
    def chapters(self) -> List['Chapter']:
        """Gets the list of chapters.
        """
        return self.__chapters

    @property
    def author_sort(self) -> str:
        """Gets or sets the string to be used when sorting by author.
        """
        return self.__author_sort

    @author_sort.setter
    def author_sort(self, value: str):
        self.__author_sort = value

    @property
    def authors(self) -> str:
        """Gets or sets the authors. Multiple authors should be separated by 
        ampersands.
        """
        return self.__authors

    @authors.setter
    def authors(self, value: str):
        self.__authors = value

    @property
    def book_producer(self) -> str:
        """Gets or sets the book producer.
        """
        return self.__book_producer

    @book_producer.setter
    def book_producer(self, value: str):
        self.__book_producer = value

    @property
    def comments(self) -> str:
        """Gets or sets the ebook description.
        """
        return self.__comments

    @comments.setter
    def comments(self, value: str):
        self.__comments = value

    @property
    def cover(self) -> str:
        """Gets or sets the path or url to the cover image.
        """
        return self.__cover

    @cover.setter
    def cover(self, value: str):
        self.__cover = value

    @property
    def isbn(self) -> str:
        """Gets or sets the ISBN of the book.
        """
        return self.__isbn

    @isbn.setter
    def isbn(self, value: str):
        self.__isbn = value

    @property
    def language(self) -> str:
        """Gets or sets the language.

        Must be a ISO 639-2 code, defaults to 'und' if no language was given
        or the value is not a string or does not follow the ISO 639-2 format
        (string with 2 or 3 characters).

        See: https://en.wikipedia.org/wiki/List_of_ISO_639-2_codes
        """
        return self.__language

    @language.setter
    def language(self, value: str):
        # todo unit test language
        if not value:
            self.__language = 'und'
            return

        faulty_language_warning = \
            ("Book.language must be a string representing a "
             "ISO 639-2 language code, falling back to 'und'.")

        try:
            value = str(value)
        except ValueError:
            log.warning(faulty_language_warning)
            self.__language = 'und'
            return

        if len(value) not in [2, 3]:
            log.warning(faulty_language_warning +
                        " value was: {}".format(value))
            self.__language = 'und'
            return

        self.__language = value

    @property
    def pubdate(self) -> date:
        """Gets or sets the publication date.
        """
        return self.__pubdate

    @pubdate.setter
    def pubdate(self, value: date):
        self.__pubdate = value

    @property
    def publisher(self) -> str:
        """Gets or sets the ebook publisher.
        """
        return self.__publisher

    @publisher.setter
    def publisher(self, value: str):
        self.__publisher = value

    @property
    def rating(self) -> int:
        """Gets or sets the rating.
        
        :raises InvalidRatingError: The rating of a book must be an int or 
            None or castable to int with a value >= 1 or <= 5 .
        """
        return self.__rating

    @rating.setter
    def rating(self, value: int):
        # todo unit test rating
        if value is None:
            self.__rating = None

        try:
            value = int(value)
            if value < 1 or value > 5:
                raise ValueError
        except ValueError:
            raise InvalidRatingError(
                "The rating of a book must be an int or castable to int "
                "with a value >= 1 or <= 5 or None: '{}'".format(value))

        self.__rating = value

    @property
    def series(self) -> str:
        """Gets or sets the series this ebook belongs to.
        """
        return self.__series

    @series.setter
    def series(self, value: str):
        self.__series = value

    @property
    def series_index(self) -> int:
        """Gets or sets the series index.
        
        :raises InvalidSeriesIndexError: 
            The rating of a book must be an int or castable to int.
        """
        return self.__series_index

    @series_index.setter
    def series_index(self, value: int):
        # todo unit test series_index
        if value is None:
            self.__series_index = None
            return

        try:
            value = int(value)
        except ValueError:
            raise InvalidSeriesIndexError(
                'The rating of a book must be an int or castable to int.')

        self.__series_index = value

    @property
    def tags(self) -> str:
        """Gets or sets the tags for the book. Should be a comma 
        separated list.
        """
        return self.__tags

    @tags.setter
    def tags(self, value: str):
        self.__tags = value

    @property
    def title(self) -> str:
        """Gets or sets the title of the book.
        """
        return self.__title

    @title.setter
    def title(self, value: str):
        self.__title = value

    @property
    def title_sort(self) -> str:
        """Gets or sets the version of the title to be used for sorting.
        """
        return self.__title_sort

    @title_sort.setter
    def title_sort(self, value: str):
        self.__title_sort = value

    @classmethod
    def from_dict(cls, dict_: Dict) -> 'Book':
        """Creates a new Book object from the provided python dictionary.

        The structure and contents of the dictionary must be equivalent to
        the apub JSON format.

        :param dict_: 
            The dictionary to translate into a Project object.
        :type dict_: :obj:`Dict`

        :returns: A new Book created from the dictionary.
        """
        if 'book' not in dict_:
            raise NoBookFoundError

        book_dict = dict_['book']

        book = Book()

        get_value = cls.get_value_from_dict

        book.author_sort = get_value('author_sort', book_dict)
        book.authors = get_value('authors', book_dict)
        book.book_producer = get_value('book_producer', book_dict)
        book.comments = get_value('comments', book_dict)
        book.cover = get_value('cover', book_dict)
        book.isbn = get_value('isbn', book_dict)
        book.language = get_value('language', book_dict, 'und')
        book.pubdate = get_value(
            'pubdate', book_dict, default=date.today().isoformat())
        book.publisher = get_value('publisher', book_dict)
        book.rating = get_value('rating', book_dict)
        book.series = get_value('series', book_dict)
        book.series_index = get_value('series_index', book_dict)
        book.tags = get_value('tags', book_dict)
        book.title = get_value('title', book_dict)
        book.title_sort = get_value('title_sort', book_dict)

        book.chapters.extend(Book._get_chapters_from_dict(dict_))

        return book

    @classmethod
    def _get_chapters_from_dict(cls, project_dict: Dict) -> List['Chapter']:
        """Returns the chapters contained in the project dictionary as a list
        of Chapter objects.

        :param project_dict: The project dictionary.

        :returns: A list of Chapter objects or an empty list.
        """
        if 'chapters' in project_dict:
            chapters = []
            for chapter_dict in project_dict['chapters']:
                chapters.append(Chapter.from_dict(chapter_dict))
            return chapters

        return []


class Chapter(FromDict):
    """The chapter class is used to define all metadata required for a chapter
    of a book.
    """

    def __init__(self):
        self.__publish = True
        self.__slug = None
        self.__source = None

    @property
    def publish(self) -> bool:
        """Determines wether the chapter will be included
        in the resulting output or not.

        Defaults to True
        """
        return self.__publish

    @publish.setter
    def publish(self, value: bool):
        self.__publish = value

    @property
    def slug(self) -> str:
        """Gets or sets the url friendly representation of the title

        Mandatory if you use JsonOutput, optional for all other outputs.
        """
        return self.__slug

    @slug.setter
    def slug(self, value: str):
        self.__slug = value

    @property
    def source(self) -> str:
        """Gets or sets the file name of the source file
        """
        return self.__source

    @source.setter
    def source(self, value: str):
        self.__source = value

    @classmethod
    def from_dict(cls, dict_: Dict) -> 'Chapter':
        """Creates a new Chapter object from the provided python dictionary.

        The structure and contents of the dictionary must be equivalent to
        the apub JSON chapter format.

        :param dict_: The dictionary to translate into a Chapter object.

        :returns: A new Chapter created from the dictionary.
        """
        chapter = Chapter()

        get_value = cls.get_value_from_dict

        chapter.source = get_value('source', dict_)
        chapter.publish = get_value('publish', dict_, default=True)
        chapter.slug = get_value('slug', dict_)

        return chapter
