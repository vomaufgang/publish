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

import logging
import os
import subprocess
from abc import ABCMeta, abstractmethod
from tempfile import mkstemp

import markdown
from pkg_resources import resource_string
from typing import List

from apub.book import Book
from apub.errors import NoChaptersFoundError
from apub.fromdict import FromDict
from apub.substitute import Substitute

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler)


class Output(FromDict, metaclass=ABCMeta):
    def __init__(self):
        self.name = None
        self.path = None
        self.css = None
        self.force_publish = False

    @abstractmethod
    def make(self, book, substitutions):
        pass

    @classmethod
    def from_dict(cls, dict_):
        output_type = cls.get_value_from_dict('type', dict_)

        if output_type == 'html':
            output = HtmlOutput.from_dict(dict_)
        elif output_type == 'json':
            raise NotImplementedError('Output type \'json\' is planned '
                                      'for Version 3.0')
        elif output_type == 'ebook-convert':
            output = EbookConvertOutput.from_dict(dict_)
        else:
            raise NotImplementedError(
                'Unrecognized output type: {0}'.format(output_type))

        # todo validate mandatory parameters name & path

        get_value = cls.get_value_from_dict

        output.name = get_value('name', dict_)
        output.path = get_value('path', dict_)
        output.css = get_value('css', dict_)
        output.force_publish = get_value(
            'force_publish', dict_, default=False)

        return output

    @staticmethod
    def filter_chapters_by_publish(chapters, publish=True):
        for chapter in chapters:
            if chapter.publish == publish:
                yield chapter


# !/usr/bin/env python3
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


_supported_metadata_attrs = {
    'ebook-convert': [
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
}


# todo apart from error handling, logging and validation, this should be
#      usable already - test it


class EbookConvertOutput(Output):
    def __init__(self):
        super().__init__()
        self.ebookconvert_params = []

    def make(self, book: Book, substitutions: List[Substitute]):
        (temp_handle, temp_path) = mkstemp(suffix=".html")
        try:
            self._make_html(temp_path, book, substitutions)

            call_params = [
                'ebook-convert',
                temp_path,
                self.path
            ]

            # todo validate mandatory book attributes - are there even any
            #      mandatory ones?

            call_params.extend(_yield_attrs_as_ebookconvert_params(book))
            call_params.extend(self.ebookconvert_params)

            subprocess.call(call_params)
        finally:
            os.remove(temp_path)

    def _make_html(self,
                   temp_path: str,
                   book: Book,
                   substitutions: List[Substitute]):
        html_output = HtmlOutput()

        html_output.path = temp_path
        html_output.css = self.css
        html_output.force_publish = self.force_publish

        html_output.make(book, substitutions)

    @classmethod
    def from_dict(cls, dict_: dict):
        ebook_convert_output = EbookConvertOutput()

        ebook_convert_output.ebookconvert_params = cls.get_value_from_dict(
            'ebookconvert_params', dict_, [])

        return ebook_convert_output


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
    for attr_name in _supported_metadata_attrs:
        if hasattr(object_, attr_name):
            attr = str(getattr(object_, attr_name))
            if attr and not attr.isspace():
                yield "--{0}=\"{1}\"".format(attr_name, attr)


# todo optional subtitle


class HtmlOutput(Output):
    def __init__(self):
        super().__init__()
        self.css_path = None
        self.generate_toc = False  # todo implement HtmlOutput.generate_toc
        #    ^ is dependant upon book & chapter url_friendly_title
        #      for jump links

    def make(self,
             book: Book,
             substitutions: List[Substitute] = None) -> None:
        if not book:
            raise AttributeError("book must not be None")

        if not substitutions:
            substitutions = []

        html_ = self.get_html(book, substitutions)

        html_ = self._apply_template(content=html_,
                                     title=book.title,
                                     css=self._get_css(),
                                     language=book.language)

        self.write_file(html_)

    def write_file(self, html_: str):
        with open(self.path, 'w') as file:
            file.write(html_)

    def _apply_template(self,
                        content: str,
                        title: str,
                        css: str,
                        language: str) -> str:
        template = resource_string(__name__, 'template.html')

        return template.format(content=content,
                               title=title,
                               css=css,
                               language=language)

    def _get_css(self) -> str:
        if not self.css_path:
            return ''

        css_path = os.path.join(os.getcwd(), self.css_path)

        with open(css_path, 'r') as file:
            css = file.read()

        return css if css else ''

    def get_html(self,
                 book: Book,
                 substitutions: List[Substitute]) -> str:
        markdown_ = self._read_markdown(book)

        markdown_ = self._apply_substitutions(
            markdown_,
            substitutions)

        html_ = markdown.markdown(markdown_)

        return html_

    def _read_markdown(self, book: Book) -> str:
        # todo document HtmlOutput._read_markdown
        # todo unit test HtmlOutput._read_markdown
        markdown_ = []
        md_paragraph_sep = '\n\n'

        if not book.chapters or len(book.chapters) <= 0:
            raise NoChaptersFoundError('Your book contains no chapters that'
                                       'could be published.')

        if self.force_publish:
            chapters = book.chapters
        else:
            chapters = filter(lambda x: x.publish is True,
                              book.chapters)

        if len(chapters) <= 0:
            raise NoChaptersFoundError('None of your chapters are set to be'
                                       'published.')

        for chapter in chapters:
            with open(chapter.source, 'r') as file:
                markdown_.append(file.read())

        return md_paragraph_sep.join(markdown_)

    def _apply_substitutions(self, markdown_, substitutions):
        """Applies the list of substitutions to the markdown content.

        Args:
            markdown_ (str): 
                The dict of markdown strings by chapter.
            substitutions (list of apub.substitute.Substitute):
                The list of substitutions to be applied.

        Returns:
            str: The dict of markdown strings by chapter with
                 the substitutions applied.
        """
        for substitution in substitutions:
            markdown_ = substitution.apply_to(markdown_)

        return markdown_

    @classmethod
    def from_dict(cls, dict_: dict) -> 'HtmlOutput':
        html_output = HtmlOutput()
        get_value = cls.get_value_from_dict

        html_output.css_path = get_value('css_path',
                                         dict_,
                                         default=None)

        return html_output


class JsonOutput(Output):
    def __init__(self):
        super().__init__()
        raise NotImplementedError('Planned for Version 3.0')

    def make(self, book, substitutions):
        raise NotImplementedError('Planned for Version 3.0')

    @classmethod
    def from_dict(cls, dict_):
        raise NotImplementedError('Planned for Version 3.0')
