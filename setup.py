"""easyredditbot is an API to create a reddit bot as quickly as possible.

Copyright (C) 2017 teaearlgraycold

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from os import path
from re import search
from setuptools import setup

PACKAGE_NAME = 'easyredditbot'
HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, PACKAGE_NAME, 'version.py'), 'r') as fp:
    VERSION = search('__version__ = \'([^\']+)\'', fp.read()).group(1)

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description='Create a reddit bot as quickly as possible',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Utilities',
    ],
    url='http://github.com/teaearlgraycold/easyredditbot',
    author='teaearlgraycold',
    license='GPLv3',
    packages=[PACKAGE_NAME],
    install_requires=[
        'praw >=4.0, <6.0',
    ],
    tests_require=[
        'nose',
    ],
    test_suite='nose.collector',
    zip_safe=False
)
