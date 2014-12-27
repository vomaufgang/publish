#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
    'markdown>=2.5.2',
    'wheel>=0.24.0',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='apub',
    version='1.0.0b',
    # TODO: put meaningful description here
    description='Python Boilerplate contains all the boilerplate you need to create a Python package.',
    long_description=readme + '\n\n' + history,
    author='Christopher Knörndel',
    author_email='cknoerndel@anited.de',
    url='https://github.com/vomaufgang/apub/',
    packages=[
        'apub',
        'apub.cli',
        'apub.extensions',
        'apub.extensions.markdown',
        'apub.model',
        'apub.output',
    ],
    entry_points={
        'console_scripts': [
            'apub-make = apub.cli.cli:make',
            'apub-focus = apub.cli.cli:focus',
            'apub-quickstart = apub.cli.cli:quickstart',
        ],
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='apub',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)