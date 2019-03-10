#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# anited. publish - Python package with cli to turn markdown files into ebooks
# Copyright (c) 2014 Christopher Knörndel
#
# Distributed under the MIT License
# (license terms are at http://opensource.org/licenses/MIT).

"""Load anited. publish projects from yaml strings.
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
    """Loads a yaml string into a Python dictionary.

    Args:
        yaml: The yaml string.

    Returns:
        The yaml structure as a Python dictionary.
    """
    return YAML.load(yaml)


def load_project(yaml: str) -> Tuple[Book,
                                     Iterable[Substitution],
                                     Iterable[Union[HtmlOutput, EbookConvertOutput]]]:
    """Loads a yaml string using the anited. publish project structure and returns the
    components of the project as a tuple: the book, the substitutions and the outputs.

    A book is always returned. Any properties of the book class not set in the yaml will be
    left at their default values as defined in the book class.

    If the yaml string does not contain any substitutions or outputs, empty lists are returned
    in their place.

    Args:
        yaml: The yaml string.

    Returns:
        A tuple consisting of the book, the list of substitutions and the list of outputs.
    """
    dict_ = load_yaml(yaml)

    book = _load_book(dict_)
    book.chapters.extend(_load_chapters(dict_['chapters']))
    substitutions = list(_load_substitutions(dict_))

    return book, substitutions, []


def _load_book(dict_: Dict) -> Book:
    """Translates a dictionary into a book object. Dictionary keys and values are mapped to
    corresponding book properties of the same name.

    Dictionary keys that have no corresponding properties are omitted.

    Args:
        dict_: The dictionary.

    Returns:
        The book.
    """
    book = Book(**dict_)

    return book


def _load_chapters(dict_: Dict) -> Iterable[Chapter]:
    """Translates a dictionary into a list of chapter objects.

    The dictionary is assumed to have the following structure::

        {
            'chapters': [{ 'src': 'some_file.md' },
                         { 'src': '...' }]
        }

    If the key 'chapters' is not present in the dictionary or if there are no chapter
    sub-dictionaries, an empty list is returned instead.

    Args:
        dict_: The dictionary.

    Returns:
        The list of chapter objects or an empty list either if not chapter sub-dictionaries are
        present in the encapsulating dictionary or if the 'chapters' key itself is missing.
    """
    chapters = []

    if 'chapters' in dict_ and dict_['chapters']:
        for chapter in dict_['chapters']:
            chapters.append(Chapter(**chapter))

    return chapters


def _load_substitutions(dict_: Dict) -> Iterable[Substitution]:
    """Translates a dictionary into a list of substitution objects.

    The dictionary is assumed to have the following structure::

        {
            'substitutions': [{ 'old': 'some', 'new': 'text' },
                              { 'pattern: '...', 'replace_with': '...' }]
        }

    If the key 'substitutions' is not present in the dictionary or if there are no substitution
    sub-dictionaries, an empty list is returned instead.

    The type of the substitution is inferred from the key names of the individual sub-dictionary.
    The keys 'old' and 'new' will lead to the creation of a SimpleSubstitution and so on. Note that
    the key names must match exactly. The keys 'old' and 'replace_with' inside the same
    sub-dictionary will lead to a TypeError, because no Substitution class matches those property
    names.

    Args:
        dict_: The dictionary.

    Returns:
        The list of chapter objects or an empty list either if not chapter sub-dictionaries are
        present in the encapsulating dictionary or if the 'chapters' key itself is missing.

    Raises:
        TypeError: If the key names of a substitution dictionary don't match any Substitution
            class implementation.
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
    """Translates a dictionary into a list of output objects.

    The dictionary is assumed to have the following structure::

        {
            'outputs': [{ 'path': 'some', 'new': 'text' },
                        { 'path: '...', 'replace_with': '...' }]
        }

    If the key 'outputs' is not present in the dictionary or if there are no output
    sub-dictionaries, an empty list is returned instead.

    The type of the output is inferred from the file name provided as a value of the 'path' key
    of the output sub-dictionary.

    A file name ending in the file type '.html' will produce an HtmlOutput. '.epub', '.mobi' or
    any other file type excluding '.html' will produce an EbookConvertOutput.

    Note that a local stylesheet *replaces* the global stylesheet, but local ebookconvert_params
    are *added* to the global ebookconvert_params if present.

    Args:
        dict_: The dictionary.

    Returns:
        The list of output objects or an empty list either if not output sub-dictionaries are
        present in the encapsulating dictionary or if the 'outputs' key itself is missing.
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
                output['ebookconvert_params'] = global_ec_params + local_ec_params
            else:
                output['ebookconvert_params'] = global_ec_params

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
