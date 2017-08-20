#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# apub - Python package with cli to turn markdown files into ebooks
# Copyright (c) 2014 Christopher Knörndel
#
# Distributed under the MIT License
# (license terms are at http://opensource.org/licenses/MIT).

import logging
import os
import shutil
import subprocess
import uuid
from abc import ABCMeta, abstractmethod
from tempfile import mkdtemp
from textwrap import fill
from typing import Iterable, Generator, Optional

import markdown
from pkg_resources import resource_string

from apub import __version__ as apub_version
from apub.book import Book, Chapter
from apub.substitution import Substitution, apply_substitutions

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

SUPPORTED_EBOOKCONVERT_ATTRS = [
    'author_sort',
    'authors',
    'book_producer',
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


# todo validate mandatory book attributes - are there even any
#      mandatory ones?
# todo optional subtitle, supported by HtmlOutput and JsonOutput


class Output(metaclass=ABCMeta):
    """Abstract base class for specific Output implementations.

    :ivar css_path: The path to the style sheet.
    :ivar force_publish: Determines wether to force publish all chapters.
        
        If set to true, all chapters of the book will be published
        no matter how the chapters are configured.

        Defaults to False.
    :ivar path: The output path.
    """

    def __init__(self,
                 path: str,
                 css_path: Optional[str] = None,
                 force_publish: Optional[bool] = False):
        self.path = path
        self.css_path = css_path
        self.force_publish = force_publish

    @abstractmethod
    def make(self, book: Book, substitutions: Iterable[Substitution] = None):
        """Makes the Output for the provided book and substitutions.

        Abstract method: Implementation has to be provided by any Output
        subclass.
        """
        pass

    def get_chapters_to_publish(self,
                                chapters: Iterable[Chapter]
                                ) -> Iterable[Chapter]:
        """Gets the list of chapters set to be published based on
        each chapters 'publish' attribute and the outputs force_publish
        override.

        :returns: The list of chapters set to be published.
        """
        if self.force_publish:
            return chapters
        else:
            return list(filter(lambda c: c.publish is True, chapters))

    def _get_css(self) -> str:
        # todo document _get_css
        if not self.css_path:
            return ''

        css_path = os.path.join(os.getcwd(), self.css_path)

        log.info('Collecting stylesheet ...')
        with open(css_path, 'r') as file:
            css = file.read()

        return css if css else ''

    def _get_html_document(self,
                           book: Book,
                           substitutions: Iterable[Substitution]) -> str:
        # todo document _get_html_document
        # todo this also means that EbookconvertOutput doesn't have to call HtmlOut anymore
        """

        :param book: The book.
        :param substitutions: The substitutions.
        """

        html_content = self._get_html_content(book.chapters, substitutions)
        html_document = _apply_template(html_content=html_content,
                                        title=book.title,
                                        css=self._get_css(),
                                        language=book.language)

        return html_document

    def _get_html_content(self,
                          chapters: Iterable[Chapter],
                          substitutions: Iterable[Substitution]) -> str:
        # todo document _get_html_content
        markdown_ = self._get_markdown_content(chapters)
        markdown_ = apply_substitutions(
            markdown_,
            substitutions)

        log.info('Rendering markdown to html ...')
        return markdown.markdown(markdown_)

    def _get_markdown_content(self,
                              chapters: Iterable[Chapter]
                              ) -> str:
        # todo document _get_markdown_content
        markdown_ = []
        md_paragraph_sep = '\n\n'

        if not chapters:
            raise NoChaptersFoundError('Your book contains no chapters.')

        chapters_to_publish = self.get_chapters_to_publish(chapters)

        if not chapters_to_publish:
            raise NoChaptersFoundError('None of your chapters are set to be'
                                       'published.')

        log.info('Collecting chapters ...')
        for chapter in chapters_to_publish:
            with open(chapter.source, 'r') as file:
                markdown_.append(file.read())

        return md_paragraph_sep.join(markdown_)

    def validate(self):
        """Validates the Output object.

        :raises AttributeError: Errors encountered during validation are
            raised as AttributeErrors.
        """
        if not self.path:
            raise AttributeError('Output path must be set.')


class EbookConvertOutput(Output):
    """Turns Book objects and its chapters into an ebook using
    Kavid Goyals ebookconvert command line tool.

    :ivar css_path: The path to the style sheet.
    :ivar force_publish: Determines wether to force publish all chapters.

        If set to true, all chapters of the book will be published
        no matter how the chapters are configured.

        Defaults to False.
    :ivar path: The output path.
    :ivar ebookconvert_params: An optional list of additional command
        line arguments that will be passed to ebookconvert.
    """

    def __init__(self,
                 path: str,
                 css_path: Optional[str] = None,
                 force_publish: Optional[bool] = False,
                 ebookconvert_params: Optional[Iterable[str]] = None):
        super().__init__(path, css_path, force_publish)
        self.ebookconvert_params = \
            [] if not ebookconvert_params else ebookconvert_params

    def make(self,
             book: Book,
             substitutions: Optional[Iterable[Substitution]] = None):
        """Makes the Output for the provided book and substitutions.
        """
        log.info('Making EbookConvertOutput ...')
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
            temp_path = os.path.join(
                temp_directory, str(uuid.uuid4()) + '.html')

            html_document = self._get_html_document(book, substitutions)

            with open(temp_path, 'w') as file:
                file.write(html_document)

            call_params = [
                'ebook-convert',
                temp_path,
                self.path
            ]

            call_params.extend(_yield_attrs_as_params(book))
            call_params.extend(self.ebookconvert_params)

            log.info('Calling ebook-convert ...')
            subprocess.call(call_params)
            log.info('... EbookConvertOutput finished')
        except FileNotFoundError:
            # todo split into multiple try's, FNFE may also be raised by _get_css, open, etc.
            # -> don't split, but use sub-trys because all temp activity must be rmtree'd
            log.error(fill('Could not find ebook-convert. Please install calibre if you want to '
                           'use EbookconvertOutput and make sure ebook-convert is accessible '
                           'through the PATH variable.'))
        finally:
            shutil.rmtree(temp_directory)


class HtmlOutput(Output):
    """Turns a Book object and its chapters into an html document.

    :ivar css_path: The path to the style sheet.
    :ivar force_publish: Determines whether to force publish all chapters.

        If set to true, all chapters of the book will be published
        no matter how the chapters are configured.

        Defaults to False.
    :ivar path: The output path.
    """

    def __init__(self,
                 path: str,
                 css_path: Optional[str] = None,
                 force_publish: Optional[bool] = False):
        super().__init__(path, css_path, force_publish)

    def make(self,
             book: Book,
             substitutions: Optional[Iterable[Substitution]] = None):
        """Makes the Output for the provided book and substitutions.

        :param book: The book.
        :param substitutions: The substitutions.
        """
        log.info('Making HtmlOutput ...')
        if not book:
            raise AttributeError("book must not be None")

        if not substitutions:
            substitutions = []

        html_document = self._get_html_document(book, substitutions)

        with open(self.path, 'w') as file:
            file.write(html_document)

        log.info('... HtmlOutput finished')


class JsonOutput(Output):
    """Planned for Version 3.0"""

    def __init__(self,
                 path: str,
                 css_path: Optional[str] = None,
                 force_publish: Optional[bool] = False, ):
        super().__init__(path, css_path, force_publish)
        raise NotImplementedError('Planned for Version 3.0')

    def make(self,
             book: Book,
             substitutions: Iterable[Substitution] = None):
        raise NotImplementedError('Planned for Version 3.0')


def _apply_template(html_content: str,
                    title: str,
                    css: str,
                    language: str) -> str:
    # todo document _apply_template
    template = resource_string(__name__, 'template.html') \
        .decode('utf-8') \
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


def _yield_attrs_as_params(book: Book) -> Generator[str, None, None]:
    """Takes a book and returns a generator yielding all attributes
    that can be processed by the ebookconvert command line as a param
    array.

    :param book: The book.

    :returns: A generator yielding all attributes of the object supported
        by ebookconvert.
    """
    # This way the book can contain attrs not supported by ebookconvert
    # (or any other specific output that follows this explicit pattern)
    for attr_name in SUPPORTED_EBOOKCONVERT_ATTRS:
        if hasattr(book, attr_name):
            attr = getattr(book, attr_name)
            if not attr:
                continue
            attr = str(attr)
            if attr and not attr.isspace():
                yield "--{0}=\"{1}\"".format(attr_name, attr)


# Errors

class NoChaptersFoundError(Exception):
    pass
