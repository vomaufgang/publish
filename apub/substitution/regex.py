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


from .substitution import Substitution


class RegexSubstitution(Substitution):
    def apply_to(self, text):
        # todo implement RegexSubstitution.apply_to
        raise NotImplementedError

    @classmethod
    def from_dict(cls, dict_):
        regex_substitution = RegexSubstitution()

        # todo move away from this generic solution and set + validate
        #      required fields instead

        for k, v in dict_.items():
            setattr(regex_substitution, k, v)

        return regex_substitution
