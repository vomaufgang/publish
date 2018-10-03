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
from anited_publish.book import Book
# noinspection PyProtectedMember
from anited_publish.yaml import (load_yaml, _load_book)


# todo: split huge yaml unit test into multiple unit tests testing one section each

# todo: add missing book metadata to test yaml
BOOK_SECTION = r"""
title: title
author: author
language: language
"""

CHAPTER_SECTION = r"""
chapters:
  - src: first_chapter.md
  - src: second_chapter.md
  - src: unfinished_chapter.md
    anited_publish: False
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
    anited_publish: False

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
                'anited_publish': False,
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
    yaml = YAML

    expected = Book(title='My book',
                    author='Max Mustermann',
                    language='en')

    dict_ = load_yaml(yaml)
    actual = _load_book(dict_)

    assert actual.__dict__ == expected.__dict__
