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
# $Id: test_catalog.py 191 2007-08-07 03:15:46Z mccosar $

"""
Test suite for catalog.py version 2 series -- Bruce H. McCosar

CORE as of version 2.0.0:

Tests may be added, but no test may be removed unless it is faulty.
Some tests exist only to ensure that all functions behave properly,
even if they are known to be mere shortcuts.  That may not be true
in future versions.
"""

__metaclass__ = type


import unittest
from operator import add

from pcsets.catalog import SetCatalog


# Let's just do this once.
maincatalog = SetCatalog()


class AllTests(unittest.TestCase):

    def setUp(self):
        self.r = maincatalog
        self.expected = [1, 1, 6, 12, 29, 38, 50, 38, 29, 12, 6, 1, 1]
        self.total = reduce(add, self.expected)

    def test_correct_entries_per_page(self):
        for n in range(13):
            found = len(self.r.page(n))
            self.assertEqual(found, self.expected[n])

    def test_correct_entry_placement(self):
        for n in range(13):
            for entry in self.r.page(n):
                self.assertEqual(len(entry), n)

    def test_total_length_via_len(self):
        self.assertEqual(len(self.r), self.total)

    def test_total_length_via_iter(self):
        flatcatalog = list(self.r)
        self.assertEqual(len(flatcatalog), self.total)
