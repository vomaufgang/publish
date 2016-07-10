#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_chapter
----------------------------------

Tests for `apub.model.chapter` module.
"""

import unittest
from apub.book import Book, Chapter
from apub.project import Project
from apub.output import HtmlOutput
from apub.make import make


class TestMake(unittest.TestCase):
    def test_make(self):
        book = Book()
        book.title = "Book"
        book.authors = "Author"

        chapter = Chapter()
        chapter.title = "Chapter 1"
        chapter.source = 'D:\\Test\\test.chapter'
        book.chapters.append(chapter)

        chapter = Chapter()
        chapter.title = "Chapter 2"
        chapter.source = 'D:\\Test\\test.chapter'
        book.chapters.append(chapter)

        project = Project()
        project.book = book

        html = HtmlOutput()
        html.path = 'D:\\Test\\test.html'
        html.single_file = True  # todo shouldn't his be false by default?

        project.outputs.append(html)

        make(project)

        pass


if __name__ == '__main__':
    unittest.main()
