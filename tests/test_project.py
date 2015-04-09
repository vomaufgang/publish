#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_project
----------------------------------

Tests for `apub.model.project` module.
"""

import unittest
from apub.metadata import Project


class TestProject(unittest.TestCase):

    def setUp(self):
        self.project = Project()
        pass

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
