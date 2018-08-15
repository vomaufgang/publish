#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# apub - Python package with cli to turn markdown files into ebooks
# Copyright (c) 2014 Christopher Knörndel
#
# Distributed under the MIT License
# (license terms are at http://opensource.org/licenses/MIT).

""" todo yaml docstring
"""

from typing import Dict, Tuple, Iterable, Union
from ruamel.yaml import YAML

from apub.book import Book, Chapter
from apub.output import HtmlOutput, EbookConvertOutput
from apub.substitution import Substitution

YAML_ = YAML(typ='safe', pure=True)


def load_yaml(yaml: str) -> Dict:
    """todo: docstring load_yaml"""
    return YAML_.load(yaml)


def load_project(yaml: str) -> Tuple[Book,
                                     Iterable[Substitution],
                                     Iterable[Union[HtmlOutput, EbookConvertOutput]]]:
    """todo: docstring load_project"""
    dict_ = load_yaml(yaml)

    book = _load_book(dict_)

    if 'chapters' in dict_:
        chapters = dict_['chapters']
        if chapters:
            book.chapters.extend(_load_chapters(dict_['chapters']))

    return book, [], []


def _load_book(dict_: Dict) -> Book:
    """todo: docstring _load_book"""
    book = Book(**dict_)

    return book


def _load_chapters(list_: Iterable) -> Iterable[Chapter]:
    """todo: docstring _load_chapters
    todo: unit test _load_chapters"""
    if list_:
        for dict_ in list_:
            yield Chapter(**dict_)

    # todo: raise NoChaptersFoundError
