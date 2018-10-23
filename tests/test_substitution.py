#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# anited. publish - Python package with cli to turn markdown files into ebooks
# Copyright (c) 2014 Christopher Knörndel
#
# Distributed under the MIT License
# (license terms are at http://opensource.org/licenses/MIT).

"""Tests for `publish.substitution` module.
"""

# pylint: disable=missing-docstring,no-self-use,invalid-name

from abc import ABCMeta

from publish.substitution import (Substitution,
                                  SimpleSubstitution,
                                  apply_substitutions, RegexSubstitution)


class TestSubstitution:
    def test_substitution_is_abc(self):
        assert isinstance(Substitution, ABCMeta)

    def test_apply_to_is_abstract(self):
        assert 'apply_to' in Substitution.__abstractmethods__


class TestSimpleSubstitution:
    def test_apply_to(self):
        substitution = SimpleSubstitution(old='foo', new='bar')

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
        substitution = SimpleSubstitution(old='foo', new='bar')

        actual = substitution.apply_to('')

        assert actual == ''


class TestRegexSubstitution:
    def test_apply_to(self):
        substitution = RegexSubstitution(pattern=r'\+\+(.*?)\+\+',
                                         replace_with=r'<span class="small-caps">\1</span>')
        text = '\n'.join([
            'foo',
            '++something else++',
            'something foo',
        ])
        expected = '\n'.join([
            'foo',
            '<span class="small-caps">something else</span>',
            'something foo',
        ])

        actual = substitution.apply_to(text)

        assert actual == expected

    def test_apply_to_new_syntax(self):
        substitution = RegexSubstitution(pattern=r'\+\+(?P<text>.*?)\+\+',
                                         replace_with=r'<span class="small-caps">\g<text></span>')
        text = '\n'.join([
            'foo',
            '++something else++',
            'something foo',
        ])
        expected = '\n'.join([
            'foo',
            '<span class="small-caps">something else</span>',
            'something foo',
        ])

        actual = substitution.apply_to(text)

        assert actual == expected

    def test_apply_to_empty_input(self):
        substitution = RegexSubstitution(pattern=r'\+\+(.*?)\+\+',
                                         replace_with='<span class="small-caps">\1</span>')

        actual = substitution.apply_to('')

        assert actual == ''


def test_apply_substitutions():
    substitution1 = SimpleSubstitution(old='foo', new='bar')
    substitution2 = SimpleSubstitution(old='something', new='anything')
    substitution3 = RegexSubstitution(pattern=r'\+\+(.*?)\+\+',
                                      replace_with=r'<span class="small-caps">\1</span>')

    text = '\n'.join([
        'foo',
        'foo',
        'something else',
        '++something else++',
        'something foo',
        '',
        'foo else',
    ])
    expected = '\n'.join([
        'bar',
        'bar',
        'anything else',
        '<span class="small-caps">anything else</span>',
        'anything bar',
        '',
        'bar else',
    ])

    actual = apply_substitutions(text, [substitution1, substitution2, substitution3])

    assert actual == expected
