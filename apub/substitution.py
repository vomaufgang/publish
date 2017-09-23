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

# todo move back to google docstrings, now that the autodoc type hint module works with napoleon.

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
        pass


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

    def __init__(self, old: str=None, new: str=None):
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
