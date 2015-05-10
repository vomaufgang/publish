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
import subprocess
from tempfile import mkstemp

from .output import Output
from .html import HtmlOutput


class EbookConvertOutput(Output):

    def __init__(self):
        super().__init__()
        self.ebookconvert_params = []

    def make(self, metadata, chapters, substitutions):
        (temp_handle, temp_path) = mkstemp(suffix=".html")
        try:
            self._make_html(temp_path, metadata, chapters, substitutions)

            call_params = [
                'ebook-convert',
                temp_path,
                self.path
            ]

            custom_params = _dict_to_param_array(self.ebookconvert_params)

            call_params.extend(custom_params)

            subprocess.call(call_params)
        finally:
            os.remove(temp_path)

    def _make_html(self, temp_path, metadata, chapters, substitutions):
        html_output = HtmlOutput()

        html_output.path = temp_path
        html_output.css = self.css
        html_output.force_publish = self.force_publish

        html_output.single_file = True

        html_output.make(metadata, chapters, substitutions)

    @staticmethod
    def from_dict(dict_):
        ebook_convert_output = EbookConvertOutput()

        # todo move away from this generic solution and set + validate required fields instead

        for k, v in dict_.items():
            setattr(ebook_convert_output, k, v)

        return ebook_convert_output


def _dict_to_param_array(dict_):
    param_array = []

    for k, v in dict_:
        param_array.append("--{0}={1}".format(k, v))

    return param_array
