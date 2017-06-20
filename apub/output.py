#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# apub - Python package with cli to turn markdown files into ebooks
# Copyright (c) 2014 Christopher Knörndel
#
# Distributed under the MIT License
# (license terms are at http://opensource.org/licenses/MIT).

import logging
from typing import Iterable, Generator

import markdown
import os
import shutil
import subprocess
import uuid
from abc import ABCMeta, abstractmethod
from pkg_resources import resource_string
from tempfile import mkdtemp

from apub import __version__ as apub_version
from apub.book import Book, Chapter
from apub.errors import NoChaptersFoundError
from apub.substitution import Substitution

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler)


_supported_ebookconvert_attrs = [
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

# todo: Output has 'css', html_output has 'css_path' - choose one,
#       remove the other

# todo validate mandatory book attributes - are there even any
#      mandatory ones?

# todo optional subtitle, supported by HtmlOutput and JsonOutput

# todo what was generate_toc even for?


class Output(metaclass=ABCMeta):
    """Abstract base class for specific Output implementations.

    :ivar css_path: The path to the style sheet.
    :ivar force_publish: Determines wether to force publish all chapters.
        
        If set to true, all chapters of the book will be published
        no matter how the chapters are configured.
    :ivar path: The output path.
    """

    def __init__(self,
                 path: str=None,
                 css_path: str=None,
                 force_publish: bool=False):
        self.path = path
        self.css_path = css_path
        self.force_publish = force_publish

    @abstractmethod
    def make(self, book: Book, substitutions: Iterable[Substitution]=None):
        pass

    def get_chapters_to_publish(self,
                                chapters: Iterable[Chapter]
                                ) -> Iterable[Chapter]:
        if self.force_publish:
            return chapters
        else:
            return list(filter(lambda c: c.publish is True, chapters))

    def validate(self):
        """Validates the Book object.
        
        Errors are raised as AttributeErrors."""
        if not self.path:
            raise AttributeError('Output path must be set.')


class EbookConvertOutput(Output):

    def __init__(self,
                 path: str=None,
                 css_path: str=None,
                 force_publish: bool=False,
                 ebookconvert_params: Iterable[str]=None):
        super().__init__(path, css_path, force_publish)
        self.ebookconvert_params = \
            [] if not ebookconvert_params else ebookconvert_params

    def make(self,
             book: Book,
             substitutions: Iterable[Substitution]=None):
        if not book:
            raise AttributeError("book must not be None")

        if not substitutions:
            substitutions = []

        self.validate()

        temp_directory = mkdtemp()
        # mkstmp and NamedTemporaryFile won't work, because the html file
        # will be kept open by EbookConvertOutput with exclusive access,
        # which means ebook-convert can't read the html to create the epub.
        # -> ebook-convert fails with 'Permission denied'.

        try:
            html_output = HtmlOutput()
            html_output.path = os.path.join(
                temp_directory, str(uuid.uuid4()) + '.html')
            html_output.css_path = self.css_path
            html_output.force_publish = self.force_publish

            html_output.make(book, substitutions)

            call_params = [
                'ebook-convert',
                html_output.path,
                self.path
            ]

            call_params.extend(_yield_attrs_as_params(book))
            call_params.extend(self.ebookconvert_params)

            subprocess.call(call_params)
        finally:
            shutil.rmtree(temp_directory)


def _yield_attrs_as_params(book: Book) -> Generator[str, None, None]:
    """Takes a book and returns a generator yielding all attributes
    that can be processed by the ebookconvert command line as a param array.

    :param book: The book.

    :returns: A generator yielding all attributes of the object supported by
        ebookconvert.
    """
    # This way the book can contain attrs not supported by ebookconvert
    # (or any other specific output that follows this explicit pattern)
    for attr_name in _supported_ebookconvert_attrs:
        if hasattr(book, attr_name):
            attr = getattr(book, attr_name)
            if not attr:
                continue
            attr = str(attr)
            if attr and not attr.isspace():
                yield "--{0}=\"{1}\"".format(attr_name, attr)


class HtmlOutput(Output):

    def __init__(self,
                 path: str=None,
                 css_path: str=None,
                 force_publish: bool=False):
        super().__init__(path, css_path, force_publish)

    def make(self,
             book: Book,
             substitutions: Iterable[Substitution]=None):
        """Makes the HtmlOutput for the provided book and substitutions.

        :param book: The book.
        :param substitutions: The substitutions.
        """
        if not book:
            raise AttributeError("book must not be None")

        if not substitutions:
            substitutions = []

        html_document = self._get_html_document(book, substitutions)

        with open(self.path, 'w') as file:
            file.write(html_document)

    def _get_html_document(self,
                           book: Book,
                           substitutions: Iterable[Substitution]
                           ) -> str:
        """

        :param book: The book.
        :param substitutions: The substitutions.
        """

        html_content = self._get_html_content(book.chapters, substitutions)
        html_document = self._apply_template(html_content=html_content,
                                             title=book.title,
                                             css=self._get_css(),
                                             language=book.language)

        return html_document

    def _get_html_content(self,
                          chapters: Iterable[Chapter],
                          substitutions: Iterable[Substitution]
                          ) -> str:
        markdown_ = self._get_markdown_content(chapters)
        markdown_ = self._apply_substitutions(
            markdown_,
            substitutions)

        return markdown.markdown(markdown_)

    def _apply_template(self,
                        html_content: str,
                        title: str,
                        css: str,
                        language: str) -> str:
        template = resource_string(__name__, 'template.html')\
            .decode('utf-8')\
            .replace('\r\n', '\n')
        # resource_string opens the file as bytes, which means that we
        # have to decode to utf-8. The replace is necessary because
        # resource_string, instead of open, does not automatically
        # strip \r\n down to \n on windows systems. Leaving \r\n as is
        # would produce double line breaks when writing the resulting string
        # back to disc, thus we have to do the replacement ourselves, too.

        return template.format(content=html_content,
                               title=title,
                               css=css,
                               language=language,
                               apub_version=apub_version)

    def _get_css(self) -> str:
        if not self.css_path:
            return ''

        css_path = os.path.join(os.getcwd(), self.css_path)

        with open(css_path, 'r') as file:
            css = file.read()

        return css if css else ''

    def _get_markdown_content(self,
                              chapters: Iterable[Chapter]
                              ) -> str:
        markdown_ = []
        md_paragraph_sep = '\n\n'

        if not chapters:
            raise NoChaptersFoundError('Your book contains no chapters.')

        chapters_to_publish = self.get_chapters_to_publish(chapters)

        if not chapters_to_publish:
            raise NoChaptersFoundError('None of your chapters are set to be'
                                       'published.')

        for chapter in chapters_to_publish:
            with open(chapter.source, 'r') as file:
                markdown_.append(file.read())

        return md_paragraph_sep.join(markdown_)

    def _apply_substitutions(
            self,
            markdown_: str,
            substitutions: Iterable[Substitution]) -> str:
        """Applies the list of substitutions to the markdown content.

        :param markdown_: The markdown content of the chapter.
        :param substitutions: The list of substitutions to be applied.

        :returns: The dict of markdown strings by chapter with
            the substitutions applied.
        """
        for substitution in substitutions:
            markdown_ = substitution.apply_to(markdown_)

        return markdown_


class JsonOutput(Output):
    """Planned for Version 3.0"""

    def __init__(self):
        super().__init__()
        raise NotImplementedError('Planned for Version 3.0')

    def make(self,
             book: Book,
             substitutions: Iterable[Substitution]=None):
        raise NotImplementedError('Planned for Version 3.0')
