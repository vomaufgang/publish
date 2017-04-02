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

    def test_constructor_find_empty_raises_value_error(self):
        with self.assertRaises(ValueError) as context_manager:
            SimpleSubstitution(find='')

        exception = context_manager.exception

        excpected = 'SimpleSubstitution.find must not be empty'
        actual = str(exception)

        self.assertEqual(actual, excpected)

    def test_constructor_find_none_raises_value_error(self):
        with self.assertRaises(TypeError) as context_manager:
            SimpleSubstitution(find=None)

        exception = context_manager.exception

        excpected = 'SimpleSubstitution.find must not be None'
        actual = str(exception)

        self.assertEqual(actual, excpected)

    def test_find_setter_empty_raises_value_error(self):
        substitution = SimpleSubstitution(find='foo')
        with self.assertRaises(ValueError) as context_manager:
            substitution.find = ''

        exception = context_manager.exception

        excpected = 'SimpleSubstitution.find must not be empty'
        actual = str(exception)

        self.assertEqual(actual, excpected)

    def test_find_setter_none_raises_value_error(self):
        substitution = SimpleSubstitution(find='foo')
        with self.assertRaises(TypeError) as context_manager:
            substitution.find = None

        exception = context_manager.exception

        excpected = 'SimpleSubstitution.find must not be None'
        actual = str(exception)

        self.assertEqual(actual, excpected)

    def test_find_setter_not_representable_as_str_raises_type_error(self):
        substitution = SimpleSubstitution(find='foo')

        class BrokenStr:
            def __str__(self):
                raise Exception('broken __str__')

        with self.assertRaises(TypeError) as context_manager:
            substitution.find = BrokenStr()

        exception = context_manager.exception

        excpected = ("SimpleSubstitution.find must be a string or "
                     "have a working string representation via "
                     "__str__")
        actual = str(exception)

        self.assertEqual(actual, excpected)

    def test_constructor_find_not_representable_as_str_raises_type_error(self):
        class BrokenStr:
            def __str__(self):
                raise Exception('broken __str__')

        with self.assertRaises(TypeError) as context_manager:
            SimpleSubstitution(find=BrokenStr())

        exception = context_manager.exception

        excpected = ("SimpleSubstitution.find must be a string or "
                     "have a working string representation via "
                     "__str__")
        actual = str(exception)

        self.assertEqual(actual, excpected)


if __name__ == '__main__':
    unittest.main()
