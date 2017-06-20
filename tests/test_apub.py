#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# apub - Python package with cli to turn markdown files into ebooks
# Copyright (c) 2014 Christopher Knörndel
#
# Distributed under the MIT License
# (license terms are at http://opensource.org/licenses/MIT).

import unittest


class TestApub(unittest.TestCase):
    def test_all(self):
        """Test that __all__ contains only names that are actually exported.
        """
        import apub

        missing = list(set(name for name in apub.__all__
                           if getattr(apub, name, None) is None))

        self.assertFalse(
            missing,
            msg="__all__ contains unresolved names: {0}"
                .format(", ".join(missing), ))
