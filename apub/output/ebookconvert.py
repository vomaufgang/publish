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
from tempfile import mkstemp

from .output import Output
from .html import HtmlOutput


justifications = ['original', 'left', 'justify', 'right']


class EbookConvertOutput(Output):

    def __init__(self, output_path=None, ebookconvert_params=None,
                 css_path=None):
        super().__init__(output_path)
        self.__change_justification = 'original'
        self.__css_path = css_path
        self.__output_path = output_path
        self.__ebookconvert_params = ebookconvert_params

    def make(self, project):
        if self.output_path is None:
            raise AttributeError("output_path of EpubOutput must not be None")

        temp_file = mkstemp(suffix=".html")
        HtmlOutput(
            output_path=self.output_path,
            output_range="todo",
            css_path=self.__css_path
        ).make()
        # todo call ebook-convert
        os.remove(temp_file)
        pass

    @staticmethod
    def from_dict(dict_):
        ebook_convert_output = EbookConvertOutput()

        for k, v in dict_:
            setattr(ebook_convert_output, k, v)

        return ebook_convert_output
