#!/usr/bin/env python3
# coding: utf8
#
# apub - Python package with cli to turn markdown files into ebooks
# Copyright (C) 2015  Christopher Knörndel
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import markdown

from apub.output import Output
from apub.errors import NoChaptersFoundError
from apub.book import Book, Chapter
from apub.substitution import Substitution

import logging
import logging.config
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class HtmlOutput(Output):

    def __init__(self):
        super().__init__()
        self.single_file = False
        pass

    def make(
            self,
            book,
            substitutions):
        """

        Args:
            substitutions (list[Substitution]): todo
            book (Book): todo
        """
        # todo implement HtmlOutput.make
        # todo docstring

        if not book:
            raise AttributeError("book must not be None")
        if not substitutions or hasattr(substitutions, "__iter__"):
            log.warn("")

        chapters_html = HtmlOutput.get_chapters_html(book, substitutions)

        if self.single_file:
            self.write_single_file(chapters_html)
        else:
            self.write_file_per_chapter(chapters_html)

    def write_single_file(self, chapters_html):
        with open(self.path, 'w') as file:
            for chapter in chapters_html:
                if chapter.publish or self.force_publish:
                    file.writelines(chapters_html[chapter])

    def write_file_per_chapter(self, html_):
        # todo remember to implement force_publish vs false
        raise NotImplementedError

    @classmethod
    def get_chapters_html(cls, book, substitutions):
        """

        Args:
            book:
            substitutions:

        Returns:
            dict[Chapter,str]:
        """
        chapters_markdown = HtmlOutput._read_chapters_markdown(book)

        chapters_markdown = HtmlOutput._apply_substitutions(
                chapters_markdown,
                substitutions)

        chapters_html = HtmlOutput._transform_markdown_to_html(
                chapters_markdown)

        return chapters_html

    @classmethod
    def _read_chapters_markdown(cls, book):
        chapters_markdown = {}
        if not book.chapters or len(book.chapters) <= 0:
            raise NoChaptersFoundError()

        for chapter in book.chapters:
            with open(chapter.source, 'r') as file:
                chapters_markdown[chapter] = file.read()

        return chapters_markdown

    @classmethod
    def _transform_markdown_to_html(cls, markdown_):
        html_ = {}
        for chapter in markdown_:
            html_[chapter] = Html.from_markdown(
                    markdown_[chapter])
        return html_

    @classmethod
    def _apply_substitutions(cls, markdown_, substitutions):
        for chapter in markdown_:
            for substitution in substitutions:
                markdown_[chapter] = substitution.apply_to(
                        markdown_[chapter])

        return markdown_

    @classmethod
    def from_dict(cls, dict_):
        html_output = HtmlOutput()

        # todo move away from this generic solution and set + validate required fields instead

        for k, v in dict_.items():
            setattr(html_output, k, v)

        return html_output


class Html:
    """Provides methods that return the finished html content for a single
    chapter, including the application of substitutions."""
    @classmethod
    def from_chapter(cls, chapter, substitutions=None):
        """Returns the resulting html content of a chapter, applying all
        substitutions and transforming the contents from markdown to html.

        The file that is associated with the chapter must contain markdown
        content.

        Optionally a list of substitutions can be supplied. These will be
        applied to the contents *before* the transformation from markdown to
        html takes place. For a list of possible substitution types please
        take a look at the :py:mod:`substitution` package.

        Args:
            chapter (apub.metadata.Chapter): The chapter.
            substitutions (apub.substitution.Substitution): The list of
                substitutions to be applied. Defaults to None. [optional]

        Returns:
            str: the resulting html
        """
        return Html.from_file(chapter.source, substitutions)

    @classmethod
    def from_file(cls, path, substitutions=None):
        """Returns the resulting html content of a file, applying all
        substitutions and transforming the contents from markdown to html.

        The file must contain markdown content.

        Optionally a list of substitutions can be supplied. These will be
        applied to the contents *before* the transformation from markdown to
        html takes place. For a list of possible substitution types please
        take a look at the :py:mod:`substitution` package.

        Args:
            :param path: the path to the file
            :type path: string
            :param substitutions: the list of substitutions to be applied
                [optional]
            :type substitutions: subclass of :class:`Substitution` or None

        :rtype: string containing html
        """
        try:
            with open(path, encoding='utf-8') as file:
                contents = file.read()
                return Html.from_markdown(contents, substitutions)
        except IOError:
            raise

    @classmethod
    def from_markdown(cls, markdown_content):
        """Returns the resulting html content of a string containing markdown,
        applying all substitutions and transforming the contents from markdown
        to html.

        Optionally a list of substitutions can be supplied. These will be
        applied to the contents *before* the transformation from markdown to
        html takes place. For a list of possible substitution types please
        take a look at the :py:mod:`substitution` package.

        Args:
            :param markdown_content: the markdown content
            :type markdown_content: string

        :rtype: string containing html
        """
        return markdown.markdown(markdown_content)
