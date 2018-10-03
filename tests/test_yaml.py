#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# anited_publish - Python package with cli to turn markdown files into ebooks
# Copyright (c) 2014 Christopher Knörndel
#
# Distributed under the MIT License
# (license terms are at http://opensource.org/licenses/MIT).

"""Tests for `anited_publish.yaml` module.
"""

# pylint: disable=missing-docstring,no-self-use,invalid-name,protected-access
# pylint: disable=too-few-public-methods
import pytest

from anited_publish.book import Book, Chapter
# noinspection PyProtectedMember
from anited_publish.yaml import (load_yaml, _load_book, _load_chapters)


# todo: split huge yaml unit test into multiple unit tests testing one section each

# todo: add missing book metadata to test yaml
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
  - some other param

stylesheet: style.css

outputs:
  - type: html
    output: example.html
  - type: ebookconvert
    output: example.epub
  - type: ebookconvert
    output: example.mobi
    ebookconvert_params:
      - some additional param
  - type: ebookconvert
    output: additional_stylesheet.epub
    stylesheet: additional.css
"""

YAML = r"""
title: My book
author: Max Mustermann
language: en

chapters:
  - src: first_chapter.md
  - src: second_chapter.md
  - src: unfinished_chapter.md
    publish: False

substitutions:
  - old: Some
    new: Thing
  - pattern: \+\+(?P<text>.*?)\+\+
    replace_with: <span class="small-caps">\g<text></span>

ebookconvert_params:
  - level1-toc=//h:h1
  - level2-toc=//h:h2
  - change-justification=left

stylesheet: style.css

outputs:
  - type: html
    output: example.html
  - type: ebookconvert
    output: example.epub
  - type: ebookconvert
    output: example.mobi
    ebookconvert_params:
      - mobi-file-type=both
  - type: ebookconvert
    output: additional_stylesheet.epub
    stylesheet: additional.css
"""

# todo: Make the -- optional for ebookconvert_params, add them automatically when missing


def test_load_yaml():
    """Integration test."""
    yaml = YAML

    expected = {
        'title': 'My book',
        'author': 'Max Mustermann',
        'language': 'en',
        'chapters': [
            {
                'src': 'first_chapter.md',
            },
            {
                'src': 'second_chapter.md',
            },
            {
                'src': 'unfinished_chapter.md',
                'publish': False,
            },
        ],
        'substitutions': [
            {
                'old': 'Some',
                'new': 'Thing',
            },
            {
                'pattern': r'\+\+(?P<text>.*?)\+\+',
                'replace_with': r'<span class="small-caps">\g<text></span>',
            },
        ],
        'ebookconvert_params': [
            'level1-toc=//h:h1',
            'level2-toc=//h:h2',
            'change-justification=left',
        ],
        'stylesheet': 'style.css',
        'outputs': [
            {
                'type': 'html',
                'output': 'example.html',
            },
            {
                'type': 'ebookconvert',
                'output': 'example.epub',
            },
            {
                'type': 'ebookconvert',
                'output': 'example.mobi',
                'ebookconvert_params': [
                    'mobi-file-type=both',
                ]
            },
            {
                'type': 'ebookconvert',
                'output': 'additional_stylesheet.epub',
                'stylesheet': 'additional.css',
            },
        ]
    }

    actual = load_yaml(yaml)

    assert actual == expected


def test_load_book():
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
        _ = _load_book(load_yaml(yaml))


def test_load_chapters():
    yaml = CHAPTER_SECTION

    expected = [Chapter(src='first_chapter.md'),
                Chapter(src='second_chapter.md'),
                Chapter(src='unfinished_chapter.md',
                        publish=False)]
    actual = _load_chapters(load_yaml(yaml))

    assert len(actual) == len(expected)
    assert actual[0].__dict__ == expected[0].__dict__
    assert actual[1].__dict__ == expected[1].__dict__
    assert actual[2].__dict__ == expected[2].__dict__
