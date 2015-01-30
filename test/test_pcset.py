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
# $Id: test_pcset.py 191 2007-08-07 03:15:46Z mccosar $

"""
Test suite for pcset.py version 2 series -- Bruce H. McCosar

This test suite is really thorough, and sometimes analyzes functions from
basic principles, just as a sanity check on the system.

CORE as of version 2.0.0:

Tests may be added, but no test may be removed unless it is faulty.
Some tests exist only to ensure that all functions behave properly,
even if they are known to be mere shortcuts.  That may not be true
in future versions.
"""

__metaclass__ = type

import unittest

from pcsets.pcset import *


class BasicServices(unittest.TestCase):

    def setUp(self):
        self.s = '9B12468'
        self.i = [9,11,1,2,4,6,8]

    # correct input, correct output

    def test_from_string_to_string(self):
        pcs = PcSet(self.s)
        self.assertEqual(str(pcs),self.s)

    def test_from_string_to_list(self):
        pcs = PcSet(self.s)
        self.assertEqual(list(pcs),self.i)

    def test_from_list_to_string(self):
        pcs = PcSet(self.i)
        self.assertEqual(str(pcs),self.s)

    def test_from_list_to_list(self):
        pcs = PcSet(self.i)
        self.assertEqual(list(pcs),self.i)

    def test_from_string_get_len(self):
        pcs = PcSet(self.s)
        self.assertEqual(len(pcs),7)

    def test_from_list_get_len(self):
        pcs = PcSet(self.i)
        self.assertEqual(len(pcs),7)

    # unusual input, correct output

    def test_remove_duplicates(self):
        pcs = PcSet('01AAAA')
        self.assertEqual(list(pcs),[0,1,10])

    def test_convert_floats(self):
        pcs = PcSet([0,1,2.2,3.1415])
        self.assertEqual(list(pcs),[0,1,2,3])

    def test_empty_string(self):
        pcs = PcSet('')
        self.assertEqual(list(pcs),[])

    def test_empty_list(self):
        pcs = PcSet([])
        self.assertEqual(str(pcs),'')

    # incorrect input

    def test_incorrect_string(self):
        self.assertRaises(DefinitionError,PcSet,'01E')

    def test_incorrect_list(self):
        self.assertRaises(DefinitionError,PcSet,[0,1,'a'])

    def test_non_iterable(self):
        self.assertRaises(DefinitionError,PcSet,25)

    def test_accidental_space(self):
        self.assertRaises(DefinitionError,PcSet,'047 9')


class FundamentalMethods(unittest.TestCase):

    def setUp(self):
        self.pcs = PcSet('0146')

    # These also test the __iter__ method, indirectly

    def test_inverse(self):
        """
        Test the principle that, for a given pcset, the sum of the
        corresponding elements in the original and the inverse will
        always be 0 (in mod 12 arithmetic).
        """
        inv = self.pcs.invert()
        self.assertEqual(len(self.pcs),len(inv))
        for n,i in zip(self.pcs,inv):
            self.assertEqual((n+i)%12,0)

    def test_transpose(self):
        """
        Tests the principle that, for a given pcset, the difference
        between the corresponding element in the original and the
        transposed version will always be equal to the transposition
        amount (in mod 12 arithmetic).
        """
        for x in range(12):
            trx = self.pcs.transpose(x)
            self.assertEqual(len(self.pcs),len(trx))
            for n,t in zip(self.pcs,trx):
                self.assertEqual((t-n)%12,x%12)

    def test_transpose_float(self):
        trf = self.pcs.transpose(3.6)
        for n,t in zip(self.pcs,trf):
            self.assertEqual((t-n)%12,3)

    def test_transpose_empty(self):
        es = PcSet([])
        self.assertEqual(list(es.transpose(3)),[])


