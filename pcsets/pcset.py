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
# $Id: pcset.py 191 2007-08-07 03:15:46Z mccosar $

"""
pcset.py -- version 2.0 -- Bruce H. McCosar

Pitch Class Sets are a mathematical model for analyzing and composing music.
Each note 'C' through 'B' has an equivalent pitch class number 0 through 11:

      | common |      C#      D#          F#      G#      A#      |
      |  note  |  C   --  D   --  E   F   --  G   --  A   --  B   |
      |  name  |      Db      Eb          Gb      Ab      Bb      |
      |        |                                                  |
      |  pc #  |  0   1   2   3   4   5   6   7   8   9   10  11  |

Sets of these numbers may be operated on by mathematical functions such as
transpose and invert, and analyzed by such measures as interval vectors and
relations to other sets, particularly prime sets.


Features:

  * All PcSet methods return NEW PcSets instead of modifying the original in
    place. This makes it possible to chain calls together, such as:

    newpcs = pcs.invert().transpose(4).reverse()

  * The basic PcSet class does not understand note names, only numerical pitch
    classes. Note operations are in a separate module(noteops.py).

    There are two ways to define pitch classes (PcSets):

    -- As a specificiation string.  Fast and easy, this is simply a string
       containing the numerical values for the pitch classes, with A = 10 and
       B = 11.  Example: PcSet('0146A')

    -- As a list of integers.  Example: [0,1,3,4,6,7,9,10]

    Duplicate values in the definition will be ignored.  All numbers will be
    mapped to the modulus 12 domain (from 0 to 11)

  * The PcSet class supports __len__, __str__, and __iter__, making the
    following calls possible (and replacing some of the version 1 methods):

    Purpose                                    NEW in v2.0  Old method
    =========================================  ===========  ==============
    Find cardinality of a set (# of elements)  len(pcs)     pcs.card()
    Return the set as a string                 str(pcs)     pcs.toString()
    Create a list of the elements in the set   list(pcs)    pcs.toList()


CORE as of version 2.0.0 -- new functionality may occasionally be added,
and bugs will be fixed, but the interface defined here will not change
in the entire version 2 series.
"""

__metaclass__ = type

__all__ = ['PcSet','PcSetException','DefinitionError']


class PcSetException(Exception):
    """
    The base class for exceptions in the pcset family of modules.
    """
    def __init__(self):
        self.message = self.__doc__

    def __str__(self):
        return self.message


class DefinitionError(PcSetException):
    """
    This exception type is thrown when something goes wrong in defining a
    PcSet (creating a PcSet instance). Any exception that occurs during
    definition will be a subclass of this.
    """


class IllegalCharacter(DefinitionError):
    """
    When defining a PcSet as a specification string, the only legal
    characters are the digits 0-9 and the capital letters A and B.
    The first illegal character encountered was: %(illegal)s
    """
    def __init__(self,ch):
        self.message = self.__doc__ % {'illegal' : ch}


class NonIterableDef(DefinitionError):
    """
    When defining a PcSet, the definition must be an iterable type
    such as a list, set, tuple, or string. In this case, something
    non-iterable was encountered:

    problem input = %(problem)s %(classification)s
    """
    def __init__(self,x):
        trouble = {
            'problem' : x,
            'classification' : type(x)
            }
        self.message = self.__doc__ % trouble


def moderate(x):
    """
    A utility function. Returns the integer between 0 and 11 that best
    represents the input value mod 12. Character values for the digits 0
    through 9 are converted to integers; the characters 'A' and 'B' are
    interpreted as 10 and 11, respectively.
    """
    try:
        n = int(x)
    except ValueError:
        if x == 'A':
            n = 10
        elif x == 'B':
            n = 11
        else:
            raise IllegalCharacter(x)
    return n % 12


