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

from apub.errors import NoBookFoundError, NoChaptersFoundError
from apub.fromdict import FromDict

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class Book(FromDict):
    """The Book is used to define the attributes and metadata
    required for creating a book via ebook-convert.

    It is one of the four integral parts of the project structure, the others
    being Project, Chapter, outputs and substitutions.

    See the users guide for more extensive documentation on how they fit
    together or the respective docs on info for the individual parts.

    More information on the attributes can be found here:
    http://manual.calibre-ebook.com/cli/ebook-convert.html#metadata
    
    :ivar author_sort: The string to be used when sorting by author.
    :ivar authors: The authors. Multiple authors should be separated by 
        ampersands.
    :ivar book_producer: The book producer.
    :ivar comments: The ebook description.
    :ivar cover: The path or url to the cover image.
    :ivar isbn: The ISBN of the book.
    :ivar language: The language. Should be an ISO 639-2 code, see:
        
        https://en.wikipedia.org/wiki/List_of_ISO_639-2_codes
    :ivar pubdate: The publication date.
    :ivar publisher: The ebook publisher.
    :ivar rating: The rating. Should be a number between 1 and 5.
    :ivar series: The series this ebook belongs to.
    :ivar series_index: The index of the book in this series.
    :ivar tags: The tags for the book. Should be a comma separated list.
    :ivar title: The title of the book.
    :ivar title_sort: The version of the title to be used for sorting.
    """

    def __init__(self):
        self.__chapters = []

        # attributes supported as metadata by ebook-convert:
        self.author_sort = None
        self.authors = None
        self.book_producer = None
        self.comments = None
        self.cover = None
        self.isbn = None
        self.language = 'und'
        self.pubdate = date.today().isoformat()
        self.publisher = None
        self.rating = None
        self.series = None
        self.series_index = None
        self.tags = None
        self.title = None
        self.title_sort = None

    @property
    def chapters(self):
        """Gets the list of chapters.
        """
        return self.__chapters

    @classmethod
    def from_dict(cls, dict_):
        """Creates a new Book object from the provided python dictionary.

        The structure and contents of the dictionary must be equivalent to
        the apub JSON format.

        :param dict_: 
            The dictionary to translate into a Book object.
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
        # todo unit test this, if awkward -> store date() instead, get string
        #      here and convert to date
        book.pubdate = get_value(
            'pubdate', book_dict, default=date.today().isoformat())
        book.publisher = get_value('publisher', book_dict)
        book.rating = get_value('rating', book_dict)
        book.series = get_value('series', book_dict)
        book.series_index = get_value('series_index', book_dict)
        book.tags = get_value('tags', book_dict)
        book.title = get_value('title', book_dict)
        book.title_sort = get_value('title_sort', book_dict)

        if 'chapters' in book_dict:
            for chapter_dict in book_dict['chapters']:
                book.chapters.append(Chapter.from_dict(chapter_dict))
        else:
            raise NoChaptersFoundError

        return book


class Chapter(FromDict):
    """The chapter class is used to define all metadata required for a chapter
    of a book.
    
    :ivar publish: Determines wether the chapter will be included
        in the resulting output or not.
    :ivar source: The full path to the source file.
     
        Example: '.\my\file.md'.
    """

    def __init__(self):
        self.publish = True
        self.source = None

    @classmethod
    def from_dict(cls, dict_):
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

        return chapter
