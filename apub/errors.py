#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# apub - Python package with cli to turn markdown files into ebooks
# Copyright (c) 2014 Christopher Knörndel
#
# Distributed under the MIT License
# (license terms are at http://opensource.org/licenses/MIT).


class MalformedIdError(Exception):
    pass


class MalformedSlugError(Exception):
    pass


class OutputNotFoundError(Exception):
    pass


class MalformedProjectJsonError(Exception):
    pass


class NoChaptersFoundError(Exception):
    pass


class NoBookFoundError(Exception):
    pass