def binaryvalue(i):
    """
    A utility function. Finds the binary 'index value' for a list of integers,
    encoded so that if an integer is present in the list, it is one 'bit' in
    the binary number. Therefore, [0,1,7] would be 2**0 + 2**1 + 2**7.  Since
    PcSets are guaranteed to have no duplicates, this gives a unique integer
    between 0 and 4095 for each possible set.
    """
    value = 0
    for bit in i:
        value += 2**bit
    return value


class PcSet:

    """
    Pitch Class Set. Once defined, the set can be manipulated using the
    supplied methods, which are grouped into the following categories:

    FUNDAMENTAL METHODS
        invert()
        transpose(n)

    SET OPERATIONS
        complement()
        reverse()
        sort()
        shift(n)
        zero()
        normal()
        reduced()
        prime()

    SET ANALYSIS
        ivec()
        cvec()

    SHORTHAND METHODS
        I()
        T(n)
        TnI(n)
        Ixy(x,y)

    In addition, PcSets have default string, length, and iterator methods,
    making possible calls such as len(pcs), str(pcs), and list(pcs).

    A useful reference for understanding pc sets:
    http://www.jaytomlin.com/music/settheory/help.html
    """

    # basic services

    def __init__(self,definition):
        """
        A PcSet may be defined as a spec string or as a list. If a string is
        entered, the only characters allowed are 0-9 and A-B (A represents
        10 and B is 11). If a problem is encountered with the input to the
        constructor, a DefinitionError is raised.
        """
        try:
            redefinition = [moderate(note) for note in list(definition)]
        except TypeError:
            # non-iterables go here
            raise NonIterableDef(definition)
        self.definition = []
        for note in redefinition:
            # remove duplicates
            if note not in self.definition:
                self.definition.append(note)

    def __iter__(self):
        for note in self.definition:
            yield note

    def __str__(self):
        output = ''
        for x in self:
            if x < 10:
                output += str(x)
            elif x == 10:
                output += 'A'
            elif x == 11:
                output += 'B'
        return output

    def __repr__(self):
        return 'PcSet(%s)' % self.definition

    def __len__(self):
        return len(self.definition)

    # fundamental methods

    def invert(self):
        """
        Returns a new PcSet which is the inverse of the original.
        """
        inverse = [((12-note) % 12) for note in self]
        return PcSet(inverse)

    def transpose(self,n):
        """
        Returns a new PcSet which is the original transposed by n.
        """
        transposed = [((note+n) % 12) for note in self]
        return PcSet(transposed)

    # set operations

    def complement(self):
        """
        Returns a new PcSet which is the complement of the original set -- it
        contains all the elements which the original does not.
        """
        anti = []
        for note in range(12):
            if note not in self:
                anti.append(note)
        return PcSet(anti)

    def reverse(self):
        """
        Returns a new PcSet with the elements of the original reversed.
        """
        return PcSet(reversed(self.definition))

    def sort(self):
        """
        Returns a new PcSet in which the elements of the original have been
        sorted in ascending order.
        """
        return PcSet(sorted(self))

    def shift(self,n):
        """
        Returns a new PcSet in which the elements of the original have been
        shifted up 'n' places. (Negative values for n shift down instead; zero
        does nothing but return a copy.)
        """
        size = len(self)
        copy = list(self)
        if size > 1:
            uptimes = int(n) % size
            if uptimes > 0:
                for x in range(uptimes):
                    copy.insert(0,copy.pop())
        return PcSet(copy)

    def zero(self):
        """
        Returns a new PcSet in which the elements have been transposed so that
        the first element is zero.
        """
        try:
            return self.transpose(-self.definition[0])
        except IndexError:
            # empty set, no first element
            return PcSet(self)

    def normal(self):
        """
        Returns a new PcSet which is the 'normal form' of the original. The
        normal form has elements arranged to take up smallest total interval
        space from beginning to end. In the case of ties, the arrangement with
        the best 'packing' toward the left is chosen.
        """
        size = len(self)
        if size < 2:
            return PcSet(self)
        # determine all the possible shift rotations of the sorted set
        original = self.sort()
        rotations = [original.shift(n) for n in range(size)]
        # determine which arrangement has the lowest binary value
        # when compared from a fair start (first element on zero)
        bestnormal = rotations.pop()
        established = binaryvalue(bestnormal.zero())
        for arrangement in rotations:
            challenger = binaryvalue(arrangement.zero())
            if challenger < established:
                bestnormal = arrangement
                established = challenger
        return bestnormal

    def reduced(self):
        """
        Returns a new PcSet which is the 'reduced form' of the original.
        For a given PcSet 'pcs', this is equivalent to the operation series

            pcs.normal().zero()

        The returned set will be easily comparable to other reduced sets.
        For example:

        >>> from pcsets.noteops import pcfor
        >>> examples = [pcfor(s) for s in ('C E G', 'A C# E', 'A C E')]
        >>> print [str(p) for p in examples]
        ['047', '914', '904']
        >>> print [str(p.normal()) for p in examples]
        ['047', '914', '904']
        >>> print [str(p.reduced()) for p in examples]
        ['047', '047', '037']
        >>> print [str(p.prime()) for p in examples]
        ['037', '037', '037']

        The chords C major, A major, and A minor are not easily comparable in
        normal form. When the normal form is transposed to start on zero, it's
        clear that '047' must be the reduced form that corresponds to what we
        think of as 'major' chords.

        Note, however, that the difference disappears when these are put in
        prime form. (See the documentation for the prime() method.)
        """
        return self.normal().zero()

    def prime(self):
        """
        Returns a new PcSet which is the 'prime form' of the original.
        The prime form can be transformed into any of the sets in its
        'family' through the operations T(n) and T(n)I.

        Any set will have a normal form.  If the set is transposed so that
        the first element is zero, this is the reduced form.  However, any
        set will also have an inversion.  The reduced form of the inversion
        can be compared to the original reduced form.  The prime form,
        then, is the reduced set that has the closest leftward packing.
        """
        original = self.normal().zero()          # reduced form
        inverted = self.invert().normal().zero() # reduced form of inverse
        if binaryvalue(original) < binaryvalue(inverted):
            return original
        else:
            return inverted

    # set analysis

    def ivec(self):
        """
        Finds the Interval Vector for the set. This is defined as a six member
        vector, with each value representing an interval group:

        [0] = Number of Group 1 inversions (minor 2nd, major 7th)
        [1] = Same, but for Group 2 (major 2nd, minor 7th)
        ...   (and so on)
        [5] = Same, but for Group 6 (the tritone)
        """
        ivec = [0] * 6
        workingcopy = list(self.sort())
        while len(workingcopy) > 1:
            note = workingcopy.pop()
            for othernote in workingcopy:
                intervalclass = (note - othernote) % 12
                if intervalclass > 6:
                    intervalclass = (12 - intervalclass) % 12
                ivec[intervalclass-1] += 1
        return ivec

    def cvec(self):
        """
        Common Tone Vector: finds the number of common tones for each possible
        value of n in the operation TnI. Returns a twelve member vector where
        element 0 is the number of common tones under T(0)I, 1 under T(1)I,
        and so on.
        """
        cvec = [0] * 12
        rawtable = []
        for x in self:
            for y in self:
                rawtable.append((x+y) % 12)
        entries = set(rawtable)
        for value in entries:
            cvec[value] += rawtable.count(value)
        return cvec

    # shorthand methods

    def I(self):
        """
        Shorthand for invert()
        """
        return self.invert()

    def T(self,n):
        """
        Shorthand for transpose(n)
        """
        return self.transpose(n)

    def TnI(self,n):
        """
        Shorthand for two combined operations: first inversion, then
        transposition by n. (Although class methods use postfix notation, the
        original pc set theory literature commonly uses prefix notation such
        as this.)
        """
        return self.invert().transpose(n)

    def Ixy(self,x,y):
        """
        Shorthand for inversion around an axis specified by pitch classes x
        and y. Inversion around this axis will cause x to become y and y to
        become x.
        """
        return self.invert().transpose(x+y)
