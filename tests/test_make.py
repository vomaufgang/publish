#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_chapter
----------------------------------

Tests for `apub.model.chapter` module.
"""

import unittest
from unittest.mock import MagicMock, patch

from apub.errors import OutputNotFoundError
from apub.make import make, make_every_output, find_output_by_name
from apub.output import Output
from apub.project import Project


class TestMake(unittest.TestCase):
    def test_make(self):
        # book = Book()
        # book.title = "Book"
        # book.authors = "Author"
        #
        # chapter = Chapter()
        # chapter.title = "Chapter 1"
        # chapter.source = 'D:\\Test\\test.chapter'
        # book.chapters.append(chapter)
        #
        # chapter = Chapter()
        # chapter.title = "Chapter 2"
        # chapter.source = 'D:\\Test\\test.chapter'
        # book.chapters.append(chapter)
        #
        # project = Project()
        # project.book = book
        #
        # html = HtmlOutput()
        # html.path = 'D:\\Test\\test.html'
        # html.single_file = True  # todo shouldn't his be false by default?
        #
        # project.outputs.append(html)
        #
        # make(project)

        pass

    def test_find_output_by_name_finds_output(self):
        mock_outputs = list(self.get_mock_outputs(3))
        for i, mock_output in enumerate(mock_outputs):
            mock_output.name = str(i)

        expected = mock_outputs[1]
        actual = find_output_by_name(mock_outputs, '1')

        self.assertEqual(actual, expected)

        self.assertNotEqual(actual, mock_outputs[0])
        self.assertNotEqual(actual, mock_outputs[2])

    def test_find_output_by_name_no_match_raises_output_not_found_error(self):
        mock_outputs = list(self.get_mock_outputs(3))
        for i, mock_output in enumerate(mock_outputs):
            mock_output.name = str(i)

        with self.assertRaises(OutputNotFoundError) as context_manager:
            find_output_by_name(mock_outputs, '3')

        exception = context_manager.exception

        excpected = "No output using the following name could be found: '3'"
        actual = str(exception)

        self.assertEqual(actual, excpected)

    @patch('apub.make.make_every_output')
    def test_make_omitting_output_calls_make_every_output(
            self, mocked_make_every_output):
        make(Project())
        make_every_output_called = mocked_make_every_output.called

        self.assertTrue(make_every_output_called)

    def test_make_every_output_makes_every_output(self):
        mock_outputs = self.get_mock_outputs(3)

        project = Project()
        project.outputs = mock_outputs

        make_every_output(project)

        all_called = all(mock_output.make.called
                         for mock_output in mock_outputs)

        self.assertTrue(all_called)

    def get_mock_outputs(self, amount):
        class TestOutput(Output):
            def make(self, **kwargs):
                pass

        for _ in range(amount):
            mock_output = TestOutput()
            mock_output.make = MagicMock()
            yield mock_output


if __name__ == '__main__':
    unittest.main()
