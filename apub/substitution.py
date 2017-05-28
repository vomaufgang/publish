#!/usr/bin/env python3
# coding: utf8
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


class Substitution(FromDict, metaclass=ABCMeta):
    # todo write unit tests

    @abstractmethod
    def apply_to(self, text):
        """
        
        :param text: The text to apply this simple substitution to.
        
        .. note::
            The current implementation schema of apply_to might prove
            inefficient, because every single substitution leads to an
            additional iteration the splitted lines of text.

            If this proves true, the implementation should be changed to an
            approach that is based on a single split and a single iteration
            over all lines, diring which all substitutions get applied to a
            line at the same time while retaining the order of application
            defined in the json project.
        """
        raise NotImplementedError

    @classmethod
    def from_dict(cls, dict_):
        substitution_type = dict_['type']

        if substitution_type == 'simple':
            return SimpleSubstitution.from_dict(dict_)

        elif substitution_type == 'regex':
            raise NotImplementedError(
                "Substitution type 'regex' is planned for Version 3.0")

        raise NotImplementedError(
            "Unrecognized substitution type: {}".format(substitution_type))


class RegexSubstitution(Substitution):
    def __init__(self):
        super().__init__()
        raise NotImplementedError("Planned for Version 3.0")

    def apply_to(self, text):
        raise NotImplementedError("Planned for Version 3.0")

    @classmethod
    def from_dict(cls, dict_):
        raise NotImplementedError("Planned for Version 3.0")


class SimpleSubstitution(Substitution):
    """ todo

    :ivar find: todo
    :ivar replace_with: todo
    """

    # todo document SimpleSubstitution
    def __init__(self, find=None, replace_with=None):
        super().__init__()
        self.find = find
        self.replace_with = replace_with

    def apply_to(self, text):
        """ todo

        :param text: The text to apply this simple substitution to.

        .. note:: The current implementation schema of apply_to might prove
            inefficient, because every single substitution leads to an
            additional iteration over the splitted lines of text.

            If this proves true, the implementation should be changed to an
            approach that is based on a single split and a single iteration
            over all lines, diring which all substitutions get applied to a
            line at the same time while retaining the order of application
            defined in the json project.
        """
        lines = text.splitlines()

        altered_lines = [line.replace(self.find, self.replace_with)
                         for line in lines]

        return '\n'.join(altered_lines)

    @classmethod
    def from_dict(cls, dict_):
        simple_substitution = SimpleSubstitution()

        get_value = cls.get_value_from_dict

        simple_substitution.find = get_value('find', dict_)
        simple_substitution.replace_with = get_value('replace_with', dict_)

        return simple_substitution
