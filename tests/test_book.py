#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# apub - Python package with cli to turn markdown files into ebooks
# Copyright (c) 2014 Christopher Knörndel
#
# Distributed under the MIT License
# (license terms are at http://opensource.org/licenses/MIT).

"""Tests for `apub.book` module.
"""

# pylint: disable=missing-docstring,no-self-use,invalid-name

from datetime import date

import pytest
from apub.book import Book, Chapter
from tests import get_test_book


class TestBook:
    def test_constructor(self):
        book = get_test_book()
        book.rating = 36
        book.series_index = 42

        assert book.title == 'title'
        assert book.author_sort == 'author_sort'
        assert book.authors == 'authors'
        assert book.book_producer == 'book_producer'
        assert book.comments == 'comments'
        assert book.cover == 'cover'
        assert book.isbn == 'isbn'
        assert book.language == 'language'
        assert book.pubdate == 'pubdate'
        assert book.publisher == 'publisher'
        assert book.rating == 36
        assert book.series == 'series'
        assert book.series_index == 42
        assert book.tags == 'tags'
        assert book.title_sort == 'title_sort'

    def test_default_attribute_values(self):
        book = Book('title')

        assert book.author_sort is None
        assert book.authors is None
        assert book.book_producer is None
        assert book.comments is None
        assert book.cover is None
        assert book.isbn is None
        assert book.language == 'und'
        assert book.pubdate == date.today().isoformat()
        assert book.publisher is None
        assert book.rating is None
        assert book.series is None
        assert book.series_index is None
        assert book.tags is None
        assert book.title_sort is None

    def test_chapters_is_get_only(self):
        book = Book('title')
        with pytest.raises(AttributeError):
            # noinspection PyPropertyAccess
            book.chapters = []

    def test_chapters_is_iterable(self):
        book = Book('title')
        iter(book.chapters)

    def test_language(self):
        book = Book('title')
        book.language = 'de'

        assert book.language == 'de'

        book.language = 'eng'

        assert book.language == 'eng'

    def test_author_sort(self):
        book = Book('title')
        book.author_sort = "abc"

        assert book.author_sort == "abc"

    def test_authors(self):
        book = Book('title')
        book.authors = "abc"

        assert book.authors == "abc"

    def test_book_producer(self):
        book = Book('title')
        book.book_producer = "abc"

        assert book.book_producer == "abc"

    def test_comments(self):
        book = Book('title')
        book.comments = "abc"

        assert book.comments == "abc"

    def test_cover(self):
        book = Book('title')
        book.cover = "abc"

        assert book.cover == "abc"

    def test_isbn(self):
        book = Book('title')
        book.isbn = "abc"

        assert book.isbn == "abc"

    def test_publisher(self):
        book = Book('title')
        book.publisher = "abc"

        assert book.publisher == "abc"

    def test_series(self):
        book = Book('title')
        book.series = "abc"

        assert book.series == "abc"

    def test_tags(self):
        book = Book('title')
        book.tags = "abc"

        assert book.tags == "abc"

    def test_title(self):
        book = Book('title')
        book.title = "abc"

        assert book.title == "abc"

    def test_title_is_required(self):
        with pytest.raises(TypeError):
            # noinspection PyArgumentList
            Book()  # pylint: disable=no-value-for-parameter

    def test_title_sort(self):
        book = Book('title')
        book.title_sort = "abc"

        assert book.title_sort == "abc"


class TestChapter:
    def test_constructor(self):
        chapter = Chapter('source',
                          publish=False)

        assert chapter.source_path == 'source'
        assert chapter.publish is False

    def test_default_attribute_values(self):
        chapter = Chapter('source')

        assert chapter.publish is True

    def test_publish(self):
        chapter = Chapter('source')
        chapter.publish = False

        assert chapter.publish is False

    def test_source(self):
        chapter1 = Chapter('source')
        chapter1.source_path = "abc"

        chapter2 = Chapter('source')

        assert chapter1.source_path == "abc"
        assert chapter2.source_path == "source"

    def test_source_is_required(self):
        with pytest.raises(TypeError):
            # noinspection PyArgumentList
            Chapter()  # pylint: disable=no-value-for-parameter
