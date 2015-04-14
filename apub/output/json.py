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
from .html import _Html
from ..lzstring import LZString


class JsonOutput(Output):
    lzstring = LZString()

    def __init__(self):
        super().__init__()
        self.compress = False
        # todo: the resulting json contains a field "compressed: value"
        #   to indicate wether areader has to decompress the html contents
        #   before passing them to monocle

    def make(self, metadata, chapters, substitutions):
        # todo implement JsonOutput.make

        chapter_array = []

        if not self.force_publish:
            chapters = Output.filter_chapters_by_publish(
                chapters,
                publish=True)

        for chapter in chapters:
            uncompressed_content = _Html.from_chapter(chapter)

            if self.compress:
                # todo implement content encryption
                compressed_content = 1
                content = compressed_content
            else:
                content = uncompressed_content

            chapter_dict = {
                'title': chapter.title,
                'url_friendly_title': chapter.url_friendly_title,
                'compressed': self.compress,
                'content': content
            }

            chapter_array.append(chapter_dict)
            pass

        raise NotImplementedError

    @staticmethod
    def compress(content):
        return JsonOutput.lzstring.compressToBase64(content)

    @staticmethod
    def from_dict(dict_):
        json_output = JsonOutput()

        for k, v in dict_:
            setattr(json_output, k, v)

        return json_output
