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
# $Id: pcops.py 191 2007-08-07 03:15:46Z mccosar $

"""
pcops.py -- version 2.0 -- Bruce H. McCosar

This module contains the following PcSet operations, grouped into families.
In general, operations that involve only a single set are found in pcset.py;
operations on two or more sets are found here.

EQUALITY
    exact_equality(a,b)
    set_equality(a,b)
    same_prime(a,b)

TRANSFORMATION RELATIONSHIPS
    op_path(a,b)
    symmetry(a)
    rel_Tn(a,b)
    rel_TnI(a,b)

SET OPERATIONS
    union(a,b)
    common(a,b)

SET RELATIONSHIPS
    is_complement(a,b)
    is_prime_complement(a,b)
    subset_of(a,b)
    prime_subset_of(a,b)
    fit_in(a,b)
    harmonize(a,b)

SIMILARITY (as defined by Forte)
    Rp(a,b)
    Rp_path(a,b)
    Rp_prime(a,b)
    R0(a,b)
    R1(a,b)
    R2(a,b)
    Zpair(a,b)


CORE as of version 2.0.0 -- new functionality may occasionally be added,
and bugs will be fixed, but the interface defined here will not change
in the entire version 2 series.
"""


__metaclass__ = type

__all__ = """
exact_equality
set_equality
same_prime
op_path
symmetry
rel_Tn
rel_TnI
union
common
is_complement
is_prime_complement
subset_of
fit_in
harmonize
prime_subset_of
Rp
Rp_path
Rp_prime
R0
R1
R2
Zpair
""".split()

from .pcset import PcSet, PcSetException


class OpSetError(PcSetException):
    """
    When working with OpSets, the constructor operates in one of two modes:

        polarity = 'normal'  : (default) set 'a' varied, set 'b' constant
        polarity = 'reverse' : set 'a' constant, set 'b' varied

    Any other value for polarity (such as %(mistake)s) is not permitted.
    """
    def __init__(self, mistake):
        self.message = self.__doc__ % {'mistake': mistake}


class OpSet:

    """
    A utility class to store the results of operations testing. When created,
    this class finds every value of n which will make relation(a.T(n), b) or
    relation(a.TnI(n), b) return True.

    However, if the polarity of the operation is specified as 'reverse', set
    b is altered instead, and this class finds every value of n which will
    make relation(a, b.T(n)) or relation(a, b.TnI(n)) return True. (The default
    polarity is defined as 'normal'.)

    The instance properties Tn and TnI store a list of the results; there is
    also the boolean 'any' property which is True if there were any matches.

    Added in version 2.0.0b3: a call to str(result) when result is an OpSet
    will produce human-readable string output.  In the case of no matches,
    it will return the string 'None'.
    """

    def __init__(self, relation, ao, bo, polarity='normal'):
        self.result = {'Tn': [], 'TnI': []}
        for mode in ['Tn', 'TnI']:
            for n in range(12):
                if polarity == 'normal':
                    if mode == 'TnI':
                        a = ao.TnI(n)
                    else:
                        a = ao.T(n)
                    b = bo
                elif polarity == 'reverse':
                    if mode == 'TnI':
                        b = bo.TnI(n)
                    else:
                        b = bo.T(n)
                    a = ao
                else:
                    raise OpSetError(polarity)
                if relation(a, b):
                    self.result[mode].append(n)

    def getTn(self):
        return list(self.result['Tn'])

    def getTnI(self):
        return list(self.result['TnI'])

    def getAny(self):
        return not(self.result['Tn'] == [] and self.result['TnI'] == [])

    Tn = property(getTn)
    TnI = property(getTnI)
    any = property(getAny)

    def __str__(self):
        tn = ["T(%d)" % n for n in self.Tn]
        tni = ["T(%d)I" % n for n in self.TnI]
        s = ' '.join(tn + tni)
        if s == '':
            s = 'None'
        return s


