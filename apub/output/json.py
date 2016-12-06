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

# json outputs two files: The file specified n path and a second file
# filename.pubdate.json which the webreader uses to determine wether
# the contents where changed and an update is in order.
# This keeps the data that gets transfered during a update check to a minimum.

from .output import Output


class JsonOutput(Output):

    def __init__(self):
        super().__init__()
        raise NotImplementedError('Planned for Version 3.0')

    def make(self, book, substitutions):
        raise NotImplementedError('Planned for Version 3.0')

    @classmethod
    def from_dict(cls, dict_):
        raise NotImplementedError('Planned for Version 3.0')
