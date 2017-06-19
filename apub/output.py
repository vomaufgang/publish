#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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

import logging
import markdown
import os
import shutil
import subprocess
import uuid
from abc import ABCMeta, abstractmethod
from pkg_resources import resource_string
from tempfile import mkdtemp

from apub.errors import NoChaptersFoundError

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler)


_supported_ebookconvert_attrs = [
    'author_sort',
    'authors',
    'book_producer'
    'comments',
    'cover',
    'isbn',
    'language',
    'pubdate',
    'publisher',
    'rating',
    'series',
    'series_index',
    'tags',
    'title'
]

# todo: Output has 'css', html_output has 'css_path' - choose one,
#       remove the other

# todo validate mandatory book attributes - are there even any
#      mandatory ones?

# todo optional subtitle, supported by HtmlOutput and JsonOutput

# todo what was generate_toc even for?


class Output(metaclass=ABCMeta):
    """Abstract base class for specific Output implementations.

    :ivar css_path: The path to the style sheet.
    :ivar force_publish: Determines wether to force publish all chapters.
        
        If set to true, all chapters of the book will be published
        no matter how the chapters are configured.
    :ivar path: The output path.
    """

    def __init__(self):
        self.css_path = None
        self.force_publish = False
        self.path = None

    @abstractmethod
    def make(self, book, substitutions):
        pass

    def get_chapters_to_publish(self, book):
        if self.force_publish:
            return book.chapters
        else:
            return list(filter(lambda x: x.publish is True, book.chapters))

    def validate(self):
        """Validates the Book object.
        
        Errors are raised as AttributeErrors."""
        if not self.path:
            raise AttributeError('Output path must be set.')


class EbookConvertOutput(Output):

    def __init__(self,
                 path=None,
                 css_path=None,
                 force_publish=False,
                 ebookconvert_params=None):
        super().__init__()
        self.path = path
        self.css_path = css_path
        self.force_publish = force_publish
        self.ebookconvert_params = \
            [] if not ebookconvert_params else ebookconvert_params

    def make(self,
             book,
             substitutions=None):
        if not book:
            raise AttributeError("book must not be None")

        if not substitutions:
            substitutions = []

        self.validate()

        temp_directory = mkdtemp()
        # mkstmp and NamedTemporaryFile won't work, because the html file
        # will be kept open by EbookConvertOutput with exclusive access,
        # which means ebook-convert can't read the html to create the epub.
        # -> ebook-convert fails with 'Permission denied'.

        try:
            html_output = HtmlOutput()
            html_output.path = os.path.join(
                temp_directory, str(uuid.uuid4()) + '.html')
            html_output.css_path = self.css_path
            html_output.force_publish = self.force_publish

            html_output.make(book, substitutions)

            call_params = [
                'ebook-convert',
                html_output.path,
                self.path
            ]

            call_params.extend(_yield_attrs_as_ebookconvert_params(book))
            call_params.extend(self.ebookconvert_params)

            subprocess.call(call_params)
        finally:
            shutil.rmtree(temp_directory)


def _yield_attrs_as_ebookconvert_params(object_):
    """Takes an object and returns a generator yielding all attributes
    that can be processed by the ebookconvert command line as a param array.

    Args:
        object_ (object): An object

    Returns:
        A generator yielding all attributes of the object supported by
        ebookconvert.
    """
    # This way the book can contain attrs not supported by ebookconvert
    # (or any other specific output that follows this explicit pattern)
    for attr_name in _supported_ebookconvert_attrs:
        if hasattr(object_, attr_name):
            attr = getattr(object_, attr_name)
            if not attr:
                continue
            attr = str(attr)
            if attr and not attr.isspace():
                yield "--{0}=\"{1}\"".format(attr_name, attr)


class HtmlOutput(Output):

    def __init__(self, path=None, css_path=None, force_publish=False):
        super().__init__()
        self.path = path
        self.css_path = css_path
        self.force_publish = force_publish

    def make(self, book, substitutions=None):
        """Makes the HtmlOutput for the provided book and substitutions.
        """
        if not book:
            raise AttributeError("book must not be None")

        if not substitutions:
            substitutions = []

        html_document = self._get_html_document(book, substitutions)

        with open(self.path, 'w') as file:
            file.write(html_document)

    def _get_html_document(self, book, substitutions):

        html_content = self._get_html_content(book, substitutions)
        html_document = self._apply_template(html_content=html_content,
                                             title=book.title,
                                             css=self._get_css(),
                                             language=book.language)

        return html_document

    def _get_html_content(self, book, substitutions):
        markdown_ = self._get_markdown_content(book)
        markdown_ = self._apply_substitutions(
            markdown_,
            substitutions)

        return markdown.markdown(markdown_)

    def _apply_template(self,
                        html_content: str,
                        title: str,
                        css: str,
                        language: str) -> str:
        template = resource_string(__name__, 'template.html')\
            .decode('utf-8')\
            .replace('\r\n', '\n')
        # resource_string opens the file as bytes, which means that we
        # have to decode to utf-8. The replace is necessary because
        # resource_string, instead of open, does not automatically
        # strip \r\n down to \n on windows systems. Leaving \r\n as is
        # would produce double line breaks when writing the resulting string
        # back to disc, thus we have to do the replacement ourselves, too.

        return template.format(content=html_content,
                               title=title,
                               css=css,
                               language=language)

    def _get_css(self):
        if not self.css_path:
            return ''

        css_path = os.path.join(os.getcwd(), self.css_path)

        with open(css_path, 'r') as file:
            css = file.read()

        return css if css else ''

    def _get_markdown_content(self, book):
        markdown_ = []
        md_paragraph_sep = '\n\n'

        if not book.chapters or len(book.chapters) <= 0:
            raise NoChaptersFoundError('Your book contains no chapters that'
                                       'could be published.')

        chapters_to_publish = self.get_chapters_to_publish(book)

        if len(chapters_to_publish) <= 0:
            raise NoChaptersFoundError('None of your chapters are set to be'
                                       'published.')

        for chapter in chapters_to_publish:
            with open(chapter.source, 'r') as file:
                markdown_.append(file.read())

        return md_paragraph_sep.join(markdown_)

    def _apply_substitutions(
            self,
            markdown_,
            substitutions):
        """Applies the list of substitutions to the markdown content.

        :param markdown_: The markdown content of the chapter.
        :param substitutions: The list of substitutions to be applied.

        :returns: The dict of markdown strings by chapter with
            the substitutions applied.
        """
        for substitution in substitutions:
            markdown_ = substitution.apply_to(markdown_)

        return markdown_


class JsonOutput(Output):
    """Planned for Version 3.0"""

    def __init__(self):
        super().__init__()
        raise NotImplementedError('Planned for Version 3.0')

    def make(self, book, substitutions):
        raise NotImplementedError('Planned for Version 3.0')
