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
# $Id: test_noteops.py 191 2007-08-07 03:15:46Z mccosar $

"""
Test suite for noteops.py version 2 series -- Bruce H. McCosar

CORE as of version 2.0.0:

Tests may be added, but no test may be removed unless it is faulty.
Some tests exist only to ensure that all functions behave properly,
even if they are known to be mere shortcuts.  That may not be true
in future versions.
"""

__metaclass__ = type

import unittest
from pcsets.pcset import *
from pcsets.noteops import *


# Used in testing minimum conflict principle in notes() The only scale that
# deviates from standard is F#; since notes() can't turn the final F into 'E#'
# (natural notes are always natural notes), there will always be at least one
# conflict. Nor would it help to go to the Gb scale, which would require Cb.
PROPER_SCALE_FORMS="""
C D E F G A B        |
Db Eb F Gb Ab Bb C   |
D E F# G A B C#      |
Eb F G Ab Bb C D     |
E F# G# A B C# D#    |
F G A Bb C D E       |
F# G# A# B C# Eb F   |
G A B C D E F#       |
Ab Bb C Db Eb F G    |
A B C# D E F# G#     |
Bb C D Eb F G A      |
B C# D# E F# G# A#
""".split('|')

# Used in testing alternative scales. The definitive scale for that series
# should appear in an acceptable standard format. In order of appearance,
# they are: C melodic minor, A harmonic minor, and C harmonic major. These
# particular keys were chosen because in each case the scale has only one
# accidental -- and it had better be the right one.
ALTERNATIVE_SCALES="""
023579B = C D Eb F G A B |
9B02458 = A B C D E F G# |
024578B = C D E F G Ab B
""".split('|')


class PcForNoteTests(unittest.TestCase):

    def prep(self,c):
        return c.join(list("ABCDEFGx"))[:-2]

    # correct input, correct answer

    def test_natural(self):
        n = self.prep(' ')
        self.assertEqual(list(pcfor(n)),[9,11,0,2,4,5,7])

    def test_flats(self):
        f = self.prep('b ')
        self.assertEqual(list(pcfor(f)),[8,10,11,1,3,4,6])

    def test_sharps(self):
        s = self.prep('# ')
        self.assertEqual(list(pcfor(s)),[10,0,1,3,5,6,8])

    def test_unicode_flats(self):
        f = self.prep(u'\u266D ')
        self.assertEqual(list(pcfor(f)),[8,10,11,1,3,4,6])

    def test_unicode_sharps(self):
        s = self.prep(u'\u266F ')
        self.assertEqual(list(pcfor(s)),[10,0,1,3,5,6,8])

    def test_unicode_naturals(self):
        n = self.prep(u'\u266E ')
        self.assertEqual(list(pcfor(n)),[9,11,0,2,4,5,7])

    # empty string, correct answer

    def test_empty_string(self):
        self.assertEqual(list(pcfor('')),[])

    # bad input, exception

    def test_improper_spec_int(self):
        self.assertRaises(TranslationError,pcfor,42)

    def test_improper_spec_float(self):
        self.assertRaises(TranslationError,pcfor,4.2)

    def test_improper_spec_list(self):
        self.assertRaises(TranslationError,pcfor,[42])

    def test_improper_format_no_spaces(self):
        self.assertRaises(TranslationError,pcfor,'ABC')

    def test_improper_base_note(self):
        self.assertRaises(TranslationError,pcfor,'FGH')

    def test_improper_modifier_typo(self):
        self.assertRaises(TranslationError,pcfor,'AB C')

    def test_improper_modifier_double_flat(self):
        self.assertRaises(TranslationError,pcfor,'Abb C')

    def test_improper_modifier_double_sharp(self):
        self.assertRaises(TranslationError,pcfor,'A## C')

    def test_improper_modifier_jolly_roger(self):
        self.assertRaises(TranslationError,pcfor,u'A\u2620 C')


