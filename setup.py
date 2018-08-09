#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# apub - Python package with cli to turn markdown files into ebooks
# Copyright (c) 2014 Christopher Knörndel
#
# Distributed under the MIT License
# (license terms are at http://opensource.org/licenses/MIT).

"""Setup script for easy_install and pip."""

import sys

MIN_SUPPORTED_PYTHON_VERSION = (3, 6)

if sys.version_info < MIN_SUPPORTED_PYTHON_VERSION:
    sys.exit('Sorry, Python < {} is not supported.'.format(
        '.'.join(map(str, MIN_SUPPORTED_PYTHON_VERSION))
    ))

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


README = open('README.rst').read()
VERSION = open('apub/VERSION').read().strip()

REQUIREMENTS = [
    'markdown>=2.6',
    'Jinja2>=2.10',
    'ruamel.yaml>=0.15.50',
]

TEST_REQUIREMENTS = [
    'pytest',
    'pytest-cov',
    'pytest-runner',
]

DEV_REQUIREMENTS = [
    'tox',
    'pylint',
    'flake8',  # pylint does not support E301&E303 -> required blank lines between functions
               # and/or classes - let flake8 handle these checks
    'wheel',
]
DEV_REQUIREMENTS.extend(TEST_REQUIREMENTS)

setup(
    name='apub',
    version=VERSION,
    description='Python package with command line interface to turn markdown '
                'files into ebooks.',
    long_description=README,
    author='Christopher Knörndel',
    author_email='cknoerndel@anited.de',
    url='https://github.com/vomaufgang/apub/',
    packages=[
        'apub',
    ],
    package_data={
        'apub': ['template.html', 'VERSION']
    },
    install_requires=REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS,
    extras_require={
        'dev': DEV_REQUIREMENTS
    },
    license="MIT",
    zip_safe=False,
    keywords='apub',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
)
