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
        simple = SimpleSubstitution()
        simple.find = 'foo'
        simple.replace_with = 'bar'

        lines = '\n'.join([
            "foo",
            "foo",
            "something else",
            "something foo",
            "",
            "foo else",
        ])

        excpected = '\n'.join([
            "bar",
            "bar",
            "something else",
            "something bar",
            "",
            "bar else",
        ])

        actual = simple.apply_to(lines)

        self.assertEqual(actual, excpected)


if __name__ == '__main__':
    unittest.main()
