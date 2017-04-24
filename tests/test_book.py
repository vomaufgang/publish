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

"""
test_chapter
----------------------------------

Tests for `apub.book` module.
"""

import unittest

from apub.book import Book, Chapter


class TestBook(unittest.TestCase):
    def test_chapters_is_get_only(self):
        book = Book()
        with self.assertRaises(AttributeError):
            book.chapters = []

    def test_chapters_is_iterable(self):
        book = Book()
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
        book = Book()
        book.language = 'de'

        self.assertEqual('de', book.language)

        book.language = 'eng'

        self.assertEqual('eng', book.language)

    def test_language_defaults_to_und(self):
        book = Book()

        self.assertEqual('und', book.language)

    def test_author_sort(self):
        book = Book()
        book.author_sort = "abc"

        self.assertEqual("abc", book.author_sort)

    def test_author_sort_defaults_to_none(self):
        book = Book()

        self.assertEqual(None, book.author_sort)

    def test_authors(self):
        book = Book()
        book.authors = "abc"

        self.assertEqual("abc", book.authors)

    def test_authors_defaults_to_none(self):
        book = Book()

        self.assertEqual(None, book.authors)

    def test_book_producer(self):
        book = Book()
        book.book_producer = "abc"

        self.assertEqual("abc", book.book_producer)

    def test_book_producer_defaults_to_none(self):
        book = Book()

        self.assertEqual(None, book.book_producer)

    def test_comments(self):
        book = Book()
        book.comments = "abc"

        self.assertEqual("abc", book.comments)

    def test_comments_defaults_to_none(self):
        book = Book()

        self.assertEqual(None, book.comments)

    def test_cover(self):
        book = Book()
        book.cover = "abc"

        self.assertEqual("abc", book.cover)

    def test_cover_defaults_to_none(self):
        book = Book()

        self.assertEqual(None, book.cover)

    def test_isbn(self):
        book = Book()
        book.isbn = "abc"

        self.assertEqual("abc", book.isbn)

    def test_isbn_defaults_to_none(self):
        book = Book()

        self.assertEqual(None, book.isbn)

    def test_publisher(self):
        book = Book()
        book.publisher = "abc"

        self.assertEqual("abc", book.publisher)

    def test_publisher_defaults_to_none(self):
        book = Book()

        self.assertEqual(None, book.publisher)

    def test_series(self):
        book = Book()
        book.series = "abc"

        self.assertEqual("abc", book.series)

    def test_series_defaults_to_none(self):
        book = Book()

        self.assertEqual(None, book.series)

    def test_tags(self):
        book = Book()
        book.tags = "abc"

        self.assertEqual("abc", book.tags)

    def test_tags_defaults_to_none(self):
        book = Book()

        self.assertEqual(None, book.tags)

    def test_title(self):
        book = Book()
        book.title = "abc"

        self.assertEqual("abc", book.title)

    def test_title_defaults_to_none(self):
        book = Book()

        self.assertEqual(None, book.title)

    def test_title_sort(self):
        book = Book()
        book.title_sort = "abc"

        self.assertEqual("abc", book.title_sort)

    def test_title_sort_defaults_to_none(self):
        book = Book()

        self.assertEqual(None, book.title_sort)


class TestChapter(unittest.TestCase):

    # todo from_dict

    def test_publish(self):
        chapter = Chapter()
        chapter.publish = False

        self.assertEqual(False, chapter.publish)

    def test_publish_defaults_to_true(self):
        chapter = Chapter()

        self.assertEqual(True, chapter.publish)

    def test_source(self):
        chapter = Chapter()
        chapter.source = "abc"

        self.assertEqual("abc", chapter.source)

    def test_source_defaults_to_none(self):
        chapter = Chapter()

        self.assertEqual(None, chapter.source)


if __name__ == '__main__':
    unittest.main()
