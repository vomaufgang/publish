#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# apub - Python package with cli to turn markdown files into ebooks
# Copyright (c) 2014 Christopher Knörndel
#
# Distributed under the MIT License
# (license terms are at http://opensource.org/licenses/MIT).

"""This module defines substitution classes that can be passed to the output classes in
apub.output to apply text substitutions to the markdown content before it is rendered to html
or epub.
"""

# pylint: disable=too-few-public-methods,anomalous-backslash-in-string

import logging.config
import re
from abc import ABCMeta, abstractmethod
from typing import Iterable, Union

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class Substitution(metaclass=ABCMeta):
    """The Substitution class acts as an abstract interface for future
    substitution implementations.

    In order for a substitution to be executable by an output class,
    it must offer the apply_to method described below.
    """

    @abstractmethod
    def apply_to(self, text: str) -> str:
        """Applies the substitution to the text, returning the changed text.

        Args:
            text: The text to apply this simple substitution to.

        Returns:
            The changed text.
        """
        pass  # pragma: no cover


class SimpleSubstitution(Substitution):
    """The SimpleSubstitution allows for simple text replacements.

    Substitutions are always applied to all chapters when calling
    `*Output.make(book, substitutions)`.

    Attributes:
        old (str): The string to find.
        new (str): The string to replace the find string with.

    Examples:

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

    def __init__(self, old: str, new: str):
        """Initializes a new instance of the :class:`SimpleSubstitution` class.
        """
        super().__init__()
        self.old = old
        self.new = new

    def apply_to(self, text: str) -> str:
        """Applies the substitution to the text, returning the changed text.

        Args:
            text: The text to apply this simple substitution to.

        Returns:
            The changed text.
        """
        return text.replace(self.old, self.new)


class RegexSubstitution(Substitution):
    """The RegexSubstitution allows you to use regular expressions to make
    text replacements.

    Substitutions are always applied to all chapters when calling
    `*Output.make(book, substitutions)`.

    Args:
        pattern: The search pattern.
        replace_with: The string to replace the pattern with. If the regular expression
            uses groups to only replace part of the expression use standard python regex
            syntax to denote these groups, i.e. \1, \2 and so on.

            See the documentation of the python re package for more information.

    Examples:

        .. code-block:: python

            book = Book()
            book.chapters.append(Chapter(source='example.md'))

            substitution = RegexSubstitution(pattern=r'\+\+(.*?)\+\+',
                                             replace_with='<span class="hello">\1</span>')

            HtmlOutput(path='example.html').make(book, [substitution])

        Content of example.md:

        .. code-block:: md

            ++World!++

        This leads to the following output in example.html (shortened):

        .. code-block:: html

            <span class="hello">World!</span>

    """

    def __init__(self, pattern: Union[bytes, str],
                 replace_with: Union[bytes, str]):
        self.regular_expression = re.compile(pattern)
        self.replace_with = replace_with

    def apply_to(self, text: str):
        """Applies the substitution to the text, returning the changed text.

        Args:
            text: The text to apply this simple substitution to.

        Returns:
            The changed text.
        """
        return self.regular_expression.sub(self.replace_with, text)


def apply_substitutions(
        text: str,
        substitutions: Iterable[Substitution]) -> str:
    """Applies the list of substitutions to the markdown content.

    Args:
        text: The text to apply the substitutions to.
        substitutions: The list of substitutions to be applied.

    Returns:
        The changed text.
    """
    text = str(text)

    if substitutions:
        log.info('Applying substitutions ...')

    substitution_count = len(list(substitutions))

    for index, substitution in enumerate(substitutions):
        text = substitution.apply_to(text)
        log.info(f'{index + 1} of {substitution_count} applied')

    return text
