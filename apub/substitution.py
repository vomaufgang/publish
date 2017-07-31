#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# apub - Python package with cli to turn markdown files into ebooks
# Copyright (c) 2014 Christopher Knörndel
#
# Distributed under the MIT License
# (license terms are at http://opensource.org/licenses/MIT).

import logging.config
from abc import ABCMeta, abstractmethod
from typing import Iterable

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


# todo module docstring
# todo consolidate all examples in module docstring

class Substitution(metaclass=ABCMeta):
    """The Substitution class acts as an abstract interface for future
    substitution implementations.

    In order for a substitution to be executable by an output class,
    it must offer the apply_to method described below.
    """
    # todo write unit tests

    @abstractmethod
    def apply_to(self, text: str) -> str:
        """Applies the substitution to the text, returning the changed text.

        :param text: The text to apply this simple substitution to.

        :returns: The changed text.
        """
        raise NotImplementedError


class SimpleSubstitution(Substitution):
    """The SimpleSubstitution allows for simple text replacements.

    Substitutions are always applied to all chapters when calling
    `*Output.make(book, substitutions)`.

    :ivar find: The string to find.
    :type find: str
    :ivar replace_with: The string to replace the find string with.
    :type replace_with: str

    :Example:

        .. code-block:: python

            book = Book()
            book.chapters.append(Chapter(source='example.md'))

            substitution = SimpleSubstitution(find='Cow', replace_with='World')

            HtmlOutput(path='example.html').make(book, [substitution])

        Content of example.md:

        .. code-block:: md

            # Hello Cow!

        This leads to the following output in example.html (shortened):

        .. code-block:: html

            <h1>Hello World!</h1>

    """

    def __init__(self, find: str=None, replace_with: str=None):
        super().__init__()
        self.find = find
        self.replace_with = replace_with

    def apply_to(self, text: str) -> str:
        """Applies the substitution to the text, returning the changed text.

        :param text: The text to apply this simple substitution to.
        :type text: str

        :returns: The changed text.
        :rtype: str
        """
        return text.replace(self.find, self.replace_with)


def apply_substitutions(
        markdown_: str,
        substitutions: Iterable[Substitution]) -> str:
    """Applies the list of substitutions to the markdown content.

    :param markdown_: The markdown content of the chapter.
    :param substitutions: The list of substitutions to be applied.

    :returns: The dict of markdown strings by chapter with
        the substitutions applied.
    """
    if substitutions:
        log.info('Applying substitutions ...')

    substitution_count = len(list(substitutions))

    for index, substitution in enumerate(substitutions):
        markdown_ = substitution.apply_to(markdown_)
        log.info(f'{index + 1} of {substitution_count} applied')

    return markdown_
