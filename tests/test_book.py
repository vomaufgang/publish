#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# apub - Python package with cli to turn markdown files into ebooks
# Copyright (c) 2014 Christopher Knörndel
#
# Distributed under the MIT License
# (license terms are at http://opensource.org/licenses/MIT).

"""
test_chapter
----------------------------------

Tests for `apub.book` module.
"""

import pytest
from apub.book import Book, Chapter


class TestBook:
    def test_chapters_is_get_only(self):
        book = Book('title')
        with pytest.raises(AttributeError):
            # noinspection PyPropertyAccess
            book.chapters = []

    def test_chapters_is_iterable(self):
        book: Book = Book('title')
        iter(book.chapters)

    # todo for all properties: test default values (None, pubdate etc.)

    # todo language

    # todo rating

    # todo series index

    # todo pubdate (mock date.today() to procude fix date, in case of unit
    #      test running between days :-))

    # todo from_dict (actual dict, dict with invalid values,
    #                 empty dict leads to default values)

    def test_language(self):
        book = Book('title')
        book.language = 'de'

        assert 'de' == book.language

        book.language = 'eng'

        assert 'eng' == book.language

    def test_language_defaults_to_und(self):
        book: Book = Book('title')

        assert 'und' == book.language

    def test_author_sort(self):
        book = Book('title')
        book.author_sort = "abc"

        assert "abc" == book.author_sort

    def test_author_sort_defaults_to_none(self):
        book: Book = Book('title')

        assert book.author_sort is None

    def test_authors(self):
        book = Book('title')
        book.authors = "abc"

        assert "abc" == book.authors

    def test_authors_defaults_to_none(self):
        book: Book = Book('title')

        assert book.authors is None

    def test_book_producer(self):
        book = Book('title')
        book.book_producer = "abc"

        assert "abc" == book.book_producer

    def test_book_producer_defaults_to_none(self):
        book: Book = Book('title')

        assert book.book_producer is None

    def test_comments(self):
        book = Book('title')
        book.comments = "abc"

        assert "abc" == book.comments

    def test_comments_defaults_to_none(self):
        book: Book = Book('title')

        assert book.comments is None

    def test_cover(self):
        book = Book('title')
        book.cover = "abc"

        assert "abc" == book.cover

    def test_cover_defaults_to_none(self):
        book: Book = Book('title')

        assert book.cover is None

    def test_isbn(self):
        book = Book('title')
        book.isbn = "abc"

        assert "abc" == book.isbn

    def test_isbn_defaults_to_none(self):
        book: Book = Book('title')

        assert book.isbn is None

    def test_publisher(self):
        book = Book('title')
        book.publisher = "abc"

        assert "abc" == book.publisher

    def test_publisher_defaults_to_none(self):
        book: Book = Book('title')

        assert book.publisher is None

    def test_series(self):
        book = Book('title')
        book.series = "abc"

        assert "abc" == book.series

    def test_series_defaults_to_none(self):
        book: Book = Book('title')

        assert book.series is None

    def test_tags(self):
        book = Book('title')
        book.tags = "abc"

        assert "abc" == book.tags

    def test_tags_defaults_to_none(self):
        book: Book = Book('title')

        assert book.tags is None

    def test_title(self):
        book = Book('title')
        book.title = "abc"

        assert "abc" == book.title

    def test_title_cannot_be_empty(self):
        with pytest.raises(AttributeError) as exception_info:
            Book('')

        assert "'title' cannot be empty" in str(exception_info.value)

    def test_title_is_required(self):
        with pytest.raises(TypeError):
            # noinspection PyArgumentList
            Book()

    def test_title_sort(self):
        book = Book('title')
        book.title_sort = "abc"

        assert "abc" == book.title_sort

    def test_title_sort_defaults_to_none(self):
        book: Book = Book('title')

        assert book.title_sort is None


class TestChapter:
    def test_publish(self):
        chapter = Chapter('source')
        chapter.publish = False

        assert chapter.publish is False

    def test_publish_defaults_to_true(self):
        chapter = Chapter('source')

        assert chapter.publish is True

    def test_source(self):
        chapter1 = Chapter('source')
        chapter1.source = "abc"

        chapter2 = Chapter('source')

        assert "abc" == chapter1.source
        assert "source" == chapter2.source

    def test_source_cannot_be_empty(self):
        with pytest.raises(AttributeError) as exception_info:
            Chapter('')

        assert "'source' cannot be empty" in str(exception_info.value)

    def test_source_is_required(self):
        with pytest.raises(TypeError):
            # noinspection PyArgumentList
            Chapter()
