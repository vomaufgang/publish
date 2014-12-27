#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_apub
----------------------------------

Tests for `apub` module.
"""

import unittest
from apub.model.chapter import Chapter

# from apub import apub


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

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
