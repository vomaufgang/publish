#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
