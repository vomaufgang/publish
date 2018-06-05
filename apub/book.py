#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# apub - Python package with cli to turn markdown files into ebooks
# Copyright (c) 2014 Christopher Knörndel
#
# Distributed under the MIT License
# (license terms are at http://opensource.org/licenses/MIT).

"""This module defines the book and chapter classes designed to hold the metadata of a book
and its chapters required by apub.output to produce its output.
"""


import logging
from datetime import date
from typing import List

LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())


class Book:
    """The Book is used to define the attributes and metadata
    required for creating a book via ebook-convert.

    It is one of the four integral parts of the project structure, the others
    being Project, Chapter, outputs and substitutions.

    See the users guide for more extensive documentation on how they fit
    together or the respective docs on info for the individual parts.

    More information on the attributes can be found here:
    http://manual.calibre-ebook.com/cli/ebook-convert.html#metadata

    Args:
        title: The title of the book.

    Keyword Args:
        author_sort (str): The string to be used when sorting by author.
        authors (str): The authors. Multiple authors should be separated by
            ampersands.
        book_producer (str): The book producer.
        comments (str): The ebook description.
        cover (str): The path or url to the cover image.
        isbn (str): The ISBN of the book.
        language (str): The language. Should be an ISO 639-1 code, see:

            https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
        pubdate (str): The publication date.
        publisher (str): The ebook publisher.
        rating (int): The rating. Should be a number between 1 and 5.
        series (str): The series this ebook belongs to.
        series_index (int): The index of the book in this series.
        tags (str): The tags for the book. Should be a comma separated list.
        title_sort (str): The version of the title to be used for sorting.

    Attributes:
        author_sort (str): The string to be used when sorting by author.
        authors (str): The authors. Multiple authors should be separated by
            ampersands.
        book_producer (str): The book producer.
        comments (str): The ebook description.
        cover (str): The path or url to the cover image.
        isbn (str): The ISBN of the book.
        language (str): The language. Should be an ISO 639-1 code, see:

            https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
        pubdate (str): The publication date.
        publisher (str): The ebook publisher.
        rating (int): The rating. Should be a number between 1 and 5.
        series (str): The series this ebook belongs to.
        series_index (int): The index of the book in this series.
        tags (str): The tags for the book. Should be a comma separated list.
        title (str): The title of the book.
        title_sort (str): The version of the title to be used for sorting.
    """

    # pylint: disable=too-few-public-methods,too-many-instance-attributes

    def __init__(
            self,
            title: str,
            **kwargs):
        """Initializes a new instance of the :class:`Book` class.
        """
        self.__chapters = []

        # required attributes
        self.title = title

        # auto generated attributes
        self.language = kwargs.pop('language', 'und')
        self.pubdate = kwargs.pop('pubdate', date.today().isoformat())

        # optional attributes
        self.author_sort = kwargs.pop('author_sort', None)
        self.authors = kwargs.pop('authors', None)
        self.book_producer = kwargs.pop('book_producer', None)
        self.comments = kwargs.pop('comments', None)
        self.cover = kwargs.pop('cover', None)
        self.isbn = kwargs.pop('isbn', None)
        self.publisher = kwargs.pop('publisher', None)
        self.rating = kwargs.pop('rating', None)
        self.series = kwargs.pop('series', None)
        self.series_index = kwargs.pop('series_index', None)
        self.tags = kwargs.pop('tags', None)
        self.title_sort = kwargs.pop('title_sort', None)

    @property
    def chapters(self) -> List['Chapter']:
        """Gets the list of chapters.

        Returns:
            The list of chapters.
        """
        return self.__chapters


class Chapter:
    """The chapter class is used to define all metadata required for a chapter
    of a book.

    Args:
        source_path: The path to the source file.
        publish: Determines whether the chapter will be included
            in the resulting output or not.

            Default: True

    Attributes:
        source_path (str): The path to the source file.
        publish (bool): Determines whether the chapter will be included
            in the resulting output or not.

            Default: True
    """

    # pylint: disable=too-few-public-methods

    def __init__(self,
                 source_path: str,
                 publish: bool = True):
        """Initializes a new instance of the :class:`Chapter` class.
        """
        self.source_path = source_path
        self.publish = publish
