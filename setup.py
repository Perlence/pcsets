#!/usr/bin/env python

# pcsets 2.0.2 -- Pitch Class Sets for Python.
#
# Copyright 2007 Bruce H. McCosar
#
# This file is part of the package 'pcsets'
#
# The package 'pcsets' is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3 of
# the License, or (at your option) any later version.
#
# The package 'pcsets' is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# $Id: setup.py 209 2007-08-19 16:41:44Z mccosar $

"""
setup.py

If you run this script, it should install the pcsets library
to your Python distribution's site libraries.
"""

__metaclass__ = type

from setuptools import setup, find_packages


PCSETS_VERSION = '2.0.2' # <===================== (auto-substituted)


DESCRIPTION = 'Pitch Class Sets for Python.'

with open('README.md') as fp:
    LONG_DESCRIPTION = fp.read()

DOWNLOAD_URL = ("http://pcsets.googlecode.com/files/pcsets-%s.tar.gz" %
                PCSETS_VERSION)

CLASSIFIERS = """
Development Status :: 5 - Production/Stable
Environment :: Console
Intended Audience :: Education
License :: OSI Approved :: GNU General Public License (GPL)
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 2.6
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3
Programming Language :: Python :: 3.3
Programming Language :: Python :: 3.4
Topic :: Artistic Software
Topic :: Software Development :: Libraries :: Python Modules
""".strip().split('\n')

setup(
    name='pcsets',
    version=PCSETS_VERSION,
    author='Bruce H. McCosar',
    author_email='bmccosar@gmail.com',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url='http://code.google.com/p/pcsets/',
    download_url=DOWNLOAD_URL,
    classifiers=CLASSIFIERS,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
