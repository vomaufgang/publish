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
import subprocess
from tempfile import mkstemp
from typing import List

from apub.book import Book
from apub.output.output import Output
from apub.output.html import HtmlOutput
from apub.substitution import Substitution

import logging.config
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


_supported_metadata_attrs = [
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

# todo apart from error handling, logging and validation, this should be
#      usable already - test it


class EbookConvertOutput(Output):

    def __init__(self):
        super().__init__()
        self.ebookconvert_params = []

    def make(self, book: Book, substitutions: List[Substitution]):
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
                   substitutions: List[Substitution]):
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




