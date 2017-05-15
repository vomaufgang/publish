#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
