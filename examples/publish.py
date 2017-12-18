#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# apub - Python package with cli to turn markdown files into ebooks
# Copyright (c) 2014 Christopher Knörndel
#
# Distributed under the MIT License
# (license terms are at http://opensource.org/licenses/MIT).

import logging
from apub.book import Book, Chapter
from apub.output import HtmlOutput, EbookConvertOutput
from apub.substitution import SimpleSubstitution


def main():
    logging.basicConfig(format='%(message)s', level=logging.INFO)

    book = Book(
        title='Example',
        authors='Max Mustermann',
        language='en')

    book.chapters.extend(
        [Chapter(source_path='first_chapter.md'),
         Chapter(source_path='second_chapter.md')])

    substitution = SimpleSubstitution(
        old='Cows',
        new='Substitutions')

    html_output = HtmlOutput(
        path='example.html',
        css_path='style.css')
    html_output.make(book, [substitution])

    ebook_output = EbookConvertOutput(
        path='example.epub',
        css_path='style.css')
    ebook_output.make(book, [substitution])


if __name__ == '__main__':
    main()
