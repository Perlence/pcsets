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
# $Id: noteops.py 191 2007-08-07 03:15:46Z mccosar $

"""
noteops.py -- version 2.0 -- Bruce H. McCosar

Note operations:

A module that provides translation functions between named notes (for example,
'C Eb G') and pitch class sets (PcSet objects).

    pcfor(s)   : return the equivalent PcSet for the named notes in s.

    notes(pcs) : return the equivalent named notes for the PcSet pcs.

The function 'notes' can even handle lists of integers and raw pitch class set
specification strings (such as '0135A').


Example 1: PcSet from written list of notes, in this case a Cm69 chord.

    >>> from pcsets.pcset import *
    >>> from pcsets.noteops import *
    >>> cm69 = pcfor('C Eb G A D')
    >>> print cm69
    03792

Example 2: Written notes from a PcSet.

    >>> print notes(cm69)
    C Eb G A D

Example 3: 'notes' flexibility.

    >>> print notes('03792')
    C Eb G A D


CORE as of version 2.0.0 -- new functionality may occasionally be added,
and bugs will be fixed, but the interface defined here will not change
in the entire version 2 series.
"""


__metaclass__ = type

__all__ = """
TranslationError
pcfor
notes
""".split()

from .pcset import PcSet, PcSetException

# If this is set to True, then the minconflict function will terminate with an
# exception when the first three rules fail to narrow a PcSet down to a single
# string option.  It was used in developing the scoring rules.
PERFECTION_TESTING = False


UFLAT = u"\u266D"
UNATURAL = u"\u266E"
USHARP = u"\u266F"

CSCALE = list("C-D-EF-G-A-B")


# Accidentals sorted from least popular to most popular. Popularity value is
# numerical index in the list; see discussion in minconflict(pcs)
RANKING = """
A#
Gb
D#
Db
G#
Ab
C#
Eb
F#
Bb
""".split()


class TranslationError(PcSetException):
    """
    Most exceptions thrown during translation will be a subclass
    of this.  However, the 'notes' function calls PcSet() -- bad
    input will return pcset.DefinitionError subclasses.
    """


class NonStringError(TranslationError):
    """
    Argument must be a space-separated string of notes.
    The problem found was: %(x)s %(type)s
    """
    def __init__(self, x):
        f = {'x': x, 'type': type(x)}
        self.message = self.__doc__ % f


class NoteFormatError(TranslationError):
    """
    Notes must consist of a single capital letter A-G and possibly
    a single sharp or flat -- two characters maximum.  Remember that
    notes must be separated by spaces.
    The problem found was: %(problem)r
    """
    def __init__(self, s):
        self.message = self.__doc__ % {'problem': s}


class IllegalNoteError(TranslationError):
    """
    The base note must be a capital letter from A to G.
    The problem found was: %(problem)r
    """
    def __init__(self, s):
        self.message = self.__doc__ % {'problem': s}


class IllegalModifierError(TranslationError):
    """
    The only valid accidentals are 'b' for flat, '#' for sharp,
    and the unicode characters for flat, sharp, and natural.
    Also, notes must be separated by spaces.
    The illegal modifier found was: %(problem)r in %(setting)r
    """
    def __init__(self, p, s):
        self.message = self.__doc__ % {'problem': p, 'setting': s}


class PerfectionTestingFailure(PcSetException):
    """
    The first three minimum conflict rules failed to narrow the possible
    output strings to a single clear winner. This normally does not cause an
    exception. The problem is only caught when PERFECTION_TESTING is set to
    true within the module, which shouldn't be the case for most users (unless
    you're working on the code).

    The problem: pcset %(problemset)s returned too many strings:
    %(stringlist)s
    """
    def __init__(self, pcs, options):
        f = {'problemset': pcs, 'stringlist': options}
        self.message = self.__doc__ % f


def pitchclass_of(note):
    """
    A utility function that translates a character specification of
    a note into a numeric pitch class.
    """
    # Handles Cbb and D## errors.
    if len(note) > 2:
        raise NoteFormatError(note)
    # There's only one character that can sneak through the algorithm
    if note[0] == '-':
        raise IllegalNoteError(note)
    # First the base...
    try:
        base = CSCALE.index(note[0])
    except ValueError:
        raise IllegalNoteError(note)
    # ...then the modifiers
    try:
        accidental = note[1]
    except IndexError:
        accidental = ''
    # Now apply them if necessary.
    if accidental:
        if accidental == 'b' or accidental == UFLAT:
            base -= 1
        elif accidental == '#' or accidental == USHARP:
            base += 1
        elif accidental == UNATURAL:
            pass
        else:
            raise IllegalModifierError(accidental, note)
    return base


