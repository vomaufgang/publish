#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_apub
----------------------------------

Tests for `apub` module.
"""

import unittest
import os
import inspect

from apub import Chapter, apub


class TestApub(unittest.TestCase):

    def setUp(self):
        pass

    def test_something(self):
        pass

    def test_read_chapter(self):
        chapter = Chapter()
        chapter.path = os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))),
                                    'test_apub.md')
        chapter, lines = apub.read_chapter(chapter)

        self.assertEqual(3, len(lines))
        pass

    def tearDown(self):
        pass


def module_path(local_function):
    return os.path.abspath(inspect.getsourcefile(local_function))


if __name__ == '__main__':
    unittest.main()