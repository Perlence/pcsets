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
# $Id: test_pcops.py 191 2007-08-07 03:15:46Z mccosar $

"""
Test suite for pcops.py version 2 series -- Bruce H. McCosar

CORE as of version 2.0.0:

Tests may be added, but no test may be removed unless it is faulty.
Some tests exist only to ensure that all functions behave properly,
even if they are known to be mere shortcuts.  That may not be true
in future versions.
"""

__metaclass__ = type

import unittest
from functools import reduce

from pcsets.pcset import PcSet
from pcsets.pcops import *


class Equality(unittest.TestCase):

    def setUp(self):
        self.cscale = PcSet("024579B")
        self.ionian = PcSet("024579B")
        self.phrygian = PcSet("4579B02")
        self.jazzminor = PcSet("023579B")
        self.majortriad = PcSet("047")
        self.minortriad = PcSet("037")
        self.diminished = PcSet("0235689B")

    def test_exact_equality_yes(self):
        self.assert_(exact_equality(self.cscale, self.ionian))

    def test_exact_equality_no(self):
        self.failIf(exact_equality(self.ionian, self.phrygian))

    def test_set_equality_yes(self):
        self.assert_(set_equality(self.cscale, self.phrygian))

    def test_set_equality_no(self):
        self.failIf(set_equality(self.cscale, self.jazzminor))

    def test_same_prime_yes(self):
        self.assert_(same_prime(self.majortriad, self.minortriad))

    def test_same_prime_no(self):
        self.failIf(same_prime(self.majortriad, self.diminished))


class TransformationRelationships(unittest.TestCase):

    def setUp(self):
        self.cmaj = PcSet('047')
        self.amaj = PcSet('914')
        self.cmin = PcSet('037')
        self.caug = PcSet('048')        # symmetry 3
        self.cscale = PcSet('024579B')  # symmetry 1
        self.c7b5 = PcSet('046A')       # symmetry 2
        self.dim = PcSet('0369')        # symmetry 4

    def fulltest(self, a, b, expected_Tn, expected_TnI):
        result = op_path(a, b)
        self.assertEqual(result.Tn, expected_Tn)
        self.assertEqual(result.TnI, expected_TnI)

    def test_op_path_none(self):
        self.fulltest(self.cmaj, self.caug, [], [])

    def test_op_path_Tn(self):
        self.fulltest(self.cmaj, self.amaj, [9], [])

    def test_op_path_TnI(self):
        self.fulltest(self.cmaj, self.cmin, [], [7])

    def test_symmetry(self):
        trials = [
            self.cmaj,
            self.cscale,
            self.c7b5,
            self.caug,
            self.dim
            ]
        for x in range(5):
            self.assertEqual(symmetry(trials[x]), x)

    def test_op_path_symmetry1(self):
        bscale = self.cscale.T(11)
        self.fulltest(self.cscale, bscale, [11], [3])

    def test_op_path_symmetry2(self):
        d7b5 = self.c7b5.T(2)
        self.fulltest(self.c7b5, d7b5, [2, 8], [0, 6])

    def test_op_path_symmetry3(self):
        baug = self.caug.T(11)
        self.fulltest(self.caug, baug, [3, 7, 11], [3, 7, 11])

    def test_op_path_symmetry4(self):
        self.fulltest(self.dim, self.dim.T(1), [1, 4, 7, 10], [1, 4, 7, 10])

    def test_rel_Tn(self):
        self.assert_(rel_Tn(self.cmaj, self.amaj))

    def test_rel_TnI(self):
        self.assert_(rel_TnI(self.cmaj, self.cmin))


class SetOperations(unittest.TestCase):

    def test_union(self):
        """
        Tests union by constructing the chromatic scale from 8 transposed
        major chords. (Cmaj -> Fmaj -> ... -> Bmaj)
        """
        maj = PcSet('047')
        circle = [maj.T(n*5) for n in range(8)]
        chromo = reduce(union, circle)
        self.assertEqual(set(chromo), set(range(12)))

    def test_common(self):
        """
        Very similar to the test applied to cvec in test_pcset.py: finds the
        common tone vector, then makes sure the common tones are actually
        there for each value of TnI.
        """
        c = PcSet('024579B')
        cvec = c.cvec()
        for n in range(12):
            self.assertEqual(len(common(c, c.TnI(n))), cvec[n])