def pcfor(spec):
    """
    Translates a space-separated string of notes into a PcSet. As is standard,
    C = 0, C#/Db = 1, and so on, all the way to B = 11.

    The capital letters A through G are respected; 'b' stands for flat, and
    '#' for sharp. Double flats and double sharps are not permitted.

    If the string given is unicode and contains flat (U+266D) or sharp
    (U+266F), the symbols are respected as normal specifiers.

    If for some reason the natural (U+266E) is given, it's silently ignored.
    This function always regards a note such as 'B' as pitch class 11, even
    if it is preceded in the list by an altered version of itself (Bb or B#).
    Therefore a natural sign is not necesary.

    If other unicode symbols are encountered, such as double sharp or double
    flat, it will trigger an exception, and I have to say you asked for it.
    """
    try:
        notelist = spec.split()
    except AttributeError:
        raise NonStringError(spec)
    return PcSet([pitchclass_of(note) for note in notelist])


def flat(pc):
    """
    Utility function.  Black key pc's are returned as flat notes.
    """
    note = CSCALE[pc]
    if note == '-':
        note = CSCALE[pc+1] + 'b'
    return note


def sharp(pc):
    """
    Utility function.  Black key pc's are returned as sharp notes.
    """
    note = CSCALE[pc]
    if note == '-':
        note = CSCALE[pc-1] + '#'
    return note


def conflict(notestring):
    """
    Utility function. Conflict score starts at 0 and becomes more negative as
    more namespace collisions are found (eg B and Bb).  Discriminates harshly
    against triple hitters (eg Db D D#), making them count as five conflicts.
    """
    amount = 0
    for note in "CDEFGAB":
        sharednames = notestring.count(note)
        if sharednames == 2:
            amount -= 1
        elif sharednames > 2:
            amount -= 5
    return amount


def neighborconflict(notestring):
    """
    Utility function.  Neighbor Conflict score starts at 0 and becomes
    more negative as more neighbors are found with the same base note name.
    """
    amount = 0
    notes = notestring.split()
    for n in range(len(notes)-1):
        first = notes[n]
        second = notes[n+1]
        if first[0] == second[0]:
            amount -= 1
    return amount


def popularitycontest(notestring):
    """
    Utility function. 'Black key' notes have a 'popularity ranking', and the
    total score is just the sum of the individual popularities.
    """
    amount = 0
    for note in notestring.split():
        try:
            amount += RANKING.index(note)
        except ValueError:
            # not found
            pass
    return amount


def eliminate(items, based_on=None):
    """
    Utility function. A virtual contest -- eliminates items from a list if
    they don't have the best scores in the group. Only the items that scored
    the best are returned. The rest go off to loser land (probably the Garbage
    Collector waits outside this function with the truck engine running). The
    'based_on' function must return a numerical score -- high wins, low loses.
    """
    champion = items.pop()
    winningscore = based_on(champion)
    winners_circle = [champion]
    for challenger in items:
        score = based_on(challenger)
        if score > winningscore:
            # Win.  Take over winner's circle.
            winners_circle = [challenger]
            winningscore = score
        elif score == winningscore:
            # Tie.  Join the winner's circle.
            winners_circle.append(challenger)
        else:
            # LOSER!
            pass
    return winners_circle


def minconflict(pcs):
    """
    Utility function. Generates every possible permutation for sharp and flat
    note names for the 'black key' notes, then decides which one leads to the
    least name conflict using an ordered series of criteria:

    1. Count the number of name conflicts in each string (example, 'B Bb').
       Pass on only those strings which have the least conflicts.

    2. To decide between strings with equal conflicts, count the number that
       involve neighboring notes. Example: 'Bb B C' = 1, 'Bb C B' = 0.  Pass
       on only those strings which have the fewest conflicting neighbors.

    3. Finally, if there are still choices, assign each string a 'popularity
       grade' based on how often the accidental appears in music.

       As the key signature changes from C to G, F# appears; from G to D, C#
       appears. Therefore the sharp ranking is:

           F# > C# > G# > D# > A#

       For flats, as the signature changes from C to F, Bb appears; from F to
       Bb, Eb appears.  Therefore the flat ranking is:

           Bb > Eb > Ab > Db > Gb

       To make ties less likely, the flats are valued slightly more than the
       sharps of equivalent rank . . . horn players would probably agree.

    4. As an absolute last ditch attempt, if all else fails, the function
       sorts the remaining strings and picks the one that comes first.
    """
    # permutations
    options = [[]]  # seed for an expandable list of lists
    for pc in pcs:
        if CSCALE[pc] != '-':
            # natural note
            [s.append(CSCALE[pc]) for s in options]
        else:
            # accidental, list doubles in size.
            build = []
            for choice in flat(pc), sharp(pc):
                # deep copy
                wcopy = [list(s) for s in options]
                [s_copy.append(choice) for s_copy in wcopy]
                build.extend(wcopy)
            options = build
    # Transform into a list of strings.
    options = [' '.join(notelists) for notelists in options]
    # RANKING: a single item should bypass all remaining tests.
    # Tests will be popped from the end in order.
    ranking_functions = [
        popularitycontest,  # least important
        neighborconflict,
        conflict            # most important
        ]
    while len(options) > 1:
        try:
            contest = ranking_functions.pop()
        except IndexError:
            # no more tests!
            break
        options = eliminate(options, based_on=contest)
    if len(options) > 1:
        # algorithm perfection testing (optional)
        if PERFECTION_TESTING:
            raise PerfectionTestingFailure(pcs, options)
        # alphabetical order ;-) ...the last resort.
        options.sort()
    return options[0]


