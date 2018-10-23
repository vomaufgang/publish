#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# anited. publish - Python package with cli to turn markdown files into ebooks
# Copyright (c) 2014 Christopher Knörndel
#
# Distributed under the MIT License
# (license terms are at http://opensource.org/licenses/MIT).

""" todo yaml docstring
"""

import logging
from typing import Dict, Tuple, Iterable, Union
import ruamel.yaml

from publish.book import Book, Chapter
from publish.output import HtmlOutput, EbookConvertOutput
from publish.substitution import Substitution, SimpleSubstitution, RegexSubstitution

LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())

YAML = ruamel.yaml.YAML(typ='safe', pure=True)


def load_yaml(yaml: str) -> Dict:
    """todo: docstring load_yaml"""
    return YAML.load(yaml)


def load_project(yaml: str) -> Tuple[Book,
                                     Iterable[Substitution],
                                     Iterable[Union[HtmlOutput, EbookConvertOutput]]]:
    """todo: docstring load_project"""
    dict_ = load_yaml(yaml)

    book = _load_book(dict_)
    book.chapters.extend(_load_chapters(dict_['chapters']))
    substitutions = list(_load_substitutions(dict_))
    # todo _load_outputs

    return book, substitutions, []


def _load_book(dict_: Dict) -> Book:
    """todo: docstring _load_book
    """
    book = Book(**dict_)

    return book


def _load_chapters(dict_: Dict):
    """todo: docstring _load_chapters
    """
    chapters = []

    if 'chapters' in dict_ and dict_['chapters']:
        for chapter in dict_['chapters']:
            chapters.append(Chapter(**chapter))

    return chapters


def _load_substitutions(dict_: Dict):
    """todo: docstring _load_substitutions
    """
    substitutions = []

    if 'substitutions' in dict_ and dict_['substitutions']:
        for substitution in dict_['substitutions']:
            if 'old' in substitution and 'new' in substitution:
                substitutions.append(
                    SimpleSubstitution(old=substitution['old'],
                                       new=substitution['new']))
            elif 'pattern' in substitution and 'replace_with' in substitution:
                substitutions.append(
                    RegexSubstitution(pattern=substitution['pattern'],
                                      replace_with=substitution['replace_with']))
            else:
                raise TypeError(
                    f'{list(substitution.keys())} do not match any substitution type.')

    return substitutions
