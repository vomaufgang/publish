#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_book
----------------------------------

Tests for `apub.model.book` module.
"""

import unittest
from apub import Book


class TestBook(unittest.TestCase):

    def setUp(self):
        self.book = Book()
        pass

    def test_title_set_and_get(self):
        title = "abc"
        self.book.title = title
        self.assertEqual(title, self.book.title)

    def test_title_set_to_None_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.book.title = None

    def test_title_set_to_empty_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.book.title = ""

    def test_title_set_to_space_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.book.title = " "

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
