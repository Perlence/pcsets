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
# $Id: catalog.py 191 2007-08-07 03:15:46Z mccosar $

"""
catalog.py -- version 2.0 -- Bruce H. McCosar

When comparing two pitch class sets, there are several ways to discuss their
relative similarity. Some of the relevant functions from pcsets.pcops are
set_equality, is_complement, and subset_of. These would not be out of place in
any other version of set theory.

There are also measures very specific to pitch class sets. These were created
by Allen Forte -- the R-series and Z-pair relationships.

However, there is one relation that truly surprises many people once they
learn about it: the concept of prime sets.

If we take an unordered set of 12 unique elements, there are 4096 possible
configurations. Compare that to the 224 'prime sets' generated and cataloged
by this module. These 224 sets represent all the rest of the possible sets in
a fundamental way:

  ! If you have a prime set, you can generate a 'family' of related sets !
  ! by applying the operations Tn and TnI with different values of n.    !

For example, the trichord '037' defines a C minor chord. It also happens to
be a prime set. (You can learn about how primes are determined by reading the
docstrings in pcsets.pcset.PcSet for the methods normal, reduced, and prime.)

When we apply the 12 possible Tn and TnI operations to '037', the Tn
operations produce every possible minor triad, while the transpositions of the
inverse (047) map out all possible major triads.

Each of the prime sets in the catalog are indexed according to cardinality
(number of elements). Look at these carefully. For instance, there are only 12
prime trichords. What this says is, in all the 12-tone music world, there are
only 12 possible unique trichords, and everything else is just a transposition
or an inversion of these primes!

Another interesting thing to note is the heptachords (cardinality 7), with
38 prime sets. Think of this: western music has tended to focus on the major
scale (013568A) and maybe a few others like the melodic minor. Look at all the
unexplored territory!

In some ways, the prime catalog produced by this module is the periodic table
for the possible elements of music.


CORE as of version 2.0.0 -- new functionality may occasionally be added,
and bugs will be fixed, but the interface defined here will not change
in the entire version 2 series.
"""

__metaclass__ = type

__all__ = ['SetCatalog']

import pickle

from .pcset import PcSet
from .pcops import exact_equality

PICKLE_FILE = 'catalog.pkl'


def all_possible_pcsets():
    for n in xrange(4096):
        result = []
        for bit in range(12):
            if n & (2**bit):
                result.append(bit)
        yield PcSet(result)


def any_match(p, page):
    for entry in page:
        if exact_equality(p, entry):
            return True
    return False


class SetCatalog:

    """
    A SetCatalog object, when created, goes through the 4096 possible
    (unordered) pitch class sets and finds the unique prime forms. [For
    more information on this, read the pcsets.catalog module docs.]

    The SetCatalog constructor accepts the following options. All have
    sensible defaults, so none are really required during routine use;
    the default conditions are shown.

        SetCatalog(rebuild=False, store=True, failsafe=False)

    Returns a new SetCatalog object.  Options:

        * If 'rebuild' is set to True, the module won't look for
          a previously saved catalog (catalog.pkl).  It will just
          go ahead and regenerate the entire thing.

        * If 'store' is set to False, the module won't try to save
          its regenerated catalog.

        * If 'failsafe' is set to True, then the module will be
          'safe against failure' to write the pickle file.  That
          is, it will ignore the IOError on opening the write.

    Note that if SetCatalog loads a pickle file, it leaves well enough
    alone -- it doesn't write its data back to the file.

    There are three main accessor methods.  Since these only work
    from an instance, let's assume sc = SetCatalog()

        * The sc.page(n) method returns the prime sets from page 'n'
          of the catalog.  Each page contains only prime sets of
          length n.  Therefore, trichords are found on page 3,
          hexachords on page 6, and so on.

        * As a sanity check, you can use len(sc) on your catalog
          object . . . it should return 224, the number of possible
          prime sets.

        * Finally, a simple way to test every possible prime for a
          property is to just use sc as an iterator, as in 'for pc
          in sc:' type statements.  It will return every prime it
          knows of, in cardinality order (the 0's first, then the
          1's, etc.)
    """

    def _rewrite(self):
        storage = open(PICKLE_FILE, 'wb')
        pickle.dump(self.catalog, storage, -1)
        storage.close()

    def _rebuild(self):
        # self.catalog[n] = a 'page' listing primes with cardinality n
        self.catalog = [[] for page in range(13)]
        # Warning: if the above is defined with the shortcut
        #     self.catalog = [[]] * 13
        # this ends up as a list of references to the same empty set!
        for s in all_possible_pcsets():
            p = s.prime()
            page = self.catalog[len(p)]
            if not any_match(p, page):
                page.append(p)
        if self.store:
            try:
                self._rewrite()
            except IOError:
                if not self.failsafe:
                    raise

    def _retrieve(self):
        storage = open(PICKLE_FILE, 'rb')
        self.catalog = pickle.load(storage)
        storage.close()

    def __init__(self, rebuild=False, store=True, failsafe=False):
        self.store = store
        self.failsafe = failsafe
        if rebuild:
            self._rebuild()
        else:
            try:
                self._retrieve()
            except IOError:
                self._rebuild()

    def page(self, n):
        """
        The 'pages' in the catalog are organized by cardinality, that is, the
        length of the prime sets. If you want to find all the possible prime
        hexachords (length 6), for instance, the information is on .page(6)

        Why this term? Because typing in 'cardinality' over and over again
        is inconvenient, and .card(n) seems to imply something to do with
        playing cards. Since we're talking about a catalog here, pages make
        more sense.
        """
        return list(self.catalog[n])

    def __iter__(self):
        for n in range(13):
            for entry in self.catalog[n]:
                yield entry

    def __len__(self):
        result = 0
        for n in range(13):
            result += len(self.catalog[n])
        return result


def showcatalog():
    print "Generating prime set catalog... (this may take a moment)"
    r = SetCatalog(rebuild=True, store=False)
    print "Pitch Class Set Catalog: %d prime sets total\n" % len(r)
    for n in range(13):
        size = len(r.page(n))
        if size > 1:
            w = 'sets'
        else:
            w = 'set'
        print "Cardinality %d: %d prime %s" % (n, size, w)
        position = 0
        for entry in r.page(n):
            if position == 0:
                print "    ",
                position = 4
            if len(entry) == 0:
                print '[]',
            else:
                print entry,
            position += len(entry) + 1
            if position > 60:
                print
                position = 0
        print
        if position > 0:
            print

if __name__ == '__main__':
    showcatalog()
