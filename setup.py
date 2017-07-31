#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

if sys.version_info < (3, 6):
    sys.exit('Sorry, Python < 3.6 is not supported.')

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
history = open('docs/history.rst').read().replace('.. :changelog:', '')
version = open('apub/VERSION').read().strip()

requirements = [
    'markdown>=2.6'
]

test_requirements = [
    'pytest',
    'pytest-cov'
]

setup_requirements = [
    'pytest-runner'
]

setup(
    name='apub',
    version=version,
    description='Python package with command line interface to turn markdown '
                'files into ebooks.',
    long_description=readme + '\n\n' + history,
    author='Christopher Knörndel',
    author_email='cknoerndel@anited.de',
    url='https://github.com/vomaufgang/apub/',
    packages=[
        'apub',
    ],
    package_data={
        'apub': ['template.html', 'VERSION']
    },
    install_requires=requirements,
    setup_requires=setup_requirements,
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
    tests_require=test_requirements
)
