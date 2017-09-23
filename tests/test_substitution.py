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
from abc import ABCMeta

import pytest
from apub.substitution import (Substitution,
                               SimpleSubstitution,
                               apply_substitutions)


class TestSubstitution:
    def test_substitution_is_abc(self):
        with pytest.raises(TypeError) as exception_info:
            Substitution()

        assert "Can't instantiate abstract class Substitution " \
               "with abstract methods apply_to" in str(exception_info.value)
        assert isinstance(SimpleSubstitution, ABCMeta)

    # noinspection PyAbstractClass
    def test_apply_to_is_abstract(self):
        class TestAbstract(Substitution):
            pass

        with pytest.raises(TypeError) as exception_info:
            TestAbstract()

        assert "Can't instantiate abstract class TestAbstract " \
               "with abstract methods apply_to" in str(exception_info.value)
        assert Substitution.apply_to.__isabstractmethod__


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


def test_apply_substitutions():
    substitution1 = SimpleSubstitution(old='foo', new='bar')
    substitution2 = SimpleSubstitution(old='something', new='anything')

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
        'anything else',
        'anything bar',
        '',
        'bar else',
    ])

    actual = apply_substitutions(text, [substitution1, substitution2])

    assert actual == expected


# noinspection PyTypeChecker
def test_apply_substitutions_text_is_cast_to_str():
    actual = apply_substitutions(None, [SimpleSubstitution('None', 'All')])
    expected = 'All'

    assert actual == expected


# noinspection PyTypeChecker
def test_apply_substitutions_substitutions_not_iterable():
    with pytest.raises(TypeError) as exception_info:
        apply_substitutions('', None)

    assert "is not iterable" in str(exception_info.value)


# noinspection PyTypeChecker
def test_apply_substitutions_substitutions_wrong_type():
    class NotADuckType:
        pass

    with pytest.raises(AttributeError) as exception_info:
        apply_substitutions('', [NotADuckType()])

    assert "has no attribute 'apply_to'" in str(exception_info.value)
