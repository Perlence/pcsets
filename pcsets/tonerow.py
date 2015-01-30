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
# $Id: tonerow.py 207 2007-08-16 02:37:36Z mccosar $

"""
tonerow.py -- version 2.0 -- Bruce H. McCosar

Implements 12-tone rows. Based on pitch class sets, tone rows have operations
and terminology of their own.


BASIC DEFINITION

A tone row is an ordered set consisting of all 12 pitch classes.


TONE ROWS COMPARED TO PC SETS

The key concept is that a tone row is defined as an *ordered* set. In
contrast, pc sets are *unordered*. In the pc set world, there is no difference
between

    [9, 11, 10, 7, 3, 1, 8, 6, 0, 5, 4, 2]

and

    [4, 10, 8, 1, 3, 9, 5, 7, 2, 11, 6, 0]

They both are equivalent to the chromatic scale -- at first glance, nothing
special. Yet in tone row terms, these two have very little in common -- the
order is everything. For this reason:

  * There are only 224 prime pitch class sets, and

  * There are only 4096 distinct pitch class sets anyway; BUT

  * There are 12! (12 factorial) possible unique tone rows
    -- that's 479,001,600.


DISTINCT TONE ROW OPERATIONS

Unlike PcSets, when ToneRow methods take an argument 'n', this generally
means "Perform this operation and return the Tone Row having 'n' as its
first member." This is opposed to PcSets, where the argument is generally an
interval or a distance.

You can think of this as the difference between nouns and verbs; telling a
PcSet to .transpose(3) says "Take each element and do something -- add 3." On
the other hand, Tone Rows like to be asked, not told ;-) The method .RI(3)
says "If you were to take this set and reverse it, then invert it, what would
it look like if you transposed it so that the first element was 3?"


    FUNDAMENTAL TONE ROW METHODS
    (see method documentation for more info)

    P(n)     : prime
    R(n)     : retrograde
    I(n)     : inverted
    RI(n)    : retrograde-inverted

    shift(i),
    rotate(i,n):

    Return a new ToneRow with the elements shifted by 'i'; rotate
    goes a bit further and transposes the first pitch to 'n' after
    the shift.


Also provided in this package are specific tone row operations. Note that most
of the operations in pcsets.pcops are completely useless for ToneRows. For
example, if we take the tone row

    [8, 0, 5, 9, 1, 7, 10, 6, 2, 3, 11, 4]

and ask for RI(2) (the retrograde inverse with 2 as the first pitch), we get

    [2, 7, 3, 4, 0, 8, 11, 5, 9, 1, 6, 10]

Now, we know for certain these two are related. However, the first two
functions in pcsets.pcops shoot around the issue: exact_equality for these two
sets would return False, and set_equality would return true. Then again it
would also return True for PcSet(range(12)).

For this reason, the pcsets.tonerow module contains its own specific functions
for ToneRows.  These are not part of the class, but separate functions that
can be imported (or that are imported by default with * ):


    AVAILABLE TONE ROW OPERATIONS
    (see function documentation for more).

    equivalent(a,b)
    rotequiv(a,b)
    randomrow()


    [More operations are planned, but not yet implemented -- for example, a
    tonerow 'generator' function from pc sets, in the form f(pcs) -> ToneRow]


CAUTIONS

ToneRow inherits all the methods of its parent class, PcSet, then defines its
own specific methods. However, given the nature of tone rows, some of the
fundamental PcSet methods have to be redefined. Certain methods even become
pointless. Here's an overview:


    INHERITED PCSET METHODS

    Many of these methods will return a new PcSet, not a new ToneRow.
    Unless indicated specifically below, assume that any PcSet parent
    method returns a PcSet instance (in cases where a set is expected).


    FUNDAMENTAL METHODS

        invert(),
        transpose(n):

        Marginally useful; I(n) is defined differently for ToneRows,
        and transpose is implied by all the ToneRow operations anyway.

    SET OPERATIONS

        complement()      : Useless.  Always returns [].

        reverse()         : Still useful, but ToneRows use R(n).

        sort()            : Useless.  Equivalent to PcSet(range(12)).

        shift(i)          : Very Useful.  Duplicates Stravinsky's 'rotation'
                            function.  RETURNS A NEW TONEROW with the elements
                            shifted by 'i' places. See also the ToneRow method
                            rotate(i,n).

        zero()            : Equivalent to method P(0).

        normal(),
        reduced(),
        prime():

        Although these three are very useful for PcSets, for ToneRows, they
        are equivalent to PcSet(range(12)).

    SET ANALYSIS

        ivec()            : Useless. Always returns [12,12,12,12,12,6]

        cvec()            : Useless. Always returns [12] * 12

    SHORTHAND METHODS

        I(),
        T(n),
        TnI(n),
        Ixy(x,y):

        See notes for transpose and inverse above.

    IMPLIED METHODS

        len(pcs)          : Useless. Always returns 12.

        str(pcs)          : Useful to a point.  Viewing 12 pitch classes as a
                            long list (with commas and brackets) is not nearly
                            as compact as '52017B463A98'. (Compare to the
                            12 tone lists given as examples in the material
                            above, which took up half the line.)

                            Readability, on the other hand, is another matter!

        list(pcs)         : Like its parent class, the ability of a ToneRow
                            to function as an iterator makes it very flexible.


EXPERIMENTAL as of version 2.0:

This is not a core module; it's in development and
won't be stable until at least version 2.1
"""

