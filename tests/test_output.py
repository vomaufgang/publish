#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# apub - Python package with cli to turn markdown files into ebooks
# Copyright (c) 2014 Christopher Knörndel
#
# Distributed under the MIT License
# (license terms are at http://opensource.org/licenses/MIT).

import pytest

from apub import __version__ as apub_version
from apub.output import (SUPPORTED_EBOOKCONVERT_ATTRS,
                         _apply_template)


def test_supported_ebookconvert_attrs():
    assert len(SUPPORTED_EBOOKCONVERT_ATTRS) == 14
    assert 'author_sort' in SUPPORTED_EBOOKCONVERT_ATTRS
    assert 'authors' in SUPPORTED_EBOOKCONVERT_ATTRS
    assert 'book_producer' in SUPPORTED_EBOOKCONVERT_ATTRS
    assert 'comments' in SUPPORTED_EBOOKCONVERT_ATTRS
    assert 'cover' in SUPPORTED_EBOOKCONVERT_ATTRS
    assert 'isbn' in SUPPORTED_EBOOKCONVERT_ATTRS
    assert 'language' in SUPPORTED_EBOOKCONVERT_ATTRS
    assert 'pubdate' in SUPPORTED_EBOOKCONVERT_ATTRS
    assert 'publisher' in SUPPORTED_EBOOKCONVERT_ATTRS
    assert 'rating' in SUPPORTED_EBOOKCONVERT_ATTRS
    assert 'series' in SUPPORTED_EBOOKCONVERT_ATTRS
    assert 'series_index' in SUPPORTED_EBOOKCONVERT_ATTRS
    assert 'tags' in SUPPORTED_EBOOKCONVERT_ATTRS
    assert 'title' in SUPPORTED_EBOOKCONVERT_ATTRS


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


# noinspection PyArgumentList
def test_apply_template_args():
    with pytest.raises(TypeError):
        _apply_template(title=None,
                        css=None,
                        language=None)
    with pytest.raises(TypeError):
        _apply_template(html_content=None,
                        css=None,
                        language=None)
    with pytest.raises(TypeError):
        _apply_template(html_content=None,
                        title=None,
                        language=None)
    with pytest.raises(TypeError):
        _apply_template(html_content=None,
                        title=None,
                        css=None)
