#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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

    :param chapters: The list of chapters.
    :type chapters: list of Chapter

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

    def __init__(
            self,
            author_sort=None,
            authors=None,
            book_producer=None,
            comments=None,
            cover=None,
            isbn=None,
            language=None,
            pubdate=None,
            publisher=None,
            rating=None,
            series=None,
            series_index=None,
            tags=None,
            title=None,
            title_sort=None,
            chapters=None):
        self.__chapters = [] if not chapters else [].extend(chapters)

        # attributes supported as metadata by ebook-convert:
        self.author_sort = author_sort
        self.authors = authors
        self.book_producer = book_producer
        self.comments = comments
        self.cover = cover
        self.isbn = isbn
        self.language = 'und' if not language else language
        self.pubdate = date.today().isoformat() if not pubdate else pubdate
        self.publisher = publisher
        self.rating = rating
        self.series = series
        self.series_index = series_index
        self.tags = tags
        self.title = title
        self.title_sort = title_sort

    @property
    def chapters(self):
        """Gets the list of chapters.

        :returns: The list of chapters.
        :rtype: list of Chapter
        """
        return self.__chapters


class Chapter:
    """The chapter class is used to define all metadata required for a chapter
    of a book.
    
    :ivar publish: Determines wether the chapter will be included
        in the resulting output or not.
    :ivar source: The full path to the source file.
     
        Example: '.\my\file.md'.
    """

    def __init__(self, source=None, publish=True):
        # todo unit test kwargs
        self.publish = publish
        self.source = source