__metaclass__ = type

__all__ ="""
ToneRow
equivalent
rotequiv
randomrow
ToneRowException
""".split()


from pcset import PcSet, PcSetException, moderate
from random import shuffle


class ToneRowException(PcSetException):
    """
    Any exception in the ToneRow module will be derived from this class.
    """
    pass


class IncompleteRowError(ToneRowException):
    """
    ToneRows must contain all 12 pitch classes.
    The problem found was:
        %(problem)r
    of length %(length)d
    """
    def __init__(self,problem):
        trouble = {
            'problem' : list(problem), # needed for helpful %r conversion.
            'length'  : len(problem)
            }
        self.message = self.__doc__ % trouble


def correct_transposition(pcs,n):
    """
    Utility function.  Takes an input PcSet and returns it with
    the first element transposed to n; n can even be a string,
    with A = 10 and B = 11 (other values cause an exception).
    """
    first_element = list(pcs)[0]
    return pcs.T(moderate(n)-first_element)


class ToneRow(PcSet):

    """
    ToneRow:

    A ToneRow is an ordered set consisting of all 12 pitch classes.
    The order of the elements is the most important thing.

    ToneRows have the following methods:

        P(n)
        R(n)
        I(n)
        RI(n)

    ToneRows also inherit methods from PcSet, but some of these are
    of little use with 12-tone constructs, which set operations tend
    to regard as just another chromatic scale.
    """

    def __init__(self,definition):
        """
        A ToneRow must be length 12.  It may be defined any way
        that a PcSet can:

            1. Through ToneRow([list of integers])
            2. Through ToneRow('spec string')
            3. And, indirectly through ToneRow(pcfor("list of notes"))
        """
        super(ToneRow,self).__init__(definition)
        if len(self) < 12:
            raise IncompleteRowError(self)

    def P(self,n):
        """
        PRIME (ToneRow operation)

        Returns a new ToneRow with the pitches in the same order as the
        original, but transposed so that 'n' is the first note.

        Note that, for convenience and consistency, you are allowed to
        input string values 'A' for 10 and 'B' for 11.  Any other strings
        will trigger an IllegalCharacter exception.
        """
        return ToneRow(correct_transposition(self,n))

    def R(self,n):
        """
        RETROGRADE (ToneRow operation)

        Returns a new ToneRow with the pitches in reverse order compared to
        the original, but transposed so that 'n' is the first note.

        Note that, for convenience and consistency, you are allowed to
        input string values 'A' for 10 and 'B' for 11.  Any other strings
        will trigger an IllegalCharacter exception.
        """
        return ToneRow(correct_transposition(self.reverse(),n))

    def I(self,n):
        """
        INVERSE (ToneRow operation)

        Returns a new ToneRow with the original pitches inverted, but
        transposed so that 'n' is the first note.

        Note that, for convenience and consistency, you are allowed to input
        string values 'A' for 10 and 'B' for 11. Any other strings will
        trigger an IllegalCharacter exception.
        """
        return ToneRow(correct_transposition(self.invert(),n))

    def RI(self,n):
        """
        RETROGRADE INVERSE (ToneRow operation)

        Returns a new ToneRow with the pitches inverted, in reverse order
        compared to the original, and transposed so that 'n' is the first
        note.

        Note that, for convenience and consistency, you are allowed to input
        string values 'A' for 10 and 'B' for 11. Any other strings will
        trigger an IllegalCharacter exception.
        """
        ri = self.invert().reverse()
        return ToneRow(correct_transposition(ri,n))

    def shift(self,i):
        """
        SHIFT (ToneRow operation)

        Returns a new ToneRow with the pitches shifted in position by 'i'
        places.

        Remember that shifting +1 place means FORWARD; the last element pops
        off the end and becomes the first. Shifting -1 means BACKWARD, toward
        the earlier numbers in the series; the first element pops out of the
        front and goes to the back of the line.

        Note that 'i' must be an integer, not a string. The shift function can
        accommodate negative numbers; however, in spec string notation (0-9
        and A-B), there is no such thing -- only a single character.
        """
        pcs = PcSet(self) # I have to call on an ancestor here,
                          # or there's a loop!
        return ToneRow(pcs.shift(i))

    def rotate(self,i,n):
        """
        ROTATE (ToneRow operation)

        Returns a new ToneRow with the pitches shifted in position by 'i'
        places, then transposed so that the first pitch is 'n'.

        Remember that shifting +1 place means FORWARD; the last element pops
        off the end and becomes the first. Shifting -1 means BACKWARD, toward
        the earlier numbers in the series; the first element pops out of the
        front and goes to the back of the line.

        As in the four main methods (P, R, I, and RI), the expected initial
        pitch 'n' can also be a string, with A = 10 and B = 11.

        However, the shift amount 'i' must be an integer, not a string.The
        shift function can accommodate negative numbers; however, in spec
        string notation (0-9 and A-B), there is no such thing -- only a single
        character.
        """
        pcs = PcSet(self)
        return ToneRow(correct_transposition(pcs.shift(i),n))

    def contour(self):
        """
        Returns the contour vector for a given ToneRow. This is defined as the
        list of (ascending) intervals between each successive element in the
        row. The row is considered to 'wrap around' at the ends.

        For example:

        if a        = [2, 7, 8, 5, 11, 6, 3, 10, 4, 9, 0, 1], then
        a.contour() =   [5, 1, 9, 6,  7, 9, 7,  6, 5, 3, 1, 1]

        Which may be read as a set of instructions for generating the row:

            Transpose element 0 by 5 to get element 1. [2 becomes 7]
            Transpose element 1 by 1 to get element 2. [7 becomes 8]
            Transpose element 2 by 9 to get element 3. [8 becomes 5]
            ...
            Transpose the final element by 1 to get the starting element.

        Unlike a ToneRow, a contour vector does NOT have to have unique
        elements. In fact, several commonly known 12-tone arrangements have
        only one interval value, repeated across the entire vector:

            The ascending chromatic scale has a contour of all 1's;
            The descending chromatic scale -- all 11's.
            The "circle of fifths" -- all 7's.
            The "circle of fourths" -- all 5's.

        When the ToneRow is rendered as another Prime form, the contour vector
        does not change -- transposition of the elements does not affect
        the relationships between the elements. The same is true within the
        different transpositions of R, I, and RI.

        Between the different branches of the ToneRow 'family', however,
        the contour vector may change. For the simplest case, the ascending
        chromatic scale rendered as retrograde or inverted just becomes the
        descending scale; RI restores it to ascending. Therefore the contour
        vector would vary between all 1's and all 11's. For more typical
        cases, the respective contours are related, but distinct:

        If a = [4, 5, 6, 8, 0, 2, 11, 10, 9, 1, 7, 3], then:

            P contour  = [1, 1, 2, 4, 2, 9, 11, 11, 4, 6, 8, 1]
            R contour  = [4, 6, 8, 1, 1, 3, 10, 8, 10, 11, 11, 11]
            I contour  = [11, 11, 10, 8, 10, 3, 1, 1, 8, 6, 4, 11]
            RI contour = [8, 6, 4, 11, 11, 9, 2, 4, 2, 1, 1, 1]

        The easiest to understand is the relationship between P and I; each
        interval in the P contour has been inverted. The same relationship
        holds between R and RI.

        However, the P to R relationship is less clear because of the
        arbitrary starting element, the first, in the definition. When
        rendered as retrograde, the first element becomes the last; the
        contour, which was originally reckoned starting with this element, is
        therefore 1.) inverted relative to prime and 2.) shifted 'backwards'
        by one place, since the original starting element is now, effectively,
        in position '-1'.
        """
        c = []
        for this, next in zip(self,self.shift(-1)):
            c.append((next-this)%12)
        return c


def equivalent(a,b):
    """
    Returns True if the operations P(n), R(n), I(n), and RI(n) return the same
    family of ToneRows for both 'a' and 'b'. In other words, all 48 possible
    forms (four methods times 12 different starting points) for 'a' and 'b'
    should match. [In reality, if *any* match, then all match.]
    """
    standard = b.P(0)
    # abracadabra
    methods = [a.P, a.I, a.R, a.RI]
    for f in methods:
        test = f(0)
        if list(test) == list(standard):
            return True
    return False


def rotequiv(a,b):
    """
    Rotational equivalence:
    Returns True if any of the 12 possible rotations of 'a' or 'b'
    are equivalent (see definition for equivalent(a,b)).
    """
    for n in range(12):
        if equivalent(a.shift(n),b):
            return True
    return False


def randomrow():
    """
    Returns a randomly generated ToneRow.  This is probably not perfect;
    it uses the default Python pseudorandom number generator, and with
    12 factorial combinations, there is no guarantee that every possible
    row will be generated over time on every machine architecture.

    That's why we call this 'experimental'!
    """
    r = range(12)
    shuffle(r)
    return ToneRow(r)