class SetOperations(unittest.TestCase):

    def setUp(self):
        self.amaj = PcSet('9B12468')
        self.empty = PcSet([])
        self.chromatic = PcSet(range(12))
        self.g7 = PcSet('7B25')

    # complement

    def test_complement(self):
        """
        Tests the principle that the union of the original set and its
        complement should be the chromatic set.
        """
        fsm5 = self.amaj.complement()
        self.assertEqual(len(fsm5)+len(self.amaj),12)
        chromatic = PcSet(list(self.amaj)+list(fsm5))
        self.assertEqual(len(chromatic),12)

    def test_complement_chromatic(self):
        empty = self.chromatic.complement()
        self.assertEqual(list(empty),[])

    def test_complement_empty_set(self):
        chromatic = self.empty.complement()
        self.assertEqual(list(chromatic),range(12))

    # reverse

    def test_reverse(self):
        n = list(self.amaj)
        r = list(self.amaj.reverse())
        size = len(n)
        self.assertEqual(size,len(r))
        for x in range(size):
            self.assertEqual(n[x],r[size-1-x])

    def test_reverse_empty(self):
        r = self.empty.reverse()
        self.assertEqual(list(r),[])

    # sort

    def test_sort(self):
        csphryg = self.amaj.sort()
        self.assertEqual(str(csphryg),'124689B')

    def test_sort_empty(self):
        es = self.empty.sort()
        self.assertEqual(list(es),[])

    # shift

    def test_shift(self):
        arotations = []
        for x in range(len(self.amaj)):
            arotations.append(self.amaj.shift(x))
        lastelements = []
        for pcs in arotations:
            lastnote = list(pcs).pop()
            lastelements.append(lastnote)
        lastelements.reverse()
        self.assertEqual(list(self.amaj),lastelements)

    def test_shift_empty(self):
        es = self.empty.shift(3)
        self.assertEqual(list(es),[])

    # zero

    def test_zero(self):
        cmaj = self.amaj.zero()
        self.assertEqual(str(cmaj),'024579B')

    def test_zero_empty(self):
        es = self.empty.zero()
        self.assertEqual(list(es),[])

    # normal

    def test_normal(self):
        g7n = self.g7.normal()
        self.assertEqual(list(g7n),[11,2,5,7])

    def test_normal_empty(self):
        es = self.empty.normal()
        self.assertEqual(list(es),[])

    # reduced

    def test_reduced(self):
        amajchord = PcSet([9,1,4])
        self.assertEqual(list(amajchord.reduced()),[0,4,7])

    # prime

    def test_prime_1(self):
        maj = self.amaj.prime()
        self.assertEqual(str(maj),'013568A')

    def test_prime_2(self):
        m7b5 = self.g7.prime()
        self.assertEqual(str(m7b5),'0258')

    def test_prime_empty(self):
        es = self.empty.prime()
        self.assertEqual(list(es),[])


class SetAnalysis(unittest.TestCase):

    def setUp(self):
        self.amaj = PcSet('9B12468')
        self.empty = PcSet([])

    # ivec

    def test_ivec_ait1(self):
        ait1 = PcSet('0146')
        self.assertEqual(ait1.ivec(),[1]*6)

    def test_ivec_ait2(self):
        ait2 = PcSet('0137')
        self.assertEqual(ait2.ivec(),[1]*6)

    def test_ivec_empty(self):
        self.assertEqual(self.empty.ivec(),[0]*6)

    # cvec

    def test_cvec(self):
        """
        Tests the fundamental definition of cvec: that a given value at
        index n will be the number of common tones for the operation TnI.
        """
        cvec = self.amaj.cvec()
        for n in range(12):
            original = set(self.amaj)
            transformed = set(self.amaj.invert().transpose(n))
            common_tones = len(original & transformed)
            self.assertEqual(common_tones,cvec[n])

    def test_cvec_empty(self):
        self.assertEqual(self.empty.cvec(),[0]*12)


class ShorthandMethods(unittest.TestCase):

    def setUp(self):
        self.pcs = PcSet('0146')

    def test_T(self):
        a = self.pcs.T(3)
        b = self.pcs.transpose(3)
        self.assertEqual(list(a),list(b))

    def test_I(self):
        a = self.pcs.I()
        b = self.pcs.invert()
        self.assertEqual(list(a),list(b))

    def test_TnI(self):
        a = self.pcs.TnI(3)
        b = self.pcs.invert().transpose(3)
        self.assertEqual(list(a),list(b))

    def test_Ixy(self):
        """
        Tests the principle that the two specified pitches should transform
        into each other.
        """
        n = list(self.pcs)
        a = list(self.pcs.Ixy(1,4))
        b = list(self.pcs.invert().transpose(5))
        self.assertEqual(a,b)
        self.assertEqual(a[1],n[2])
        self.assertEqual(a[2],n[1])