def notes(pcslist, pref=''):
    """
    This function takes a PcSet or a list of numeric pitch classes and
    translates it into a human-readable string of note names. Optionally, it
    understands PcSet specification strings as well -- provided A is used for
    10 and B for 11 (same as the string output of PcSet).

    The space-separated notes returned are formatted in several ways,
    depending on the setting the 'pref' parameter:


        pref = ''  (not set)  : (default) 'minimum conflict' setting.
                                 See the discussion below.

        pref = 'b' (flats)    : 'all flats' setting.
                                 Flats are chosen.  The 'black key' notes
                                 are always Db, Eb, Gb, Ab, and Bb.

        pref = '#' (sharps)   : 'all sharps' setting.
                                 Sharps are chosen.  The 'black key' notes
                                 are always C#, D#, F#, G#, and A#

        pref = u"" (unicode)  : See the 'unicode' discussion below.
                                 The unicode sharp and flat characters
                                 are legal substitutes for '#' and 'b'

        pref = (anything else): UNDEFINED. Who knows what the future holds?


    THE 'MINIMUM CONFLICT' SETTING:

    Note names are chosen to minimize the sharing of names with accidentals.
    For example, 'A# B C Db' would be chosen over 'Bb B C Db', 'A# B C C#', or
    (worst of all) 'Bb B C C#'. This applies only to the 'black key' notes --
    natural-named notes always appear as themselves.


    UNICODE

    If the pref is set to the unicode character for the flat symbol (U+266D)
    or the sharp symbol (U+266F), these are respected as the normal ASCII
    specifiers above. The returned string will be unicode as well, using the
    correct unicode symbols.

    To specify default behavior (minimum conflict, see below) but unicode
    results, set pref=u"" (the unicode empty string). Additionally, if the
    input to the function is a unicode spec string (for instance, u'037'),
    this will also trigger unicode output.
    """
    # gatekeeper
    pcs = PcSet(pcslist)
    # accidental preference
    if pref == 'b' or pref == UFLAT:
        stringform = ' '.join([flat(pc) for pc in pcs])
    elif pref == '#' or pref == USHARP:
        stringform = ' '.join([sharp(pc) for pc in pcs])
    else:
        stringform = minconflict(pcs)
    # final formatting
    if type(pref) == type(u"") or type(pcslist) == type(u""):
        stringform = stringform.replace('b', UFLAT)
        stringform = stringform.replace('#', USHARP)
    return stringform


if __name__ == '__main__':
    print "\nDifferent interpretations of the chromatic scale:\n"
    print "\t>>> from pcsets.pcset import PcSet"
    print "\t>>> from pcsets.noteops import notes, pcfor"
    print "\t>>> chromatic = PcSet(range(12))"
    print "\t>>> print notes(chromatic, pref='b')"
    print "\t", notes(range(12), pref='b')
    print "\t>>> print notes(range(12),pref='#') # notes() handles pc lists"
    print "\t", notes(range(12), pref='#')
    print "\t>>> print notes(range(12))          # default 'minimum conflict'"
    print "\t", notes(range(12))
    print "\t>>> # noteops also allows you to convert from notes to pcsets."
    print "\t>>> print pcfor('C Db D Eb E F Gb G Ab A Bb B')"
    print "\t", pcfor('C Db D Eb E F Gb G Ab A Bb B'), "\n"

    print "Minimum conflict tries to select notes so there is minimum"
    print "namespace conflict between the note names. For example, pitch"
    print "class set 'AB01' can be rendered 4 ways: \n"
    print "\t'Bb B C Db', 'A# B C Db','Bb B C C#', or 'A# B C C#'\n"
    print "\t>>> print notes('AB01')      # notes() understands spec strings!"
    print "\t", notes('AB01'), "\n"