class SetRelationships(unittest.TestCase):

    def setUp(self):
        self.cmaj = PcSet('047')
        self.caug = PcSet('048')
        self.cscale = PcSet('024579B')
        self.blackkeys = self.cscale.complement()
        self.c7 = PcSet('047A')

    def test_is_complement(self):
        self.assert_(is_complement(self.cscale, self.blackkeys))

    def test_is_prime_complement(self):
        mixedup = self.blackkeys.TnI(3)
        self.failIf(is_complement(self.cscale, mixedup))
        self.assert_(is_prime_complement(self.cscale, mixedup))

    def test_subset_of(self):
        self.assert_(subset_of(self.cscale, self.cmaj))

    def test_prime_subset_of(self):
        self.failIf(subset_of(self.cscale, self.blackkeys))
        self.assert_(prime_subset_of(self.cscale, self.blackkeys))

    def test_not_prime_subset(self):
        self.failIf(prime_subset_of(self.cscale, self.caug))

    def test_fit_in_1(self):
        result = fit_in(self.cscale, self.cmaj)
        self.assertEqual(result.Tn, [0, 5, 7])
        self.assertEqual(result.TnI, [4, 9, 11])

    def test_harmonize_1(self):
        result = harmonize(self.cscale, self.cmaj)
        self.assertEqual(result.Tn, [0, 5, 7])
        self.assertEqual(result.TnI, [4, 9, 11])

    def test_fit_in_2(self):
        result = fit_in(self.cscale, self.c7)
        self.assertEqual(result.Tn, [7])
        self.assertEqual(result.TnI, [9])

    def test_harmonize_2(self):
        result = harmonize(self.cscale, self.c7)
        self.assertEqual(result.Tn, [5])
        self.assertEqual(result.TnI, [9])

    # added Opset.__str__() in 2.0.0b3

    def test_OpSet_string_1(self):
        result = fit_in(self.cscale, self.c7)
        self.assertEqual(str(result), 'T(7) T(9)I')

    def test_OpSet_string_2(self):
        result = harmonize(self.cscale, self.c7)
        self.assertEqual(str(result), 'T(5) T(9)I')

    def test_OpSet_string_3(self):
        # An augmented triad can't fit in the major scale.
        result = fit_in(self.cscale, self.caug)
        self.assertEqual(str(result), 'None')


class Similarity(unittest.TestCase):

    def setUp(self):
        self.a = PcSet('9047B2')
        self.b = PcSet('047B25')
        self.c = self.b.TnI(9)
        self.d = PcSet('9048AB')
        self.forte42 = PcSet([0, 1, 2, 4])
        self.forte413 = PcSet([0, 1, 3, 6])
        self.forte43 = PcSet([0, 1, 3, 4])
        self.forte510 = PcSet([0, 1, 3, 4, 6])
        self.forte5Z12 = PcSet([0, 1, 3, 5, 6])
        self.forte5Z36 = PcSet([0, 1, 2, 4, 7])

    def test_Rp_yes(self):
        self.assert_(Rp(self.a, self.b))

    def test_Rp_no(self):
        self.failIf(Rp(self.a, self.c))

    def test_Rp_prime_yes(self):
        self.assert_(Rp_prime(self.a, self.c))

    def test_Rp_path(self):
        result = Rp_path(self.a, self.c)
        self.assertEqual(result.Tn, [5, 10])
        self.assertEqual(result.TnI, [4, 9])

    def test_Rp_prime_no(self):
        self.failIf(Rp_prime(self.a, self.d))

    def test_R0_yes(self):
        self.assert_(R0(self.forte42, self.forte413))

    def test_R0_no(self):
        self.failIf(R0(self.forte42, self.forte43))

    def test_R1_yes(self):
        self.assert_(R1(self.forte42, self.forte43))

    def test_R1_no(self):
        self.failIf(R1(self.forte42, self.forte413))

    def test_R2_yes(self):
        self.assert_(R2(self.forte510, self.forte5Z12))

    def test_R2_no_actually_R0(self):
        self.failIf(R2(self.forte42, self.forte413))

    def test_R2_no_actually_R1(self):
        self.failIf(R2(self.forte42, self.forte43))

    def test_Zpair_yes(self):
        self.assert_(Zpair(self.forte5Z12, self.forte5Z36))

    def test_Zpair_no(self):
        self.failIf(Zpair(self.forte5Z12, self.forte510))


class EmptyOperationTests(unittest.TestCase):

    def setUp(self):
        self.a = PcSet([])
        self.b = PcSet([])
        self.chromo = PcSet(range(12))

    def test_exact_equality(self):
        self.assert_(exact_equality(self.a, self.b))

    def test_set_equality(self):
        self.assert_(set_equality(self.a, self.b))

    def test_same_prime(self):
        self.assert_(same_prime(self.a, self.b))

    def test_op_path(self):
        result = op_path(self.a, self.b)
        self.assertEqual(result.Tn, list(range(12)))
        self.assertEqual(result.TnI, list(range(12)))

    def test_symmetry(self):
        self.assertEqual(symmetry(self.a), 12)

    def test_union(self):
        self.assert_(exact_equality(union(self.a, self.b), self.a))

    def test_common(self):
        self.assert_(exact_equality(common(self.a, self.b), self.a))

    def test_is_complement(self):
        self.assert_(is_complement(self.a, self.chromo))

    def test_is_prime_complement(self):
        self.assert_(is_prime_complement(self.a, self.chromo))

    def test_subset_of(self):
        self.assert_(subset_of(self.a, self.b))

    def test_prime_subset_of(self):
        self.assert_(subset_of(self.a, self.b))

    def test_fit_in(self):
        result = fit_in(self.a, self.b)
        self.assertEqual(result.Tn, list(range(12)))
        self.assertEqual(result.TnI, list(range(12)))

    def test_harmonize(self):
        result = harmonize(self.a, self.b)
        self.assertEqual(result.Tn, list(range(12)))
        self.assertEqual(result.TnI, list(range(12)))

    def test_Rp(self):
        self.failIf(Rp(self.a, self.b))

    def test_Rp_prime(self):
        # indirectly tests Rp_path as well
        self.failIf(Rp_prime(self.a, self.b))

    def test_R0(self):
        self.failIf(R0(self.a, self.b))

    def test_R1(self):
        self.failIf(R1(self.a, self.b))

    def test_R2(self):
        self.failIf(R2(self.a, self.b))

    def test_Zpair(self):
        self.assert_(Zpair(self.a, self.b))
