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

# todo: Use for all input classes
# todo: docstrings

from abc import ABCMeta, abstractmethod


class FromDict(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def from_dict(cls, dict_):
        raise NotImplementedError

    @classmethod
    def get_attribute_from_dict(cls, attribute_name, dict_, default=None):
        if attribute_name not in dict_:
            return default
        return dict_['attribute']
