#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# apub - Python package with cli to turn markdown files into ebooks
# Copyright (c) 2014 Christopher Knörndel
#
# Distributed under the MIT License
# (license terms are at http://opensource.org/licenses/MIT).

"""Tests for `apub.output` module.
"""

# pylint: disable=missing-docstring,no-self-use,invalid-name,protected-access

from typing import Iterable
from unittest.mock import patch, mock_open

import os
import pytest

from apub import __version__ as apub_version
from apub.book import Book, Chapter
# noinspection PyProtectedMember
from apub.output import (SUPPORTED_EBOOKCONVERT_ATTRIBUTES,
                         _apply_template,
                         _yield_attributes_as_params,
                         HtmlOutput, _get_ebook_convert_params)
from apub.substitution import Substitution, SimpleSubstitution
from tests import get_test_book


def test_supported_ebookconvert_attrs():
    assert len(SUPPORTED_EBOOKCONVERT_ATTRIBUTES) == 14
    assert 'author_sort' in SUPPORTED_EBOOKCONVERT_ATTRIBUTES
    assert 'authors' in SUPPORTED_EBOOKCONVERT_ATTRIBUTES
    assert 'book_producer' in SUPPORTED_EBOOKCONVERT_ATTRIBUTES
    assert 'comments' in SUPPORTED_EBOOKCONVERT_ATTRIBUTES
    assert 'cover' in SUPPORTED_EBOOKCONVERT_ATTRIBUTES
    assert 'isbn' in SUPPORTED_EBOOKCONVERT_ATTRIBUTES
    assert 'language' in SUPPORTED_EBOOKCONVERT_ATTRIBUTES
    assert 'pubdate' in SUPPORTED_EBOOKCONVERT_ATTRIBUTES
    assert 'publisher' in SUPPORTED_EBOOKCONVERT_ATTRIBUTES
    assert 'rating' in SUPPORTED_EBOOKCONVERT_ATTRIBUTES
    assert 'series' in SUPPORTED_EBOOKCONVERT_ATTRIBUTES
    assert 'series_index' in SUPPORTED_EBOOKCONVERT_ATTRIBUTES
    assert 'tags' in SUPPORTED_EBOOKCONVERT_ATTRIBUTES
    assert 'title' in SUPPORTED_EBOOKCONVERT_ATTRIBUTES


