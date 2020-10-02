#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# anited. publish - Python package with cli to turn markdown files into ebooks
# Copyright (c) 2014 Christopher Knörndel
#
# Distributed under the MIT License
# (license terms are at http://opensource.org/licenses/MIT).

"""Setup script for easy_install and pip."""

import sys
import codecs
import os.path

MIN_SUPPORTED_PYTHON_VERSION = (3, 6)

if sys.version_info < MIN_SUPPORTED_PYTHON_VERSION:
    sys.exit('Sorry, Python < {} is not supported.'.format(
        '.'.join(map(str, MIN_SUPPORTED_PYTHON_VERSION))
    ))

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def read(rel_path):
    """Reads the contents of the file atthe  relative path `rel_path`.
    """
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as file_:
        return file_.read()


def get_version(rel_path):
    """Gets the version number declared in the `__version__` constant of
    the Python file at `rel_path`.
    """
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]

    raise RuntimeError("Unable to find version string.")


README = open('README.md').read()
VERSION = get_version('publish/__init__.py')
REQUIREMENTS = open('requirements.txt').readlines()
DEV_REQUIREMENTS = open('dev-requirements.txt').readlines()[1:]

setup(
    name='anited-publish',
    version=VERSION,
    description='Python package with command line interface to turn markdown '
                'files into ebooks.',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Christopher Knörndel',
    author_email='cknoerndel@anited.de',
    url='https://gitlab.com/anited/publish',
    packages=[
        'publish',
    ],
    package_data={
        'publish': ['template.jinja', 'VERSION']
    },
    entry_points={
        'console_scripts': [
            'publish = publish.cli:main'
        ]
    },
    python_requires=">=3.6",
    install_requires=REQUIREMENTS,
    tests_require=DEV_REQUIREMENTS,
    extras_require={
        'dev': DEV_REQUIREMENTS
    },
    license="MIT",
    zip_safe=False,
    keywords='publish',
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
