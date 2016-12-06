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

import os

from apub.substitution.substitution import Substitution

import logging.config
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class SimpleSubstitution(Substitution):
    # todo write unit tests
    def __init__(self):
        self.find = ''
        self.replace_with = ''

    def apply_to(self, text):
        """
        Args:
            text (str): The text to apply this simple substitution to.

        Notes:
            The current implementation schema of apply_to might prove
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

        return os.linesep.join(altered_lines)

    @classmethod
    def from_dict(cls, dict_):
        simple_substitution = SimpleSubstitution()

        simple_substitution.find = cls.get_value_from_dict(
            'find', dict_, default='')
        simple_substitution.replace_with = cls.get_value_from_dict(
            'replace_with', dict_, default='')

        return simple_substitution
