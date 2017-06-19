#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# apub - Python package with cli to turn markdown files into ebooks
# Copyright (C) 2015  Christopher Knörndel
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from abc import ABCMeta, abstractmethod

import logging.config
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
    def apply_to(self, text):
        """Applies the substitution to the text, returning the changed text.

        :param text: The text to apply this simple substitution to.
        :type text: str

        :returns: The changed text.
        :rtype: str
        """
        raise NotImplementedError


class RegexSubstitution(Substitution):
    """Planned for Version 3.0
    """
    def __init__(self):
        super().__init__()
        raise NotImplementedError("Planned for Version 3.0")

    def apply_to(self, text):
        raise NotImplementedError("Planned for Version 3.0")


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

        .. code-block:: markdown

            # Hello Cow!

        This leads to the following output in example.html (shortened):

        .. code-block:: html

            <h1>Hello World!</h1>

    """

    def __init__(self, find=None, replace_with=None):
        super().__init__()
        self.find = find
        self.replace_with = replace_with

    def apply_to(self, text):
        """Applies the substitution to the text, returning the changed text.

        :param text: The text to apply this simple substitution to.
        :type text: str

        :returns: The changed text.
        :rtype: str
        """
        return text.replace(self.find, self.replace_with)
