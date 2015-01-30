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
# $Id: test_tonerow.py 208 2007-08-19 13:14:36Z mccosar $

"""
Test suite for tonerow.py version 2 series -- Bruce H. McCosar

EXPERIMENTAL as of version 2.0:

This is not a core module; it's in development and
won't be stable until at least version 2.1
"""

__metaclass__ = type

import unittest

from pcsets.pcset import PcSet
from pcsets.noteops import pcfor
from pcsets.tonerow import *


class ToneRowDefinition(unittest.TestCase):

    # correct definition, correct output.

    def test_trdef_list(self):
        a = [9, 1, 11, 10, 4, 2, 3, 8, 5, 7, 6, 0]
        t = ToneRow(a)
        self.assertEqual(list(t), a)

    def test_trdef_spec(self):
        a = '1268A94B7053'
        t = ToneRow(a)
        self.assertEqual(str(t), a)

    def test_trdef_pcset_notes(self):
        # looks like a notes test, but actually tests
        # whether ToneRow will accept a PcSet as input.
        a = "C Eb C# G F Bb D B F# Ab E A"
        t = ToneRow(pcfor(a))
        self.assertEqual(str(t), str(pcfor(a)))

    # incorrect definition, exception

    def test_incomplete_row(self):
        self.assertRaises(ToneRowException, ToneRow, range(11))

    # other relevant exceptions are raised by parent PcSet
    # class ... that's why we reuse code ;-)


class ToneRowMethods(unittest.TestCase):

    def setUp(self):
        # Obvious:
        # The linear ascending chromatic scale.
        self.obvious = ToneRow(range(12))
        # Obscure:
        # An example of using a simple pcset as a generator
        # for a tonerow . . . one day there will be a function
        # like this, but for now, we hack . . . .
        a = PcSet('015')
        self.obscure = ToneRow(
            str(a) +
            str(a.TnI(7)) +
            str(a.T(10)) +
            str(a.TnI(9))
            )
        # It was worked out by hand, months ago!

    def test_P_obvious(self):
        self.assertEqual(str(self.obvious.P(5)), '56789AB01234')

    def test_P_obscure(self):
        self.assertEqual(str(self.obscure.P(4)), '459BA6237108')

    def test_R_obvious_str_n(self):
        # Also includes a test for string input (A = 10, B = 11)
        self.assertEqual(str(self.obvious.R('B')), 'BA9876543210')

    def test_R_obscure(self):
        self.assertEqual(str(self.obscure.R(4)), '4893BA267510')

    def test_I_obvious(self):
        self.assertEqual(str(self.obvious.I(0)), '0BA987654321')

    def test_I_obscure(self):
        self.assertEqual(str(self.obscure.I(4)), '43B9A2651780')

    def test_RI_obvious(self):
        self.assertEqual(str(self.obvious.RI(5)), '56789AB01234')

    def test_RI_obscure(self):
        self.assertEqual(str(self.obscure.RI(4)), '40B59A621378')

    def test_shift_obvious(self):
        self.assertEqual(str(self.obvious.shift(5)), '789AB0123456')

    def test_shift_obscure(self):
        self.assertEqual(str(self.obscure.shift(4)), '3984015762AB')

    def test_rotate_obvious(self):
        self.assertEqual(str(self.obvious.rotate(5, 'A')), 'AB0123456789')

    def test_rotate_obscure(self):
        self.assertEqual(str(self.obscure.rotate(4, 'A')), 'A43B78021956')

    def test_contour_obvious(self):
        self.assertEqual(self.obvious.contour(), [1]*12)

    def test_contour_obvious_2(self):
        self.assertEqual(self.obscure.contour(),
                         [1, 4, 2, 11, 8, 8, 1, 4, 6, 11, 8, 8])


class ToneRowOperations(unittest.TestCase):

    def setUp(self):
        # Test case is generated at random each time.
        # (New system in version 2.0.2)
        self.testrow = randomrow()

    def test_equivalent_by_P(self):
        # Tests all 12 possibilities.
        for n in range(12):
            subject = self.testrow.P(n)
            self.assert_(equivalent(self.testrow, subject))

    def test_equivalent_by_R(self):
        # Tests all 12 possibilities.
        for n in range(12):
            subject = self.testrow.R(n)
            self.assert_(equivalent(self.testrow, subject))

    def test_equivalent_by_I(self):
        # Tests all 12 possibilities.
        for n in range(12):
            subject = self.testrow.I(n)
            self.assert_(equivalent(self.testrow, subject))

    def test_equivalent_by_RI(self):
        # Tests all 12 possibilities.
        for n in range(12):
            subject = self.testrow.RI(n)
            self.assert_(equivalent(self.testrow, subject))

    def test_not_equivalent(self):
        # Tests shift possibilities from 1 to 11.
        # Can't use randomrow() here, since it could
        # produce a shift equivalent random row by accident!
        # (eg the chromatic scale).
        a = ToneRow([10, 0, 2, 8, 5, 6, 3, 1, 11, 4, 9, 7])
        for i in range(11):
            subject = a.shift(i+1)
            self.failIf(equivalent(self.testrow, subject))

    def test_rotequiv(self):
        # The grand prize.
        # Generate all 48 tonerows in the family;
        # shift each by anywhere from 0 to 11.
        # Test for rotational equivalence.
        #
        # First generate a copy, just to be safe.
        # Unit testing is there to catch errors you haven't thought of.
        subject = ToneRow(self.testrow)
        methods = [subject.P, subject.R, subject.I, subject.RI]
        for f in methods:
            for n in range(12):
                # trfm = Tone Row Family Member
                trfm = f(n)
                for i in range(12):
                    # svar = Shift Variation
                    svar = trfm.shift(i)
                    self.assert_(rotequiv(self.testrow, svar))

    def test_not_rotequiv(self):
        a = ToneRow(range(12))
        # order is everything
        b = ToneRow(list(range(10)) + [11, 10])
        self.failIf(rotequiv(a, b))
