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
import markdown
import os
import subprocess
from abc import ABCMeta, abstractmethod
from pkg_resources import resource_string
from tempfile import mkstemp
from typing import List, Dict, Iterable

from apub.book import Book, Chapter
from apub.errors import NoChaptersFoundError
from apub.fromdict import FromDict
from apub.substitution import Substitution

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler)


_supported_ebookconvert_attrs = {
    'ebook-convert': [
        'author_sort',
        'authors',
        'book_producer'
        'comments',
        'cover',
        'isbn',
        'language',
        'pubdate',
        'publisher',
        'rating',
        'series',
        'series_index',
        'tags',
        'title'
    ]
}


# todo: Output has 'css', html_output has 'css_path' - choose one,
#       remove the other

# todo validate mandatory book attributes - are there even any
#      mandatory ones?

# todo optional subtitle, supported by HtmlOutput and JsonOutput

# todo what was generate_toc even for?

class Output(FromDict, metaclass=ABCMeta):
    def __init__(self):
        self.__name = None
        self.__path = None
        self.__css = None
        self.__force_publish = False

    @property
    def name(self) -> str:
        """Gets or sets the output name.
        """
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def path(self) -> str:
        """Gets or sets the output path.
        """
        return self.__path

    @path.setter
    def path(self, value: str):
        self.__path = value

    @property
    def css(self) -> str:
        """Gets or sets the style sheet.
        """
        return self.__css

    @css.setter
    def css(self, value: str):
        self.__css = value

    @property
    def force_publish(self) -> bool:
        """Gets or sets wether to force publish all chapters.
        
        If set to true, all chapters of the book will be published
        no matter how the chapters are configured.
        """
        return self.__force_publish

    @force_publish.setter
    def force_publish(self, value: bool):
        self.__force_publish = value

    @abstractmethod
    def make(self, book: Book, substitutions: List[Substitution]):
        pass

    def get_chapters_to_publish(self, book: Book) -> List[Chapter]:
        if self.force_publish:
            return book.chapters
        else:
            return list(filter(lambda x: x.publish is True, book.chapters))

    @classmethod
    def from_dict(cls, dict_: Dict) -> 'Output':
        output_type = cls.get_value_from_dict('type', dict_)

        if output_type == 'html':
            output = HtmlOutput.from_dict(dict_)
        elif output_type == 'json':
            raise NotImplementedError('Output type \'json\' is planned '
                                      'for Version 3.0')
        elif output_type == 'ebook-convert':
            output = EbookConvertOutput.from_dict(dict_)
        else:
            raise NotImplementedError(
                'Unrecognized output type: {}'.format(output_type))

        # todo validate mandatory parameters name & path

        get_value = cls.get_value_from_dict

        output.name = get_value('name', dict_)
        output.path = get_value('path', dict_)
        output.css = get_value('css', dict_)
        output.force_publish = get_value(
            'force_publish', dict_, default=False)

        return output


class EbookConvertOutput(Output):

    def __init__(self):
        super().__init__()
        self.ebookconvert_params = []

    def make(self,
             book: Book,
             substitutions: List[Substitution] = None):
        if not book:
            raise AttributeError("book must not be None")

        if not substitutions:
            substitutions = []

        (_, temp_path) = mkstemp(suffix=".html")

        try:
            html_output = HtmlOutput()
            html_output.path = temp_path
            html_output.css = self.css
            html_output.force_publish = self.force_publish

            html_output.make(book, substitutions)

            call_params = [
                'ebook-convert',
                temp_path,
                self.path
            ]

            call_params.extend(_yield_attrs_as_ebookconvert_params(book))
            call_params.extend(self.ebookconvert_params)

            subprocess.call(call_params)
        finally:
            os.remove(temp_path)

    @classmethod
    def from_dict(cls, dict_: Dict) -> 'EbookConvertOutput':
        ebook_convert_output = EbookConvertOutput()

        ebook_convert_output.ebookconvert_params = cls.get_value_from_dict(
            'ebookconvert_params', dict_, [])

        return ebook_convert_output


