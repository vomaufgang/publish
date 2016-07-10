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
from .html import HtmlOutput
from ..lzstring import LZString


class JsonOutput(Output):
    """

    """

    def __init__(self):
        super().__init__()
        self.compress_content = False
        # todo: the resulting json contains a field "is_compressed: value"
        #   to indicate wether areader has to decompress the html contents
        #   before passing them to monocle

    def make(self, book, substitutions):
        json_ = self._get_json(book, substitutions)
        self._write(json_)

    def _get_json(self, book, substitutions):
        metadata = book.metadata

        # todo cli command that recommends unique slugs for chapters based on
        #      sanitized and uniqueified chapter titles

        # todo output_path  of JsonOutput will be interpreted as a
        #      directory name because JsonOutput writes more than one file

        # v outputs to [url_friendly_title].json with instructions to add
        #   this to stories.json of areader
        example_json_metadata = {
            'aus [url_friendly_title]': {
                'title': 'AUS',
                'subtitle': 'vom Auf- und Untergang der Sterne',
                'lastUpdated'
                'etc': None
            }
        }

        # v outputs to [url_friendly_title]_chapters.json
        example_json_chapters = {
            'hunger [url_friendly_title]': {
                'content': 'content [maybe encrypted, maybe not]',
                'compressed': True  # or maybe not
            }
        }


        # todo metadata -> attributes
        # todo calculate word count?
        json_ = metadata.copy()
        json_['chapters'] = []

        lzstring = LZString()

        chapters_html = HtmlOutput.get_chapters_html(book, substitutions)

        for chapter in chapters_html:
            if not chapter.publish and not self.force_publish:
                continue

            if self.compress_content:
                content = lzstring.compressToUTF16(chapters_html[chapter])
            else:
                content = chapters_html[chapter]

            chapter_dict = {
                'title': chapter.title,
                'url_friendly_title': chapter.url_friendly_title,
                'content': content,
                'is_compressed': self.compress_content
            }

            json_['chapters'].append(chapter_dict)

        return json.dumps(json_)

    def _write(self, json_output):
        with open(self.path, 'w') as file:
            file.write(json_output)

    @classmethod
    def from_dict(cls, dict_):
        json_output = JsonOutput()

        # todo move away from this generic solution and set + validate
        #      required fields instead

        for k, v in dict_.items():
            setattr(json_output, k, v)

        return json_output
