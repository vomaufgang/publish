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

from apub.output import Output
from apub.errors import NoChaptersFoundError
from apub.metadata import Book, Chapter

import logging
import logging.config
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())



class HtmlOutput(Output):

    def __init__(self):
        super().__init__()
        self.single_file = False
        pass

    def make(self, project):
        # todo if not path: return generated html content
        # todo implement HtmlOutput.make
        """

        Args:
            project (Book):
        """

        from ..metadata import Book, Chapter
        if not project:
            raise AttributeError("project must not be None")

        if not project.chapters or len(project.chapters) <= 0:
            raise NoChaptersFoundError()

        html = []
        for chapter in project.chapters:
            html.append(Html.from_chapter(chapter))


        Html.from_chapter(Chapter())
        Html.from_file("")
        raise NotImplementedError

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
    def from_markdown(cls, markdown_content, substitutions=None):
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
