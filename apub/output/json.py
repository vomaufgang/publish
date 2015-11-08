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

import json

from .output import Output
from .html import Html
from ..lzstring import LZString


class JsonOutput(Output):
    def __init__(self):
        super().__init__()
        self.compress_content = False
        # todo: the resulting json contains a field "is_compressed: value"
        #   to indicate wether areader has to decompress the html contents
        #   before passing them to monocle

    def make(self, project):
        json_ = self._generate_json(project)
        self._write(json_)

    def _generate_json(self, project):
        metadata = project.metadata
        chapters = project.chapters

        output = metadata.copy()
        output['chapters'] = []

        if not self.force_publish:
            chapters = [chapter
                        for chapter in chapters
                        if chapter.publish]

        lzstring = LZString()

        for chapter in chapters:
            content = Html.from_chapter(chapter)

            if self.compress_content:
                content = lzstring.compressToUTF16(content)
            else:
                pass

            chapter_dict = {
                'title': chapter.title,
                'url_friendly_title': chapter.url_friendly_title,
                'content': content,
                'is_compressed': self.compress_content
            }

            output['chapters'].append(chapter_dict)

        return json.dumps(output)

    def _write(self, json_output):
        with open(self.path, 'w') as file:
            file.write(json_output)

    @classmethod
    def from_dict(cls, dict_):
        json_output = JsonOutput()




        # todo move away from this generic solution and set + validate required fields instead

        for k, v in dict_.items():
            setattr(json_output, k, v)

        return json_output
