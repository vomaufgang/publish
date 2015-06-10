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

class Anonymous(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs

class JsonOutput(Output):
    def __init__(self):
        super().__init__()
        self.compress_content = False
        self.__lzstring = None
        # todo: the resulting json contains a field "is_compressed: value"
        #   to indicate wether areader has to decompress the html contents
        #   before passing them to monocle

    @property
    def lzstring(self):
        if not self.__lzstring:
            self.__lzstring = LZString()
        return self.__lzstring

    def make(self, metadata, chapters, substitutions):
        """

        :param metadata:
        :type metadata: dict
        :param chapters:
        :type chapters: list[apub.metadata.chapter.Chapter]
        :param substitutions:
        :type substitutions: list[apub.substitution.substitution.Substitution]
        :return:
        """
        # todo implement JsonOutput.make

        chapter_array = []

        if not self.force_publish:
            chapters = [chapter
                        for chapter in chapters
                        if chapter.publish]

        for chapter in chapters:
            content = _Html.from_chapter(chapter)

            if self.compress_content:
                content = self.lzstring.compressToBase64(content)
            else:
                pass

            chapter_dict = {
                'title': chapter.title,
                'url_friendly_title': chapter.url_friendly_title,
                'is_compressed': self.compress_content,
                'content': content
            }

            chapter_array.append(chapter_dict)
            pass

        raise NotImplementedError

    @classmethod
    def from_dict(cls, dict_):
        json_output = JsonOutput()

        # todo move away from this generic solution and set + validate required fields instead

        for k, v in dict_.items():
            setattr(json_output, k, v)

        return json_output
