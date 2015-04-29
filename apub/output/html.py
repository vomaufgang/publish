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


import os
import markdown

from .output import Output


class HtmlOutput(Output):
    def __init__(self):
        super().__init__()
        self.single_file = False
        pass

    def make(self, metadata, chapters, substitutions):
        # todo if not path: return generated html content
        # todo implement HtmlOutput.make
        raise NotImplementedError

    @staticmethod
    def from_dict(dict_):
        html_output = HtmlOutput()

        for k, v in dict_.items():
            setattr(html_output, k, v)

        return html_output


class _Html():
    """Provides methods that return the finished html content for a single
    chapter, including the application of substitutions."""
    @staticmethod
    def from_chapter(chapter, substitutions=None):
        """Returns the resulting html content of a chapter, applying all
        substitutions and transforming the contents from markdown to html.

        The file that is associated with the chapter must contain markdown
        content.

        Optionally a list of substitutions can be supplied. These will be
        applied to the contents *before* the transformation from markdown to
        html takes place. For a list of possible substitution types please
        take a look at the :py:mod:`substitution` package.

        Args:
            :param chapter: the chapter
            :type chapter: :class:`Chapter`
            :param substitutions: the list of substitutions to be applied
                [optional]
            :type substitutions: subclass of :class:`Substitution` or None

        :rtype: string containing html
        """
        return _Html.from_file(chapter.source, substitutions)

    @staticmethod
    def from_file(path, substitutions=None):
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
                return _Html.from_markdown(contents, substitutions)
        except IOError:
            raise

    @staticmethod
    def from_markdown(markdown_content, substitutions=None):
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
            :param substitutions: the list of substitutions to be applied
                [optional]
            :type substitutions: subclass of :class:`Substitution` or None

        :rtype: string containing html
        """
        for substitution in substitutions:
            substitution.apply_to(markdown_content)

        return markdown.markdown(markdown_content)
