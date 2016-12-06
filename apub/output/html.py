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
import os.path
from pkg_resources import resource_string

from apub.output import Output
from apub.errors import NoChaptersFoundError
from apub.book import Book
from apub.substitution import Substitution

import logging.config
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

# todo css, title + optional subtitle, lang


class HtmlOutput(Output):

    def __init__(self):
        super().__init__()
        self.css_path = ''
        pass

    def make(self, book, substitutions=None):
        if not book:
            raise AttributeError("book must not be None")

        if substitutions is None:
            substitutions = []

        chapters_html = self.get_chapters_html(book, substitutions)

        self.write_file(chapters_html, book)

    def write_file(self, chapters_html, book):
        content = '\n'.join(chapters_html.values())
        template = resource_string(__name__, 'template.html')

        html = template.format(content=content,
                               title=book.title,
                               css=self._get_css())

        with open(self.path, 'w') as file:
            file.write(html)

    def _get_css(self):
        css_path = os.path.join(os.getcwd(), self.css_path)

        with open(css_path, 'r') as file:
            css = file.read()

        return css if css else ''

    def get_chapters_html(self, book, substitutions):
        chapters_markdown = self._read_chapters_markdown(book)

        chapters_markdown = self._apply_substitutions(
                chapters_markdown,
                substitutions)

        chapters_html = self._transform_markdown_to_html(
                chapters_markdown)

        return chapters_html

    def _read_chapters_markdown(self, book):
        chapters_markdown = {}
        if not book.chapters or len(book.chapters) <= 0:
            raise NoChaptersFoundError()

        for chapter in book.chapters:
            with open(chapter.source, 'r') as file:
                chapters_markdown[chapter] = file.read()

        return chapters_markdown

    def _transform_markdown_to_html(self, markdown_):
        html_ = {}
        for chapter in markdown_:
            html_[chapter] = Html.from_markdown(
                    markdown_[chapter])
        return html_

    def _apply_substitutions(self, markdown_, substitutions):
        """Applies the list of substitutions to the markdown content.

        Args:
            markdown_ (dict[str]): The dict of markdown strings by chapter.
            substitutions (list[Substitution]):
                The list of substitutions to be applied.

        Returns:
            dict[str]: The dict of markdown strings by chapter with
                 the substitutions applied.
        """
        for chapter in markdown_:
            for substitution in substitutions:
                markdown_[chapter] = substitution.apply_to(
                        markdown_[chapter])

        return markdown_

    @classmethod
    def from_dict(cls, dict_):
        html_output = HtmlOutput()
        get_value = cls.get_value_from_dict

        html_output.css_path = get_value('css_path',
                                         dict_,
                                         default=None)

        return html_output


class Html:
    """Provides methods that return the finished html content for a single
    chapter, including the application of substitutions."""
    @classmethod
    def from_chapter(cls, chapter):
        """Returns the resulting html content of a chapter, applying all
        substitutions and transforming the contents from markdown to html.

        The file that is associated with the chapter must contain markdown
        content.

        Optionally a list of substitutions can be supplied. These will be
        applied to the contents *before* the transformation from markdown to
        html takes place. For a list of possible substitution types please
        take a look at the :py:mod:`substitution` package.

        Args:
            chapter (apub.book.Chapter): The chapter.

        Returns:
            str: the resulting html
        """
        return Html.from_file(chapter.source)

    @classmethod
    def from_file(cls, path):
        # todo new docstring format
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

        :rtype: string containing html
        """
        try:
            with open(path, encoding='utf-8') as file:
                contents = file.read()
                return Html.from_markdown(contents)
        except IOError:
            raise

    @classmethod
    def from_markdown(cls, markdown_content):
        # todo new docstring format
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
