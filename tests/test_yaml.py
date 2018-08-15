#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# apub - Python package with cli to turn markdown files into ebooks
# Copyright (c) 2014 Christopher Knörndel
#
# Distributed under the MIT License
# (license terms are at http://opensource.org/licenses/MIT).

"""Tests for `apub.yaml` module.
"""

# pylint: disable=missing-docstring,no-self-use,invalid-name,protected-access
from apub.book import Book
# noinspection PyProtectedMember
from apub.yaml import (load_yaml, _load_book)


# todo: split huge yaml unit test into multiple unit tests testing one section each

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
  default:
    - --level1-toc=//h:h1
    - --level2-toc=//h:h2
    - --change-justification=left
  mobi:
    - --mobi-file-type=both

stylesheet: style.css

outputs:
  - type: html
    output: example.html
  - type: ebook
    output: example.epub
  - type: ebook
    output: example.mobi
    ebookconvert_params:
      - default
      - mobi
  - type: ebook
    output: overridden_stylesheet.epub
    stylesheet: overridden.css
"""


def test_load_yaml():
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
        'ebookconvert_params': {
            'default': [
                '--level1-toc=//h:h1',
                '--level2-toc=//h:h2',
                '--change-justification=left',
            ],
            'mobi': [
                '--mobi-file-type=both',
            ],
        },
        'stylesheet': 'style.css',
        'outputs': [
            {
                'type': 'html',
                'output': 'example.html',
            },
            {
                'type': 'ebook',
                'output': 'example.epub',
            },
            {
                'type': 'ebook',
                'output': 'example.mobi',
                'ebookconvert_params': [
                    'default',
                    'mobi',
                ]
            },
            {
                'type': 'ebook',
                'output': 'overridden_stylesheet.epub',
                'stylesheet': 'overridden.css',
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
