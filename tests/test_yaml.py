#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# anited. publish - Python package with cli to turn markdown files into ebooks
# Copyright (c) 2014 Christopher Knörndel
#
# Distributed under the MIT License
# (license terms are at http://opensource.org/licenses/MIT).

"""Tests for `publish.yaml` module.
"""

# pylint: disable=missing-docstring,no-self-use,invalid-name,protected-access
# pylint: disable=too-few-public-methods
import pytest

from publish.output import HtmlOutput, EbookConvertOutput
from publish.book import Book, Chapter
# noinspection PyProtectedMember
from publish.yaml import (load_yaml, _load_book, _load_chapters, _load_ebookconvert_params,
                          _load_outputs)


BOOK_SECTION = r"""
title: My book
author: Max Mustermann
language: en
"""

CHAPTER_SECTION = r"""
chapters:
  - src: first_chapter.md
  - src: second_chapter.md
  - src: unfinished_chapter.md
    publish: False
"""

SUBSTITUTION_SECTION = r"""
substitutions:
  - old: Some
    new: Thing
  - pattern: \+\+(?P<text>.*?)\+\+
    replace_with: <span class="small-caps">\g<text></span>
"""

OUTPUT_SECTION = r"""
ebookconvert_params:
  - level1-toc=//h:h1
  - change-justification=left
  - page-breaks-before=//*[(name()='h1' or name()='h2') or 
    (name()='div' and @class='page-break')]

stylesheet: style.css

outputs:
  - path: example.html
  - path: example.epub
  - path: example.mobi
    ebookconvert_params:
      - preserve-cover-aspect-ratio
  - path: replacement_stylesheet.epub
    stylesheet: replacement.css
"""  # noqa: W291


def test_load_book():
    """todo: add missing book metadata to test yaml
    """
    yaml = BOOK_SECTION

    expected = Book(title='My book',
                    author='Max Mustermann',
                    language='en')

    actual = _load_book(load_yaml(yaml))

    assert actual.__dict__ == expected.__dict__


def test_load_book_omits_unknown_attribute():
    yaml = r"""
title: My book
author: Max Mustermann
language: en
unknown_attribute: hello
"""

    actual = _load_book(load_yaml(yaml))

    assert 'unknown_attribute' not in actual.__dict__


def test_load_book_title_is_mandatory():
    yaml = r"""
author: Max Mustermann
language: en
unknown_attribute: hello
"""
    with pytest.raises(TypeError, match=r'missing 1 required positional argument: \'title\''):
        _load_book(load_yaml(yaml))


def test_load_chapters():
    yaml = CHAPTER_SECTION

    expected = [Chapter(src='first_chapter.md'),
                Chapter(src='second_chapter.md'),
                Chapter(src='unfinished_chapter.md',
                        publish=False)]
    actual = list(_load_chapters(load_yaml(yaml)))

    assert len(actual) == len(expected)
    assert actual[0].__dict__ == expected[0].__dict__
    assert actual[1].__dict__ == expected[1].__dict__
    assert actual[2].__dict__ == expected[2].__dict__


def test_load_ebookconvert_params():
    yaml = OUTPUT_SECTION

    expected = ['--level1-toc=//h:h1',
                '--change-justification=left',
                '{}{}'.format("--page-breaks-before=//*[(name()='h1' or name()='h2') or ",
                              "(name()='div' and @class='page-break')]")]

    actual = _load_ebookconvert_params(load_yaml(yaml))

    assert actual == expected


def test_load_ebookconvert_params_prepends_missing_double_minus():
    yaml = r"""
ebookconvert_params:
  - level1-toc=//h:h1
  - change-justification=left
  - --page-breaks-before=//*[(name()='h1' or name()='h2') or 
    (name()='div' and @class='page-break')]"""  # noqa: W291

    expected = ['--level1-toc=//h:h1',
                '--change-justification=left',
                ''.join(["--page-breaks-before=//*[(name()='h1' or name()='h2') or ",
                         "(name()='div' and @class='page-break')]"])]

    actual = _load_ebookconvert_params(load_yaml(yaml))

    assert actual == expected


def test_load_ebookconvert_params_strips_whitespace():
    yaml = r"""
ebookconvert_params:
  -  level1-toc=//h:h1
  -  --level2-toc=//h:h1
  - change-justification=left """

    expected = ['--level1-toc=//h:h1',
                '--level2-toc=//h:h1',
                '--change-justification=left']

    actual = _load_ebookconvert_params(load_yaml(yaml))

    assert actual == expected


def test_load_outputs_uses_html_output_for_html_file_ending():
    # todo global stylesheet & ebookconvert_params
    yaml = """
outputs:
  - path: example.html"""

    expected = [
        HtmlOutput(path='example.html'),
    ]

    actual = list(_load_outputs(load_yaml(yaml)))

    assert len(actual) == len(expected)
    assert actual[0].__dict__ == expected[0].__dict__


def test_load_outputs_uses_ebookconvert_output_for_all_other_file_endings():
    # todo global stylesheet & ebookconvert_params
    yaml = """
outputs:
  - path: example.epub
  - path: example.mobi
  - path: example.whatever"""

    expected = [
        EbookConvertOutput(path='example.epub'),
        EbookConvertOutput(path='example.mobi'),
        EbookConvertOutput(path='example.whatever'),
    ]

    actual = list(_load_outputs(load_yaml(yaml)))

    assert len(actual) == len(expected)
    assert actual[0].__dict__ == expected[0].__dict__
    assert actual[1].__dict__ == expected[1].__dict__
    assert actual[2].__dict__ == expected[2].__dict__


def test_load_outputs_loads_mixed_outputs():
    # todo global stylesheet & ebookconvert_params
    yaml = """
outputs:
  - path: example.html
  - path: example.epub"""

    expected = [
        HtmlOutput(path='example.html'),
        EbookConvertOutput(path='example.epub'),
    ]

    actual = list(_load_outputs(load_yaml(yaml)))

    assert len(actual) == len(expected)
    assert actual[0].__dict__ == expected[0].__dict__
    assert actual[1].__dict__ == expected[1].__dict__


def test_load_outputs_uses_global_stylesheet_when_no_local_present():
    yaml = """
    stylesheet: global.css
    
    outputs:
      - path: global.epub"""

    expected = [
        EbookConvertOutput(path='global.epub', stylesheet='global.css'),
    ]

    actual = list(_load_outputs(load_yaml(yaml)))

    assert len(actual) == len(expected)
    assert actual[0].__dict__ == expected[0].__dict__


def test_load_outputs_uses_local_stylesheet_when_no_global_present():
    yaml = """
    outputs:
      - path: local.epub
        stylesheet: local.css"""

    expected = [
        EbookConvertOutput(path='local.epub', stylesheet='local.css'),
    ]

    actual = list(_load_outputs(load_yaml(yaml)))

    assert len(actual) == len(expected)
    assert actual[0].__dict__ == expected[0].__dict__


def test_load_outputs_uses_local_stylesheet_when_both_present():
    yaml = """
    stylesheet: global.css
    
    outputs:
      - path: local.epub
        stylesheet: local.css"""

    expected = [
        EbookConvertOutput(path='local.epub', stylesheet='local.css'),
    ]

    actual = list(_load_outputs(load_yaml(yaml)))

    assert len(actual) == len(expected)
    assert actual[0].__dict__ == expected[0].__dict__
