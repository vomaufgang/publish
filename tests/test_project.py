#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_project
----------------------------------

Tests for `apub.model.project` module.
"""

import unittest
from apub.model.project import Project


class TestProject(unittest.TestCase):

    def setUp(self):
        self.project = Project()
        pass

    def test_books_cannot_be_set(self):
        with self.assertRaises(AttributeError):
            self.project.books = []

    def test_outputs_cannot_be_set(self):
        with self.assertRaises(AttributeError):
            self.project.outputs = []

    def test_simple_substitutions_cannot_be_set(self):
        with self.assertRaises(AttributeError):
            self.project.simple_substitutions = []

    def test_regex_substitutions_cannot_be_set(self):
        with self.assertRaises(AttributeError):
            self.project.regex_substitutions = []

    def test_read(self):
        pass

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