def _yield_attrs_as_ebookconvert_params(object_) -> Iterable[str]:
    """Takes an object and returns a generator yielding all attributes
    that can be processed by the ebookconvert command line as a param array.

    Args:
        object_ (object): An object

    Returns:
        A generator yielding all attributes of the object supported by
        ebookconvert.
    """
    # This way the book can contain attrs not supported by ebookconvert
    # (or any other specific output that follows this explicit pattern)
    for attr_name in _supported_ebookconvert_attrs:
        if hasattr(object_, attr_name):
            attr = str(getattr(object_, attr_name))
            if attr and not attr.isspace():
                yield "--{0}=\"{1}\"".format(attr_name, attr)


class HtmlOutput(Output):
    def __init__(self):
        super().__init__()
        self.__css_path = None
        self.__generate_toc = False  # todo implement HtmlOutput.generate_toc
        #    ^ is dependant upon book & chapter url_friendly_title
        #      for jump links

    @property
    def css_path(self) -> str:
        """Gets or sets the css_path.
        """
        return self.__css_path

    @css_path.setter
    def css_path(self, value: str):
        pass

    @property
    def generate_toc(self) -> bool:
        """Gets or sets the generate_toc.
        """
        return self.__generate_toc

    @generate_toc.setter
    def generate_toc(self, value: bool):
        self.__generate_toc = value

    def make(self,
             book: Book,
             substitutions: List[Substitution] = None):
        if not book:
            raise AttributeError("book must not be None")

        if not substitutions:
            substitutions = []

        html_document = self.get_html_document(book, substitutions)

        with open(self.path, 'w') as file:
            file.write(html_document)

    def get_html_document(self,
                          book: Book,
                          substitutions: List[Substitution]) -> str:

        html_content = self.get_html_content(book, substitutions)
        html_document = self._apply_template(html_content=html_content,
                                             title=book.title,
                                             css=self._get_css(),
                                             language=book.language)

        return html_document

    def get_html_content(self,
                         book: Book,
                         substitutions: List[Substitution]) -> str:
        markdown_ = self._get_markdown_content(book)
        markdown_ = self._apply_substitutions(
            markdown_,
            substitutions)

        return markdown.markdown(markdown_)

    def _apply_template(self,
                        html_content: str,
                        title: str,
                        css: str,
                        language: str) -> str:
        template = resource_string(__name__, 'template.html')

        return template.format(content=html_content,
                               title=title,
                               css=css,
                               language=language)

    def _get_css(self) -> str:
        if not self.css_path:
            return ''

        css_path = os.path.join(os.getcwd(), self.css_path)

        with open(css_path, 'r') as file:
            css = file.read()

        return css if css else ''

    def _get_markdown_content(self, book: Book) -> str:
        markdown_ = []
        md_paragraph_sep = '\n\n'

        if not book.chapters or len(book.chapters) <= 0:
            raise NoChaptersFoundError('Your book contains no chapters that'
                                       'could be published.')

        chapters_to_publish = self.get_chapters_to_publish(book)

        if len(chapters_to_publish) <= 0:
            raise NoChaptersFoundError('None of your chapters are set to be'
                                       'published.')

        for chapter in chapters_to_publish:
            with open(chapter.source, 'r') as file:
                markdown_.append(file.read())

        return md_paragraph_sep.join(markdown_)

    def _apply_substitutions(
            self,
            markdown_: str,
            substitutions: List[Substitution]) -> str:
        """Applies the list of substitutions to the markdown content.

        :param markdown_: The markdown content of the chapter.
        :param substitutions: The list of substitutions to be applied.

        :returns: The dict of markdown strings by chapter with
            the substitutions applied.
        """
        for substitution in substitutions:
            markdown_ = substitution.apply_to(markdown_)

        return markdown_

    @classmethod
    def from_dict(cls, dict_: dict) -> 'HtmlOutput':
        html_output = HtmlOutput()
        get_value = cls.get_value_from_dict

        html_output.css_path = get_value('css_path',
                                         dict_,
                                         default=None)

        return html_output


class JsonOutput(Output):
    def __init__(self):
        super().__init__()
        raise NotImplementedError('Planned for Version 3.0')

    def make(self, book, substitutions):
        raise NotImplementedError('Planned for Version 3.0')

    @classmethod
    def from_dict(cls, dict_):
        raise NotImplementedError('Planned for Version 3.0')
