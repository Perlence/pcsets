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
# $Id: setup.py 209 2007-08-19 16:41:44Z mccosar $

"""
setup.py

If you run this script, it should install the pcsets library
to your Python distribution's site libraries.
"""

__metaclass__ = type

from distutils.core import setup


PCSETS_VERSION = '2.0.2' # <===================== (auto-substituted)


DESCRIPTION = 'Pitch Class Sets for Python.'

LONG_DESCRIPTION = """
                               pcsets:
                     Pitch Class Sets for Python

                            version 2.0.2

                           Bruce H. McCosar


Welcome, and thank you for downloading pcsets. This is the third
official (non-beta) release. With this release, I start the pcsets
tutorial see "About this Package", below).

Learning about Pitch Class Sets is easy -- the four modules presented
here are, like many Python programs, self documenting. They work well
with pydoc <http://docs.python.org/lib/module-pydoc.html>.

Learning how to use these for practical compositional purposes, on the
other hand ... well, that takes a lot of individual experimentation. I
have started a short tutorial, which will eventually demonstrate some
of the techniques I've learned. However, you are a much better judge
of what you want to know than I -- please, try the module out, and
most of all, have fun learning something new.


                        About Pitch Class Sets
                        ======================

Pitch Class Sets are a mathematical model for analyzing and composing
music. Each note 'C' through 'B' has an equivalent pitch class number
0 through 11. Sets of these numbers may be operated on by mathematical
functions such as transpose and invert.

The goal of this project is to, eventually, have:

  * A Python library capable of fully implementing Pitch Class Sets
    and their common operations, as well as several convenience
    functions to bring these abstract concepts to the real world.
    (Mapping pitch classes to note names, for instance).

  * A tool for composition.  Some applications are harmonization,
    chord voicing generation, and melodic motif creation.

  * More exotic goals -- creation of new chordal elements, musical
    progressions, and harmonic relationships.


                          About this Package
                          ==================

The API will not change for any of the modules referred to as 'core'.
Bugs will be fixed and new modules will be added, but you won't wake
up one day and find that PcSets wants input in statcoulombs or Dutch
Guldens. In the version 2 series, the core will always behave like
the core. Occasionally new functionality will be introduced, but the
original functionality will never be 'broken' -- that's why I spent all
that time writing unit tests.


THE CORE

This is the core as of 2.0.0:


    pcsets.pcset

        The base class, PcSet, includes methods that operate on single
	sets, such as inversion and transposition.

    pcsets.pcops

        Operations on two or more sets, such as subset_of(a,b).

    pcsets.catalog

        Generates the entire catalog of 224 prime sets as a Python
        object. Since this takes a while to generate, it saves the
        catalog in a pickle file (catalog.pkl) for future use.

    pcsets.noteops

        The 'universal translator' from PcSets to named notes and
        vice versa.


Any *new* modules will enter as 'experimental', however, not core.
Experimental modules can change at any time.


EXPERIMENTAL MODULES

With version 2.0.1, I introduced the first experimental module:


    pcsets.tonerow

        Implements the ToneRow class.  Unlike PcSets, which are
	unordered, a ToneRow consists of all 12 pitches in an
	*ordered* arrangement.


There is a lot of good information on this subject in the Straus book
referenced below. I've also put a lot of time into writing documentation
strings for the module; a run through it with pydoc will probably tell
you somewhere between too much and far too much ;-)

Another experimental module in development (and still in hiding,
until I settle on a usable, workable interface):


  * Operations on the familiar chords and scales -- sort of a noteops
    for the common language of chord-scale theory.


These modules won't make it to the core until at least version 2.1.


THE TUTORIAL

Finally, I've made a start on the tutorial.  My hope is that working
through the documentation -- even for features that haven't been added
yet! -- will let me streamline the API and introduce more relevant
features in future releases.


Be sure to check back at the project website for updates.  I seem to
have embraced Google Code's slogan, "Release early, release often."


                   http://code.google.com/p/pcsets/
"""

DOWNLOAD_URL = \
             "http://pcsets.googlecode.com/files/pcsets-%s.tar.gz" \
             % PCSETS_VERSION

CLASSIFIERS = """
Development Status :: 5 - Production/Stable
Intended Audience :: Education
License :: OSI Approved :: GNU General Public License (GPL)
Programming Language :: Python
Topic :: Software Development :: Libraries :: Python Modules
""".strip().split('\n')

parameters = {
    'name' : 'pcsets',
    'version' : PCSETS_VERSION,
    'author' : 'Bruce H. McCosar',
    'author_email' : 'bmccosar@gmail.com',
    'description' : DESCRIPTION,
    'long_description' : LONG_DESCRIPTION,
    'url' : 'http://code.google.com/p/pcsets/',
    'download_url' : DOWNLOAD_URL,
    'classifiers' : CLASSIFIERS,
    'packages' : ['pcsets']
    }

if __name__ == '__main__':
    setup(**parameters)
