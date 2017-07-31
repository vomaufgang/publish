#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# apub - Python package with cli to turn markdown files into ebooks
# Copyright (c) 2014 Christopher Knörndel
#
# Distributed under the MIT License
# (license terms are at http://opensource.org/licenses/MIT).

"""
test_chapter
----------------------------------

Tests for `apub.model.chapter` module.
"""

from apub.substitution import SimpleSubstitution


class TestSimpleSubstitution:
    def test_apply_to(self):
        substitution = SimpleSubstitution(find='foo', replace_with='bar')

        text = '\n'.join([
            'foo',
            'foo',
            'something else',
            'something foo',
            '',
            'foo else',
        ])
        expected = '\n'.join([
            'bar',
            'bar',
            'something else',
            'something bar',
            '',
            'bar else',
        ])

        actual = substitution.apply_to(text)

        assert actual == expected

    def test_apply_to_empty_input(self):
        substitution = SimpleSubstitution(find='foo', replace_with='bar')

        text = ''
        expected = ''

        actual = substitution.apply_to(text)

        assert actual == expected
