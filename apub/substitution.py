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

from apub.fromdict import FromDict

import logging.config
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


# todo module docstring
# todo consolidate all examples in module docstring

class Substitution(FromDict, metaclass=ABCMeta):
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

    @classmethod
    def from_dict(cls, dict_):
        """Creates a new Substitution object from the provided
        python dictionary.

        The type of the Substitution is inferred from the value assigned to
        the 'type' field of the dictionary.

        The following values are supported as of Version 1.0:

        * `simple` -> `SimpleSubstitution`

        The structure and contents of the dictionary must be equivalent to
        the apub JSON format, specifically the format of the substitution
        specified by the 'type' field of the dictionary.

        :param dict_:
            The dictionary to translate into a SimpleSubstitution object.
        :type dict_: dict

        :returns: A new Substitution created from the dictionary.

        :raises NotImplementedError: The value of 'type' does not equal any
            existing Substitution implementation. See valid types above.

        :Example:

            .. code-block:: python

                dict_ = {
                    'type': 'simple',
                    'find': 'Cow',
                    'replace_with': 'Substitution'
                }

                substitution = Substitution.from_dict(dict_)

                print(substitution)
                # <apub.substitution.SimpleSubstitution object at ...>

        .. note::

            The parameter name is `dict_` with a trailing underscore. See
            docs/readme.rst or index.html of the html documentation for more
            information.


        """
        substitution_type = dict_['type']

        if substitution_type == 'simple':
            return SimpleSubstitution.from_dict(dict_)

        elif substitution_type == 'regex':
            raise NotImplementedError(
                "Substitution type 'regex' is planned for Version 3.0")

        raise NotImplementedError(
            "Unrecognized substitution type: {}".format(substitution_type))


class RegexSubstitution(Substitution):
    """Planned for Version 3.0
    """
    def __init__(self):
        super().__init__()
        raise NotImplementedError("Planned for Version 3.0")

    def apply_to(self, text):
        raise NotImplementedError("Planned for Version 3.0")

    @classmethod
    def from_dict(cls, dict_):
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

    @classmethod
    def from_dict(cls, dict_):
        """Creates a new SimpleSubstitution object from the provided
        python dictionary.

        The structure and contents of the dictionary must be equivalent to
        the apub JSON format, specifically the format for a SimpleSubstitution.

        Properties omitted in the dictionary default to en empty string.

        :param dict_:
            The dictionary to translate into a SimpleSubstitution object.
        :type dict_: dict

        :returns: A new SimpleSubstitution created from the dictionary.
        :rtype: SimpleSubstitution

        .. note::

            The parameter name is `dict_` with a trailing underscore. See
            docs/readme.rst or index.html of the html documentation for more
            information.

        """
        substitution = SimpleSubstitution()

        get_value = cls.get_value_from_dict

        substitution.find = get_value('find', dict_, default='')
        substitution.replace_with = get_value(
            'replace_with', dict_, default='')

        return substitution
