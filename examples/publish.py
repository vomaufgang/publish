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


def main():
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
