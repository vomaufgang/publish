#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# apub - Python package with cli to turn markdown files into ebooks
# Copyright (c) 2014 Christopher Knörndel
#
# Distributed under the MIT License
# (license terms are at http://opensource.org/licenses/MIT).

from apub import (Book,
                  Chapter,
                  HtmlOutput,
                  EbookConvertOutput,
                  SimpleSubstitution)
import logging


def main():
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    # todo document, logging off by default, needs to be configured by user, example
    # with basicConfig, info is good level for general information, level only affects apub, does
    # not affect ebook-convert's logging / console output

    book = Book(
        title='Example',
        authors='Max Mustermann',
        language='en')

    book.chapters.extend(
        [Chapter(source='first_chapter.md'),
         Chapter(source='second_chapter.md')])

    substitution = SimpleSubstitution(
        find='Cows',
        replace_with='Substitutions')

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
