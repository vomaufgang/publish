#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# publish - Python package with cli to turn markdown files into ebooks
# Copyright (c) 2014 Christopher Knörndel
#
# Distributed under the MIT License
# (license terms are at http://opensource.org/licenses/MIT).

"""This module offers a working example of how to use publish and its class model to
produce html and epub files from markdown files.
"""

import logging
from publish.book import Book, Chapter
from publish.output import HtmlOutput, EbookConvertOutput
from publish.substitution import SimpleSubstitution, RegexSubstitution


def main():
    """Shows how to use publish to produce an html file and an epub file while also
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
        [Chapter(src='first_chapter.md'),
         Chapter(src='second_chapter.md'),
         Chapter(src='unfinished_chapter.md', publish=False)])

    substitutions = [
        SimpleSubstitution(old='Cows',
                           new='Substitutions'),
        RegexSubstitution(pattern=r'\+\+(?P<text>.*?)\+\+',
                          replace_with=r'<span class="small-caps">\g<text></span>')]

    html_output = HtmlOutput(
        path='example.html',
        stylesheet='style.css')
    html_output.make(book, substitutions)

    ebook_output = EbookConvertOutput(
        path='example.epub',
        stylesheet='style.css')
    ebook_output.make(book, substitutions)


if __name__ == '__main__':
    main()
