#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_project
----------------------------------

Tests for `apub.model.project` module.
"""

import unittest
from unittest.mock import MagicMock

from apub.output.json import JsonOutput
from apub.book import Book, Chapter
from apub.output.html import HtmlOutput


class TestJsonOutput(unittest.TestCase):

    def test_make(self):
        json_output = JsonOutput()
        json_output._write = MagicMock(name='_write')
        # todo this can be used to verify the resulting json object without
        #      having to read actual chapter files from disk
        HtmlOutput.get_chapters_html = MagicMock(name='get_chapters_html')

        book = Book()
        book.chapters = [Chapter('title', 'source')]

        result = json_output.make(book, [])

        assert json_output._write.called is True


if __name__ == '__main__':
    unittest.main()