TEST_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="{language}">
<head>
<meta charset="UTF-8">
<meta name="generator" content="apub {apub_version}" />
<title>{title}</title>
<style type="text/css">
{css}
</style>
</head>
<body>
{content}
</body>
</html>"""


# noinspection PyMissingOrEmptyDocstring
class OutputStub(HtmlOutput):
    def make(self, book: Book, substitutions: Iterable[Substitution] = None):
        pass


class TestHtmlOutput:
    def test_constructor(self):
        output = OutputStub('a',
                            css_path='b',
                            force_publish=True)

        assert output.path == 'a'
        assert output.css_path == 'b'
        assert output.force_publish

    def test_constructor_default_values(self):
        output = OutputStub('a')

        assert output.path == 'a'
        assert output.css_path is None
        assert output.force_publish is not True

    def test_get_chapters_to_be_published(self):
        output = OutputStub('a')
        chapters = [Chapter('1', publish=True),
                    Chapter('2', publish=False),
                    Chapter('3')]  # defaults to True

        expected = [chapters[0],
                    chapters[2]]
        actual = output.get_chapters_to_be_published(chapters)

        assert actual == expected

    def test_get_chapters_to_be_published_force_publish_true(self):
        output = OutputStub('a', force_publish=True)
        chapters = [Chapter('1', publish=True),
                    Chapter('2', publish=False),
                    Chapter('3')]  # defaults to True

        expected = [chapters[0],
                    chapters[1],
                    chapters[2]]
        actual = output.get_chapters_to_be_published(chapters)

        assert actual == expected

    def test_get_chapters_to_be_published_force_publish_false(self):
        output = OutputStub('a', force_publish=False)
        chapters = [Chapter('1', publish=True),
                    Chapter('2', publish=False),
                    Chapter('3')]  # defaults to True

        expected = [chapters[0],
                    chapters[2]]
        actual = output.get_chapters_to_be_published(chapters)

        assert actual == expected

    def test_get_css(self):
        with patch('builtins.open', mock_open(read_data='css')) as mock_file:
            output = HtmlOutput('some.path', css_path='some.css')
            actual = output._get_css()

        expected = 'css'

        assert actual == expected
        mock_file.assert_called_once_with(os.path.join(os.getcwd(), 'some.css'), 'r')

    def test_get_css_returns_empty_str_if_no_css_path(self):
        output = HtmlOutput('some.path')

        expected = ''
        actual = output._get_css()

        assert actual == expected

    def test_make(self):
        output = HtmlOutput('some.path')
        book = Book('title')
        substitution = SimpleSubstitution(old='a', new='b')
        substitutions = [substitution]

        with patch('builtins.open', mock_open(read_data='css'), create=True) as mock_file, \
                patch.object(output, '_get_html_document') as mock_get_html_document, \
                patch.object(output, 'validate') as mock_validate:
            mock_get_html_document.return_value = 'document'
            output.make(book, substitutions)

        mock_get_html_document.assert_called_once_with(book, substitutions)
        mock_file.assert_called_once_with('some.path', 'w')
        mock_file_handle = mock_file()
        mock_file_handle.write.assert_called_once_with('document')
        mock_validate.assert_called_once()

    def test_make_without_substitutions(self):
        output = HtmlOutput('some.path')
        book = Book('title')

        with patch('builtins.open', mock_open(read_data='css'), create=True) as mock_file, \
                patch.object(output, '_get_html_document') as mock_get_html_document, \
                patch.object(output, 'validate') as mock_validate:
            mock_get_html_document.return_value = 'document'
            output.make(book)

        mock_file.assert_called_once_with('some.path', 'w')
        mock_file_handle = mock_file()
        mock_file_handle.write.assert_called_once_with('document')
        mock_validate.assert_called_once()


def test_apply_template():
    title = 'Foo'
    html_content = '<p>Bar</p>'
    css = 'p { font-style: italic }'
    language = 'en'

    expected = TEST_HTML_TEMPLATE.format(
        content=html_content,
        title=title,
        css=css,
        language=language,
        apub_version=apub_version)

    actual = _apply_template(
        html_content=html_content,
        title=title,
        css=css,
        language=language)

    assert actual == expected


def test_yield_attributes_as_params_from_dict():
    attributes = {attribute: attribute
                  for attribute in SUPPORTED_EBOOKCONVERT_ATTRIBUTES}

    expected = [f'--{attribute}={attribute}'
                for attribute in SUPPORTED_EBOOKCONVERT_ATTRIBUTES]
    actual = list(_yield_attributes_as_params(attributes))

    assert actual == expected


def test_yield_attributes_as_params_from_dict_omits_unsupported():
    attributes = {attribute: attribute
                  for attribute in SUPPORTED_EBOOKCONVERT_ATTRIBUTES}
    attributes['unsupported'] = 'unsupported'

    expected = [f'--{attribute}={attribute}'
                for attribute in SUPPORTED_EBOOKCONVERT_ATTRIBUTES]
    actual = list(_yield_attributes_as_params(attributes))

    assert actual == expected


def test_yield_attributes_as_params_from_object():
    object_ = get_test_book()

    expected = [f'--{attribute}={attribute}'
                for attribute in SUPPORTED_EBOOKCONVERT_ATTRIBUTES]
    actual = list(_yield_attributes_as_params(object_))

    assert actual == expected


def test_yield_attributes_as_params_from_object_omits_unsupported():
    object_ = get_test_book()
    object_.unsupported = 'unsupported'

    expected = [f'--{attribute}={attribute}'
                for attribute in SUPPORTED_EBOOKCONVERT_ATTRIBUTES]
    actual = list(_yield_attributes_as_params(object_))

    assert actual == expected


def test_yield_attributes_as_params_from_dict_missing_supported_attribute_omits_attribute():
    attributes = {attribute: attribute
                  for attribute in SUPPORTED_EBOOKCONVERT_ATTRIBUTES[:-1]}

    expected = [f'--{attribute}={attribute}'
                for attribute in SUPPORTED_EBOOKCONVERT_ATTRIBUTES[:-1]]
    actual = list(_yield_attributes_as_params(attributes))

    assert actual == expected


def test_yield_attributes_as_params_value_none_omits_attribute():
    attributes = {attribute: attribute
                  for attribute in SUPPORTED_EBOOKCONVERT_ATTRIBUTES[:-1]}
    attributes[SUPPORTED_EBOOKCONVERT_ATTRIBUTES[-1]] = None

    expected = [f'--{attribute}={attribute}'
                for attribute in SUPPORTED_EBOOKCONVERT_ATTRIBUTES[:-1]]
    actual = list(_yield_attributes_as_params(attributes))

    assert actual == expected