class NullOpSet(OpSet):

    """
    This OpSet should be returned when it is certain no match can be found.
    """

    def __init__(self):
        self.result = {'Tn': [], 'TnI': []}

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - equality


def exact_equality(a, b):
    """
    Test if two pitch class sets are *exactly* equal, including the ordering
    of the elements.
    """
    return list(a) == list(b)


def set_equality(a, b):
    """
    Test if two pitch class sets are equal. The order of the elements is
    irrelevant, but the elements must be the same in both sets.
    """
    return set(a) == set(b)


def same_prime(a, b):
    """
    Test if two pitch class sets have the same prime form. If this is the
    case, then the sets can differ only by:

        1. ordering of the elements,
        2. transposition, and
        3. inversion.

    Each prime form determines an entire class of sets. Applying the
    operations Tn and TnI to the prime, with all the possible values for n,
    will generate every member of that set class.
    """
    return exact_equality(a.prime(), b.prime())

# - - - - - - - - - - - - - - - - - - - - - - - - transformation relationships


def op_path(a, b):
    """
    Operational paths from a to b. If set a can be transformed into b through
    Tn or TnI, this function will find the possible values for n. Arrangement
    of the elements is not important. Note that two identical sets are related
    by at least T(0), and simple inverse sets are related by T(0)I.

    Also note that the returned results are operations on 'a' which will yield
    'b'. For TnI, this doesn't matter:

        TnI(a) = b and TnI(b) = a.

    However, for Tn, the relationship changes:

        Tn(a) = b, but T(12-n)(b) = a.

    The results are returned as an object with the following properties:

        results.Tn  : A list of possible values for n where Tn(a) = b
        results.TnI : A list of possible values for n where TnI(a) = b

    Either of these return values may be an empty list. There is also a
    boolean property 'any' which returns True if any transformation is found.
    """
    # screen out totally unrelated sets
    if not same_prime(a, b):
        return NullOpSet()
    # Now any two sets that get through here must have the same prime form.
    result = OpSet(set_equality, a, b)
    # sanity check
    assert result.any
    # ok, go home
    return result


def symmetry(a):
    """
    Returns the number of inversion axes which map the set onto itself.
    """
    return a.cvec().count(len(a))


def rel_Tn(a, b):
    """
    Returns True if sets a and b are related by Tn (transposition). That is,
    Tn(a) = b is true for some value of n.

    The equivalent functionality could be achieved using op_path. However,
    rel_Tn is a bit more readable.

        if op_path(a,b).Tn: ...

        -is equivalent to-

        if rel_Tn(a,b): ...
    """
    return op_path(a, b).Tn != []


def rel_TnI(a, b):
    """
    Returns True if sets a and b are related by TnI (inversion, followed by
    transposition by n). That is, TnI(a) = b is true for some value of n. See
    also rel_Tn.
    """
    return op_path(a, b).TnI != []

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - set operations


def union(a, b):
    """
    Returns a new PcSet composed of the pitch classes present in either of the
    original sets.
    """
    return PcSet(list(a) + list(b))


def common(a, b):
    """
    Returns a new PcSet composed of the tones the two sets have in common.
    """
    return PcSet(set(a).intersection(set(b)))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  set relationships


def is_complement(a, b):
    """
    Determines if set a and set b are complementary.
    """
    return len(union(a, b)) == 12


def is_prime_complement(a, b):
    """
    Determines if b, or any transposition / inversion of b, is complementary
    to set a. Note that b itself may not be a direct complement of a.
    """
    return same_prime(a.complement(), b)


def subset_of(a, b):
    """
    Determines if b is a subset of a. The first set must contain all of the
    elements of the second one.
    """
    return set(b).issubset(set(a))


def harmonize(a, b):
    """
    Finds all the operational paths by which 'a' can be transformed into set
    which contains 'b' as a subset. In other words, this function finds all
    the Tn or TnI operations that can make set a 'harmonize' with set b.

    The results are returned as an object with the following properties:

        results.Tn  : A list of values for n where b is a subset of Tn(a)
        results.TnI : A list of values for n where b is a subset of TnI(a)

    Either of these return values may be an empty list. There is also a
    boolean property 'any' which returns True if any transformation is found.
    """
    # refuse impossible quests
    if len(a) < len(b):
        return NullOpSet()
    result = OpSet(subset_of, a, b)
    return result


