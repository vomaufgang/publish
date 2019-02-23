#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# anited. publish - Python package with cli to turn markdown files into ebooks
# Copyright (c) 2014 Christopher Knörndel
#
# Distributed under the MIT License
# (license terms are at http://opensource.org/licenses/MIT).

""" todo yaml docstring
todo: Make the -- optional for ebookconvert_params, add them automatically when missing
todo: todo _load_outputs
"""
import logging
from typing import Dict, Tuple, Iterable, Union, List

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

    return book, substitutions, []


def _load_book(dict_: Dict) -> Book:
    """todo: docstring _load_book
    """
    book = Book(**dict_)

    return book


def _load_chapters(dict_: Dict) -> Iterable[Chapter]:
    """todo: docstring _load_chapters
    """
    chapters = []

    if 'chapters' in dict_ and dict_['chapters']:
        for chapter in dict_['chapters']:
            chapters.append(Chapter(**chapter))

    return chapters


def _load_substitutions(dict_: Dict) -> Iterable[Substitution]:
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


def _load_outputs(dict_: Dict) -> Iterable[Union[HtmlOutput, EbookConvertOutput]]:
    """todo: implement _load_outputs
    todo: docstring _load_outputs
    todo: document - stylesheet gets replaced, params get merged (local take precedence)
    """
    outputs = []
    global_stylesheet = None
    global_ec_params = []

    if 'stylesheet' in dict_:
        global_stylesheet = dict_['stylesheet']

    if 'ebookconvert_params' in dict_:
        global_ec_params = _load_ebookconvert_params(dict_)

    for output in dict_['outputs']:
        path = output['path']
        file_type = path.split('.')[-1]

        if 'stylesheet' not in output and global_stylesheet:
            output['stylesheet'] = global_stylesheet

        if file_type == 'html':
            outputs.append(HtmlOutput(**output))
        else:
            if 'ebookconvert_params' in output:
                local_ec_params = _load_ebookconvert_params(output)
                output['ebookconvert_params'] = local_ec_params + global_ec_params

            outputs.append(EbookConvertOutput(**output))

    return outputs


def _load_ebookconvert_params(dict_: Dict) -> List[str]:
    """Loads ebookconvert command line parameters from a dictionary.

    Prepends -- to parameters that are missing it, making -- optional within the
    ebookconvert_params block of the project file.

    Args:
        dict_: The dictionary.

    Returns:
        The list of ebookconvert command line parameters.
    """
    ebookconvert_params = []

    if 'ebookconvert_params' not in dict_:
        return ebookconvert_params

    param_list = dict_['ebookconvert_params']

    for param in param_list:
        param = param.strip()
        if param.startswith('--'):
            ebookconvert_params.append(param)
        else:
            ebookconvert_params.append(f'--{param}')

    return ebookconvert_params
