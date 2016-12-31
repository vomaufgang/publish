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


from abc import ABCMeta, abstractmethod

from apub.fromdict import FromDict

import logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler)


class Output(FromDict, metaclass=ABCMeta):
    def __init__(self):
        self.name = None
        self.path = None
        self.css = None
        self.force_publish = False

    @abstractmethod
    def make(self, book, substitutions):
        pass

    @classmethod
    def from_dict(cls, dict_):
        output_type = cls.get_value_from_dict('type', dict_)

        if output_type == 'html':
            from .html import HtmlOutput
            output = HtmlOutput.from_dict(dict_)
        elif output_type == 'json':
            raise NotImplementedError('Output type \'json\' is planned '
                                      'for Version 3.0')
        elif output_type == 'ebook-convert':
            from .ebookconvert import EbookConvertOutput
            output = EbookConvertOutput.from_dict(dict_)
        else:
            raise NotImplementedError(
                'Unrecognized output type: {0}'.format(output_type))

        # todo validate mandatory parameters name & path

        output.name = cls.get_value_from_dict('name', dict_)
        output.path = cls.get_value_from_dict('path', dict_)
        output.css = cls.get_value_from_dict('css', dict_)
        output.force_publish = cls.get_value_from_dict(
            'force_publish', dict_, default=False)

        return output

    @staticmethod
    def filter_chapters_by_publish(chapters, publish=True):
        for chapter in chapters:
            if chapter.publish == publish:
                yield chapter
