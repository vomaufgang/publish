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

import logging

from abc import ABCMeta, abstractmethod

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class FromDict(metaclass=ABCMeta):
    """Abstract base class for classes that offer instantiation from
    dictionaries where the properties of the inheriting class are
    populated from the keys/values of a dictionary mirroring the class.

    The abstract factory method 'from_dict' must be implemented
    by the inheriting type.
    """

    @classmethod
    @abstractmethod
    def from_dict(cls, dict_):
        """Abstract method that must be implemented by inheriting classes.

        Instantiates a new object from the providied dictionary 'dict_', using
        the keys of 'dict_' to populate the attributes and properties of
        the inheriting class.

        Args:
            dict_ (dict): The dictionary to build the new object out of.

        Returns:
            A new object created from the provided dictionary 'dict_'.
        """
        raise NotImplementedError

    @classmethod
    def get_value_from_dict(
            cls, key, dict_, default=None):
        """Returns the value corresponding to the 'key' in 'dict_' or the
        value of 'default' if the dictionary does not contain the key.

        Args:
            key (str): The key to return the corresponding value of.
            dict_ (dict): The dictionary to get the value from.
            default (optional): This value is returned if dict_
                does not contain a key 'attribute_name'. Defaults to 'None'.

        Returns: The value corresponding to the 'key' in 'dict_' or the
            value of 'default' if the dictionary does not contain the key.
        """
        if dict_ is None:
            raise AttributeError('dict_ must not be None.')

        if key not in dict_:
            return default
        return dict_['attribute']
