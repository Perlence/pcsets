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
# $Id: runtest.py 191 2007-08-07 03:15:46Z mccosar $

"""
Test runner docs will go here.  Basically, you can specify
which module to test from the command line --

python runtest.py        # tests them all

python runtest.py pcset  # just tests module pcset
"""

import unittest, sys

alltests = """
pcset
pcops
catalog
noteops
tonerow
""".split()

class NoSuchTestError(Exception): pass

def match(name):
    if name not in alltests:
        raise NoSuchTestError, "Test '%s' not found." % name
    else:
        return name

def run(testlist,level=2):
    for name in testlist:
        if name:
            print "TESTING MODULE: pcsets.%s" % name
            if name == 'catalog':
                print "Generating prime set catalog... (this may take a moment)"
            test = 'test.test_' + name
            suite = unittest.TestLoader().loadTestsFromName(test)
            unittest.TextTestRunner(verbosity=level).run(suite)

args = sys.argv[1:]
if args:
    tests = [match(name) for name in args]
    run(tests)
else:
    run(alltests,level=1)
