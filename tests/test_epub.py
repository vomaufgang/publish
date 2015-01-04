#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_epub
----------------------------------

Tests for `apub.model.epub` module.
"""

import unittest
from apub.output.epub import EpubOutput
from apub import Project


class TestEpub(unittest.TestCase):

    def setUp(self):
        self.epub_output = EpubOutput(Project(), '')
        pass

    def test_change_justification_set_original(self):
        justification = 'original'
        self.epub_output.change_justification = justification
        self.assertEqual(justification, self.epub_output.change_justification)

    def test_change_justification_set_left(self):
        justification = 'left'
        self.epub_output.change_justification = justification
        self.assertEqual(justification, self.epub_output.change_justification)

    def test_change_justification_set_justify(self):
        justification = 'justify'
        self.epub_output.change_justification = justification
        self.assertEqual(justification, self.epub_output.change_justification)

    def test_change_justification_set_right(self):
        justification = 'right'
        self.epub_output.change_justification = justification
        self.assertEqual(justification, self.epub_output.change_justification)

    def test_invalid_change_justification_raises_attribute_error(self):
        with self.assertRaises(AttributeError):
            self.epub_output.change_justification = 'foo'

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
