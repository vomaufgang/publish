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

import logging.config
from datetime import date
from typing import List, Dict, Optional

from apub.errors import InvalidRatingError, InvalidSeriesIndexError
from apub.fromdict import FromDict

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class Book(FromDict):
    """The Book class isused to define the attributes and metadata
    required for creating a book via ebook-convert.

    It is one of the four integral parts of the project structure, the others
    being Project, Chapter, outputs and substitutions.

    See the users guide for more extensive documentation on how they fit
    together or the respective docs on info for the individual parts.

    More information on the attributes can be found here:
    http://manual.calibre-ebook.com/cli/ebook-convert.html#metadata

    Contains the chapters on top of the attributes required by ebook-convert.

    Examples:
        Create a new book object and use its attributes::

            book = Book()
            book.title = 'My book'
            book.language = 'en'
            book.rating = 3
            # ...

        Add chapters to a book::

            chapter = Chapter()
            chapter.title = 'My chapter'
            chapter.source = 'my_script.md'
            # ...
            book.chapters.append(chapter)

        Assign the book to a project::

            project = Project()
            project.book = book
            # ... add outputs and/or substitutions to the project
            make(project)

        See the users guide for more comprehensive examples and information
        on how to use the Book and where it fits in apub as a whole.

    Attributes:
        chapters (List[Chapter]): The list of chapters.

        author_sort (Optional[str]): String to be used when sorting by author.

        authors (Optional[str]): The authors. Multiple authors should be
            separated by ampersands.

        book_producer (Optional[str]): The book producer.

        comments (Optional[str]): The ebook description.

        cover (Optional[str]): Path or url to the cover image.

        isbn (Optional[str]): The ISBN of the book.

        language (Optional[str]): The language formatted as an
            ISO 639-2 code. Defaults to 'und'.

        pubdate (Optional[str]): The publication date formatted
            as 'YYYY-MM-DD' (see ISO 8601).

        publisher (Optional[str]): The ebook publisher.

        rating (Optional[int]): The rating.
            Should be an integer between 1 and 5.

        series (Optional[str]): The series this ebook belongs to.

        series_index (Optional[int])): The index of the book in the series.

        tags (Optional[str]): The tags for the book. Should be a comma
            separated list.

        title (Optional[str]): The title

        title_sort (Optional[str]): The version of the title to be used for
            sorting.


    """

    def __init__(self):
        self.__language = None
        self.__rating = None
        self.__series_index = None

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
        self.language = 'und'
        self.pubdate = date.today().isoformat()
        self.publisher = None
        self.rating = None
        self.series = None
        self.series_index = None
        self.tags = None
        self.title = None
        self.title_sort = None

        self.chapters = []

    @property
    def language(self) -> str:
        """Gets or sets the language.

        Must be a ISO 639-2 code, defaults to 'und'.

        See: https://en.wikipedia.org/wiki/List_of_ISO_639-2_codes
        """
        return self.language

    @language.setter
    def language(self, value: str):
        if not value:
            self.__language = 'und'

        faulty_language_warning = \
            ("Book.language must be a string representing a "
             "ISO 639-2 language code, falling back to 'und': "
             "'{}'").format(value)

        try:
            value = str(value)
        except ValueError:
            log.warning(faulty_language_warning)
            self.__language = 'und'
            return

        if len(value) not in [2, 3]:
            log.warning(faulty_language_warning)
            self.__language = 'und'
            return

        self.__language = value

    @property
    def rating(self) -> int:
        return self.__rating

    @rating.setter
    def rating(self, value: int):
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
    def series_index(self) -> int:
        # todo document Book.series_index
        return self.__series_index

    @series_index.setter
    def series_index(self, value: int):
        if value is None:
            self.__series_index = None

        try:
            value = int(value)
        except ValueError:
            raise InvalidSeriesIndexError(
                'The rating of a book must be an int or castable to int.')

        self.__series_index = value

    @classmethod
    def from_dict(cls, dict_) -> 'Book':
        """Creates a new Book object from the provided python dictionary.

        The structure and contents of the dictionary must be equivalent to
        the apub JSON format.

        Args:
            dict_ (Dict): The dictionary to translate into a Project object.

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
        book.language = get_value('language', dict_, 'und')
        book.pubdate = get_value(
            'pubdate', dict_, default=date.today().isoformat())
        book.publisher = get_value('publisher', dict_)
        book.rating = get_value('rating', dict_)
        book.series = get_value('series', dict_)
        book.series_index = get_value('series_index', dict_)
        book.tags = get_value('tags', dict_)
        book.title = get_value('title', dict_)
        book.title_sort = get_value('title_sort', dict_)

        book.chapters = Book._get_chapters_from_dict(dict_)

        return book

    @classmethod
    def _get_chapters_from_dict(cls, project_dict):
        """Returns the chapters contained in the project dictionary as a list
        of Chapter objects.

        Args:
            project_dict (dict): The project dictionary.

        Returns:
            A list of Chapter objects or an empty list.
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
        source (str): File name of the source file
        slug(str): Url friendly representation of the title

            Mandatory if you use JsonOutput or HtmlOutput, optional for all
            other outputs.
        publish (bool): Determines wether the chapter will be included
            in the resulting output or not.

            Defaults to True
    """

    def __init__(self):
        self.source = None
        self.slug = None
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
            dict_: The dictionary to translate into a Chapter object.

        Returns:
            A new Chapter created from the dictionary.
        """
        chapter = Chapter()

        get_value = cls.get_value_from_dict

        chapter.source = get_value('source', dict_)
        chapter.publish = get_value('publish', dict_, default=True)
        chapter.slug = get_value('slug', dict_)

        return chapter
