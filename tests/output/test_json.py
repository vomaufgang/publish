#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_project
----------------------------------

Tests for `apub.model.project` module.
"""

import unittest
from unittest.mock import patch
from unittest.mock import MagicMock

from apub.errors import MalformedProjectJsonError
from apub.output.json import JsonOutput


class TestJsonOutput(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_make(self):
        json_output = JsonOutput()
        json_output._write = MagicMock(name='_write')
        result = json_output.make({}, [], [])

        assert json_output._write.called is True



if __name__ == '__main__':
    unittest.main()
