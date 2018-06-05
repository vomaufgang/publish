#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# apub - Python package with cli to turn markdown files into ebooks
# Copyright (c) 2014 Christopher Knörndel
#
# Distributed under the MIT License
# (license terms are at http://opensource.org/licenses/MIT).

"""This module offers the output classes used to transform book objects into html or epub files.
"""

import logging
import os
import shutil
import subprocess
import uuid
from tempfile import mkdtemp
from textwrap import fill
from typing import Iterable, Generator, Optional
from pkg_resources import resource_string

import markdown
from jinja2 import Template

from apub import __version__ as apub_version
from apub.book import Book, Chapter
from apub.substitution import Substitution, apply_substitutions

LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())

SUPPORTED_EBOOKCONVERT_ATTRIBUTES = (
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
)


class HtmlOutput:
    """Turns a Book object and its chapters into an html document.

    Args:
        path: The output path.
        **kwargs: Any other attribute of this class. (see Attributes below)


    Attributes:
        path (str): The output path.
        css_path (str): The path to the style sheet.
        force_publish (bool): Determines wether to force publish all chapters.

            If set to true, all chapters of the book will be published
            no matter how the chapters are configured.

            Defaults to False.
    """

    def __init__(self,
                 path: str,
                 **kwargs):
        """Initializes a new instance of the :class:`HtmlOutput` class.
        """
        self.path = path
        self.css_path = kwargs.pop('css_path', None)
        self.force_publish = kwargs.pop('force_publish', False)

    def make(self,
             book: Book,
             substitutions: Optional[Iterable[Substitution]] = None):
        """Makes the Output for the provided book and substitutions.

        Args:
            book: The book.
            substitutions: The substitutions.
        """
        LOG.info('Making HtmlOutput ...')

        if not substitutions:
            substitutions = []

        html_document = self._get_html_document(book, substitutions)

        with open(self.path, 'w') as file:
            file.write(html_document)

        LOG.info('... HtmlOutput finished')

    def get_chapters_to_be_published(self,
                                     chapters: Iterable[Chapter]
                                     ) -> Iterable[Chapter]:
        """Gets the list of chapters to be published based on each chapters
        `publish` attribute.

        If the outputs `force_publish` override is set to true, all chapters
        will be published regardless of their individual `publish` attributes.

        Returns:
            The list of chapters to be published.
        """
        if self.force_publish:
            return chapters

        return list(filter(lambda c: c.publish is True, chapters))

    def _get_css(self) -> str:
        """Gets the css from the css file specified in css_path as a string.

        Returns:
            The css from the css file specified in css_path as a string.
        """
        if not self.css_path:
            return ''

        css_path = os.path.join(os.getcwd(), self.css_path)

        LOG.info('Collecting stylesheet ...')
        with open(css_path, 'r') as file:
            css = file.read()

        return css if css else ''

    def _get_html_document(self,
                           book: Book,
                           substitutions: Iterable[Substitution]
                           ) -> str:
        """Takes a book, renders it to html, applying the list of substitutions in the process
        and returns the finished html document as a string.

        Args:
            book: The book.
            substitutions: The list of substitutions.

        Returns:
            The html document as a string.
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
        """Gets the content of the provided list of chapters as as an html string.

        The list of substitutions is applied to the markdown content before it is rendered to
        html.

        The order of the chapters is preserved.

        The resulting html string does not include a head or body, only the chapters markdown
        turned into html.

        Args:
            chapters: The list of chapters.
            substitutions: The list of substitutions.

        Returns:
            The content of the provided list of chapters as an html string.
        """
        markdown_ = self._get_markdown_content(chapters)
        markdown_ = apply_substitutions(
            markdown_,
            substitutions)

        LOG.info('Rendering markdown to html ...')
        return markdown.markdown(markdown_)

    def _get_markdown_content(self,
                              chapters: Iterable[Chapter]) -> str:
        """Gets the markdown content of the provided list of chapters concatenated into a single
        string.

        The order of the chapters is preserved.

        Args:
            chapters: The list of chapters.

        Returns:
            The markdown content of the list of chapters concatenated into a single string.
        """
        markdown_ = []
        md_paragraph_sep = '\n\n'

        if not chapters:
            raise NoChaptersFoundError('Your book contains no chapters.')

        chapters_to_publish = self.get_chapters_to_be_published(chapters)

        if not chapters_to_publish:
            raise NoChaptersFoundError('None of your chapters are set to be'
                                       'published.')

        LOG.info('Collecting chapters ...')
        for chapter in chapters_to_publish:
            with open(chapter.source_path, 'r') as file:
                markdown_.append(file.read())

        return md_paragraph_sep.join(markdown_)


class EbookConvertOutput(HtmlOutput):
    """Turns Book objects and its chapters into an ebook using
    Kavid Goyals ebookconvert command line tool.

    .. todo:: document format of ebookconvert_params -> {'key':'value'} or object.key = value

    Args:
        path: The output path.
        **kwargs: Any other attribute of this class. (see Attributes below)


    Attributes:
        ebookconvert_params (List[str]): An optional list of additional command
            line arguments that will be passed to ebookconvert.
        path (str): The output path.
        css_path (str): The path to the style sheet.
        force_publish (bool): Determines wether to force publish all chapters.

            If set to true, all chapters of the book will be published
            no matter how the chapters are configured.

            Defaults to False.
    """

    def __init__(self,
                 path: str,
                 **kwargs):
        """Initializes a new instance of the :class:`EbookConvertOutput` class.
        """
        super().__init__(path, **kwargs)
        self.ebookconvert_params = kwargs.pop('ebookconvert_params', [])

    def make(self,
             book: Book,
             substitutions: Optional[Iterable[Substitution]] = None):
        """Makes an ebook from the provided book object and the markdown chapters
        specified therein.

        Substitutions are applied to the raw markdown before the markdown is
        processed.

        Args:
            book: The book.
            substitutions: The list of substitutions.
        """
        LOG.info('Making EbookConvertOutput ...')
        if not book:
            raise AttributeError("book must not be None")

        if not substitutions:
            substitutions = []

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

            call_params = _get_ebook_convert_params(book,
                                                    input_path=temp_path,
                                                    output_path=self.path,
                                                    additional_params=self.ebookconvert_params)

            LOG.info('Calling ebook-convert ...')

            try:
                subprocess.call(call_params)
            except FileNotFoundError:
                LOG.error(
                    fill('Could not find ebook-convert. Please install calibre if you want to '
                         'use EbookconvertOutput and make sure ebook-convert is accessible '
                         'through the PATH variable.'))
                return
            LOG.info('... EbookConvertOutput finished')
        finally:
            shutil.rmtree(temp_directory)


def _get_ebook_convert_params(book: Book,
                              input_path: str,
                              output_path: str,
                              additional_params: Optional[Iterable[str]] = None
                              ) -> Iterable[str]:
    """Gets the call params for the ebookconvert commandline.

    The book's attributes are translated into ebookconvert metadata commandline options
    while any additional options present in EbookConvertOutput.ebookconvert_params are
    appended to the call params as is.

    Args:
        book: The book object.
        input_path: The path the html file that will be passed to ebookconvert.
        output_path: The output path.
    """
    if not additional_params:
        additional_params = []

    call_params = [
        'ebook-convert',
        input_path,
        output_path
    ]
    call_params.extend(_yield_attributes_as_params(book))
    call_params.extend(additional_params)
    return call_params


def _apply_template(html_content: str,
                    title: str,
                    css: str,
                    language: str) -> str:
    """Renders the html content, title, css and document language into the jinja2 formatted
    template and returns the resulting html document.

    Args:
        html_content: The html content gets inserted into the {{ content }} of the template.
        title: The title gets inserted into the {{ title }} of the template.
        css: The css gets inserted into the {{ css }} of the template.
        language: The language gets inserted into the {{ language }} of the template.

    Returns:
        The html document.
    """
    template = resource_string(__name__, 'template.html') \
        .decode('utf-8') \
        .replace('\r\n', '\n')
    # resource_string opens the file as bytes, which means that we
    # have to decode to utf-8. The replace is necessary because
    # resource_string, instead of open, does not automatically
    # strip \r\n down to \n on windows systems. Leaving \r\n as is
    # would produce double line breaks when writing the resulting string
    # back to disc, thus we have to do the replacement ourselves, too.

    return Template(template).render(content=html_content,
                                     title=title,
                                     css=css,
                                     language=language,
                                     apub_version=apub_version)


def _yield_attributes_as_params(object_) -> Generator[str, None, None]:
    """Takes an object or dictionary and returns a generator yielding all
    attributes that can be processed by the ebookconvert command line as a
    parameter array.

    Args:
        object_: An object or dictionary.

    Returns:
        A generator yielding all attributes of the object supported
        by ebookconvert.
    """
    # This way the book can contain attributes not supported by ebookconvert
    # (or any other specific output that follows this explicit pattern)
    for attr_name in SUPPORTED_EBOOKCONVERT_ATTRIBUTES:
        if hasattr(object_, attr_name):
            attr = getattr(object_, attr_name)
        else:
            try:
                attr = object_[attr_name]
            except (TypeError, KeyError):
                continue

        if not attr:
            continue

        attr = str(attr)
        if attr and not attr.isspace():
            yield '--{0}={1}'.format(attr_name, attr)


class NoChaptersFoundError(Exception):
    """No chapters found."""
    pass
