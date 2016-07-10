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


class Substitution(FromDict, metaclass=ABCMeta):

    @abstractmethod
    def apply_to(self, text):
        """
        Args:
            text (str): The text to apply this simple substitution to.

        Notes:
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
            from apub.substitution.simple import SimpleSubstitution
            return SimpleSubstitution.from_dict(dict_)

        elif substitution_type == 'regex':
            from apub.substitution.regex import RegexSubstitution
            return RegexSubstitution.from_dict(dict_)

        raise NotImplementedError(
            'Unrecognized substitution type: {0}'.format(substitution_type))