class NotesFromPcTests(unittest.TestCase):

    def setUp(self):
        self.chrom = PcSet(range(12))

    # correct input, correct answer.

    def test_pcs_flatpref(self):
        self.assertEqual(notes(self.chrom,pref='b'),
                         'C Db D Eb E F Gb G Ab A Bb B')

    def test_pcs_sharppref(self):
        self.assertEqual(notes(self.chrom,pref='#'),
                         'C C# D D# E F F# G G# A A# B')

    def test_pcs_flatpref_unicode(self):
        self.assertEqual(notes(self.chrom,pref=u'\u266D'),
             u'C D\u266d D E\u266d E F G\u266d G A\u266d A B\u266d B')

    def test_pcs_sharppref_unicode(self):
        self.assertEqual(notes(self.chrom,pref=u'\u266F'),
             u'C C\u266f D D\u266f E F F\u266f G G\u266f A A\u266f B')

    # Part of my specification is that notes() must also handle lists and spec
    # strings. In case something subtle changes in the module, these tests
    # will catch the breakage.

    def test_list_compatibility(self):
        self.assertEqual(notes(range(12)),notes(self.chrom))

    def test_spec_compatibility(self):
        self.assertEqual(notes('0123456789AB'),notes(self.chrom))    

    # Minimum Conflict. There are a few 'worked example' sets that should give
    # an obvious, consistent answer. The more tests here, the better.

    def test_minconf_original(self):
        # The set where the whole idea started.
        pcs = PcSet('AB01')
        answer = 'A# B C Db' # 0 namespace conflicts.
        self.assertEqual(notes(pcs),answer)

    def test_minconf_neighbor1(self):
        # Tests neighbor conflict in an ordered set, part 1.
        pcs = PcSet('AB9')
        answer = 'A# B A' # 1 conflict.
        # 'Bb B A' also has 1 conflict, but A is not neighboring.
        # Therefore B pushes Bb to A#, a less popular note.
        self.assertEqual(notes(pcs),answer)

    def test_minconf_neighbor2(self):
        # Tests neighbor conflict in an ordered set, part 2.
        pcs = PcSet('9AB')
        answer = 'A Bb B' # 1 inescapable conflict w/neighbors.
        # Compare to above.  Deciding factor is popularity.
        self.assertEqual(notes(pcs),answer)

    def test_minconf_inescapable1(self):
        # 1 conflict no matter what.
        pcs = PcSet('0134')
        answer = 'C Db Eb E'
        # 'C C# D# E' also valid, but not as popular.
        # 'C Db D# E' also technically valid, but double accidental ugly.
        # Worst answer = 'C C# Eb E' (2 conflicts)
        self.assertEqual(notes(pcs),answer)

    def test_minconf_inescapable2(self):
        # 1 conflict no matter what.
        pcs = PcSet('5689')
        answer = 'F F# G# A'
        # Similar to test above.
        # Screening against double accidental 'Gb G#'
        self.assertEqual(notes(pcs),answer)
   
    def test_minconf_inescapable3(self):
        # 1 conflict no matter what.
        pcs = PcSet('78AB')
        answer = 'G Ab Bb B'
        # Similar to test above.
        # Screening against double accidental 'Ab A#'
        self.assertEqual(notes(pcs),answer)

    # Principle: Minimum Conflict should reproduce the flat and sharp signs
    # in the 12 possible major scales. Reasoning: the note names were chosen
    # for minimum conflict in the first place. The only scale that won't work
    # should be F#/Gb (F# would require F = E#, Gb would require B = Cb -- but
    # natural notes are always natural notes in this module.

    def test_major_scale_reproduction(self):
        majorscale = PcSet('024579B')
        for n in range(12):
            answer = PROPER_SCALE_FORMS[n].strip()
            self.assertEqual(notes(majorscale.T(n)),answer)

    # Principle: Minimum Conflict should produce reasonable results for
    # these three alternative scales, which are often defined by putting
    # a single accidental in a particular major or minor key.

    def test_alternative_scale_reproduction(self):
        for entry in ALTERNATIVE_SCALES:
            spec = [e.strip() for e in entry.split('=')]
            self.assertEqual(notes(spec[0]),spec[1])

    # bad input, exception

    def test_improper_input_int(self):
        self.assertRaises(DefinitionError,notes,42)

    def test_improper_input_float(self):
        self.assertRaises(DefinitionError,notes,4.2)

    def test_improper_input_string(self):
        self.assertRaises(DefinitionError,notes,'01E')

    # empty input, no problem

    def test_empty_pcs(self):
        pcs = PcSet([])
        self.assertEqual(notes(pcs),'')

    def test_empty_list(self):
        pcs = PcSet([])
        self.assertEqual(notes([]),'')

    def test_empty_spec(self):
        self.assertEqual(notes(''),'')
