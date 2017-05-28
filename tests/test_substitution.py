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

"""
test_chapter
----------------------------------

Tests for `apub.model.chapter` module.
"""

import unittest

from apub.substitution import SimpleSubstitution


class TestSimpleSubstitution(unittest.TestCase):
    def test_apply_to(self):
        substitution = SimpleSubstitution(find='foo',
                                          replace_with='bar')

        text = '\n'.join([
            'foo',
            'foo',
            'something else',
            'something foo',
            '',
            'foo else',
        ])
        excpected = '\n'.join([
            'bar',
            'bar',
            'something else',
            'something bar',
            '',
            'bar else',
        ])

        actual = substitution.apply_to(text)

        self.assertEqual(actual, excpected)

    def test_apply_to_empty_input(self):
        substitution = SimpleSubstitution(find='foo',
                                          replace_with='bar')

        text = ''
        excpected = ''

        actual = substitution.apply_to(text)

        self.assertEqual(actual, excpected)


if __name__ == '__main__':
    unittest.main()