def fit_in(a, b):
    """
    Finds all the operational paths by which 'b' can be transformed into a
    direct subset of 'a'. In other words, this function finds all the Tn or
    TnI operations which will make b 'fit in' with a.

    The results are returned as an object with the following properties:

        results.Tn  : A list of values for n where Tn(b) is a subset of a
        results.TnI : A list of values for n where TnI(b) is a subset of a

    Either of these return values may be an empty list. There is also a
    boolean property 'any' which returns True if any transformation is found.
    """
    # refuse impossible quests
    if len(a) < len(b):
        return NullOpSet()
    # note the polarity of a and b is important; b is in the 'hot seat'
    result = OpSet(subset_of, a, b, polarity='reverse')
    return result


def prime_subset_of(a, b):
    """
    Determines if b, or any transposition / inversion of b, is a subset of a.
    Note that b itself may not be a direct subset of a.
    """
    result = fit_in(a, b)
    return result.any

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - similarity (Forte)


def Rp(a, b):
    """
    Determines if two sets of the same cardinality differ by only one tone.
    The remaining elements must match up exactly.
    """
    if len(a) != len(b):
        return False
    return len(common(a, b)) + 1 == len(a)


def Rp_path(a, b):
    """
    Finds all the operational paths by which 'a' can be transformed into a set
    which has relation Rp with 'b'. The results are returned as an object with
    the following properties:

        results.Tn  : A list of values for n where Rp(Tn(a),b) is true
        results.TnI : A list of values for n where Rp(TnI(a),b) is true

    Either of these return values may be an empty list. There is also a
    boolean property 'any' which returns True if any transformation is found.
    """
    if len(a) != len(b):
        return NullOpSet()
    result = OpSet(Rp, a, b)
    return result


def Rp_prime(a, b):
    """
    Determines if it is possible, through inversion, transposition, or a
    combination of the two, to match all the elements of sets a and b --
    except for one element in each set.
    """
    result = Rp_path(a, b)
    return result.any


def R0(a, b):
    """
    Checks for R0, or 'minimum similarity': when the interval vectors of two
    sets have no digits in common.
    """
    if len(a) != len(b):
        return False
    return all([x != y for x, y in zip(a.ivec(), b.ivec())])


def R1_or_R2(a, b):
    """
    Checks for R1 or R2, the two types of 'maximum similarity'. This is a
    utility function for the actual R1 and R2 functions, so never needs to be
    called directly. It returns a dictionary with two keys:

        'difference2': True if the interval vectors differ by two values.
        'interchange': True if these two values have been interchanged.
    """
    results = {'difference2': False, 'interchange': False}
    if len(a) != len(b):
        return results
    misfits = []
    for x, y in zip(a.ivec(), b.ivec()):
        if x != y:
            misfits.append((x, y))
    if len(misfits) == 2:
        results['difference2'] = True
        first, second = misfits[0], misfits[1]
        if first[0] == second[1] and first[1] == second[0]:
            results['interchange'] = True
    return results


def R1(a, b):
    """
    Checks for R1, one type of 'maximum similarity': the interval vectors
    should differ only by interchange of two values.
    """
    results = R1_or_R2(a, b)
    return results['interchange']


def R2(a, b):
    """
    Checks for R2, another type of 'maximum similarity': the interval vectors
    differ only by two values, but relation R1 does not hold -- the two misfit
    values are not related by interchange.
    """
    results = R1_or_R2(a, b)
    return results['difference2'] and not results['interchange']


def Zpair(a, b):
    """
    Checks if two sets are a Z pair, that is, if they have the same interval
    vector. Note this does not discriminate against testing a set against
    itself -- Zpair(a,a) will return True.
    """
    return a.ivec() == b.ivec()
