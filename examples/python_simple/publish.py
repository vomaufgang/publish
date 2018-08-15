#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# apub - Python package with cli to turn markdown files into ebooks
# Copyright (c) 2014 Christopher Knörndel
#
# Distributed under the MIT License
# (license terms are at http://opensource.org/licenses/MIT).

"""This module offers a working example of how to use apub and its class model to produce html
and epub files from markdown files.
"""

import logging
from apub.book import Book, Chapter
from apub.output import HtmlOutput, EbookConvertOutput
from apub.substitution import SimpleSubstitution, RegexSubstitution


def main():
    """Shows how to use apub to produce an html file and an epub file while also
    applying a substitution to the markdown text in the process.

    Note that logging of everything but exceptions is turned off by default and has to be
    turned on by the user by configuring the python standard logging module, for example
    by calling logging.basicConfig with the desired configuration."""
    logging.basicConfig(format='%(message)s', level=logging.INFO)

    book = Book(
        title='Example',
        authors='Max Mustermann',
        language='en')

    book.chapters.extend(
        [Chapter(source_path='first_chapter.md'),
         Chapter(source_path='second_chapter.md'),
         Chapter(source_path='unfinished_chapter.md', publish=False)])

    substitutions = [
        SimpleSubstitution(old='Cows',
                           new='Substitutions'),
        RegexSubstitution(pattern=r'\+\+(.*?)\+\+',
                          replace_with=r'<span class="small-caps">\1</span>')]

    html_output = HtmlOutput(
        path='example.html',
        css_path='style.css')
    html_output.make(book, substitutions)

    ebook_output = EbookConvertOutput(
        path='example.epub',
        css_path='style.css')
    ebook_output.make(book, substitutions)


if __name__ == '__main__':
    main()
