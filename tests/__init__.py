#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# anited_publish - Python package with cli to turn markdown files into ebooks
# Copyright (c) 2014 Christopher Knörndel
#
# Distributed under the MIT License
# (license terms are at http://opensource.org/licenses/MIT).

# pylint: disable=missing-docstring

from anited_publish.book import Book


def get_test_book():
    return Book(title='title',
                author_sort='author_sort',
                authors='authors',
                book_producer='book_producer',
                comments='comments',
                cover='cover',
                isbn='isbn',
                language='language',
                pubdate='pubdate',
                publisher='publisher',
                rating='rating',
                series='series',
                series_index='series_index',
                tags='tags',
                title_sort='title_sort')
