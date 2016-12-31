#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_project
----------------------------------

Tests for `apub.model.project` module.
"""

import unittest

from apub.output.ebookconvert import _yield_attrs_as_ebookconvert_params


class TestEbookConvertOutput(unittest.TestCase):

    def test_attrs_as_ebookconvert_params(self):
        # todo write test with custom object
        class CustomObject(object):
            pass

        # todo write test with dict
        dict_ = {
            "publisher": "Me"
        }

        pass


if __name__ == '__main__':
    unittest.main()
