#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
HISTORY = open('docs/history.rst').read().replace('.. :changelog:', '')
VERSION = open('apub/VERSION').read().strip()

REQUIREMENTS = [
    'markdown>=2.6'
]

TEST_REQUIREMENTS = [
    'pytest',
    'pytest-cov',
    'pytest-runner',
]

setup(
    name='apub',
    version=VERSION,
    description='Python package with command line interface to turn markdown '
                'files into ebooks.',
    long_description=README + '\n\n' + HISTORY,
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
    license="MIT",
    zip_safe=False,
    keywords='apub',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    tests_require=TEST_REQUIREMENTS
)
