#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_chapter
----------------------------------

Tests for `apub.model.chapter` module.
"""

import unittest
from apub import Chapter


class TestChapter(unittest.TestCase):

    def setUp(self):
        self.chapter = Chapter()
        pass

    def test_id(self):
        test_id = 'Id-1'
        self.chapter.id = test_id
        self.assertEqual(test_id, self.chapter.id)

    def test_invalid_id_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.chapter.id = '@?\/.+'

    def test_read(self):
        pass

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
