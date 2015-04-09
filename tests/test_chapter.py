#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_chapter
----------------------------------

Tests for `apub.model.chapter` module.
"""

import unittest
from apub.metadata import Chapter
import validators


class TestChapter(unittest.TestCase):

    def setUp(self):
        self.chapter = Chapter()
        pass

    def test_read(self):
        pass

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
