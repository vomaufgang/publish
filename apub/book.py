#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# apub - Python package with cli to turn markdown files into ebooks
# Copyright (c) 2014 Christopher Knörndel
#
# Distributed under the MIT License
# (license terms are at http://opensource.org/licenses/MIT).

import logging
from datetime import date
from typing import List, Optional

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class Book:
    """The Book is used to define the attributes and metadata
    required for creating a book via ebook-convert.

    It is one of the four integral parts of the project structure, the others
    being Project, Chapter, outputs and substitutions.

    See the users guide for more extensive documentation on how they fit
    together or the respective docs on info for the individual parts.

    More information on the attributes can be found here:
    http://manual.calibre-ebook.com/cli/ebook-convert.html#metadata

    :param title: The title of the book.
    :type title: str
    :param authors: The authors. Multiple authors should be separated by
        ampersands.
    :type authors: Optional[str]
    :param cover: The path or url to the cover image.
    :type cover: Optional[str]
    :param language: The language. Should be an ISO 639-1 code, see:

        https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
    :type language: Optional[str]
    :param publisher: The ebook publisher.
    :type publisher: Optional[str]
    :param series: The series this ebook belongs to.
    :type series: Optional[str]
    :param series_index: The series this ebook belongs to.
    :type series_index: Optional[str]

    :ivar author_sort: The string to be used when sorting by author.
    :ivar authors: The authors. Multiple authors should be separated by
        ampersands.
    :ivar book_producer: The book producer.
    :ivar comments: The ebook description.
    :ivar cover: The path or url to the cover image.
    :ivar isbn: The ISBN of the book.
    :ivar language: The language. Should be an ISO 639-1 code, see:

        https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
    :ivar pubdate: The publication date.
    :ivar publisher: The ebook publisher.
    :ivar rating: The rating. Should be a number between 1 and 5.
    :ivar series: The series this ebook belongs to.
    :ivar series_index: The index of the book in this series.
    :ivar tags: The tags for the book. Should be a comma separated list.
    :ivar title: The title of the book.
    :ivar title_sort: The version of the title to be used for sorting.

    :raises AttributeError: when the required parameter 'title' was omitted or
        empty.
    """

    def __init__(
            self,
            title: str,
            authors: Optional[str]=None,
            cover: Optional[str]=None,
            language: Optional[str]=None,
            publisher: Optional[str]=None,
            series: Optional[str]=None,
            series_index: Optional[int]=None):
        """

        Returns:
            :
        """
        if not title:
            raise AttributeError("'title' cannot be empty")
            # todo test for 'title' cannot be empty AttributeError

        self.__chapters = []
        # todo test if param chapters is not iterable, .extend throws TypeError

        # attributes supported as metadata by ebook-convert:
        self.author_sort: str = None
        self.authors: str = authors
        self.book_producer: str = None
        self.comments: str = None
        self.cover: str = cover
        self.isbn: str = None
        self.language: str = 'und' if not language else language
        self.pubdate: str = date.today().isoformat()
        self.publisher: str = publisher
        self.rating: int = None
        self.series: str = series
        self.series_index: int = series_index
        self.tags: str = None
        self.title: str = title
        self.title_sort: str = None

    @property
    def chapters(self) -> List['Chapter']:
        """Gets the list of chapters.

        :returns: The list of chapters.
        """
        return self.__chapters


class Chapter:
    """The chapter class is used to define all metadata required for a chapter
    of a book.

    :param source: The full path to the source file. Example: '\.\\my\\file.md\'.
    :type source: str
    :param publish: Determines whether the chapter will be included
        in the resulting output or not.

        Default: True
    :type publish: Optional[bool]

    :ivar source: The full path to the source file. Example: '\.\\my\\file.md\'.
    :ivar publish: Determines whether the chapter will be included
        in the resulting output or not.

        Default: True
    """

    def __init__(self, source: str, publish: Optional[bool]=True):
        if not source:
            raise AttributeError("'source' cannot be empty")
            # todo test for 'source' cannot be empty AttributeError

        # todo unit test kwargs
        self.publish: Optional[bool] = publish
        self.source: str = source
