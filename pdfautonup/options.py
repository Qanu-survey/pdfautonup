#!/usr/bin/env python3

# Copyright Louis Paternault 2011-2014
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>. 1

"""Manage options"""

import argparse
import textwrap

from pdfautonup import VERSION
from pdfautonup import paper

def commandline_parser():
    """Return a command line parser."""

    parser = argparse.ArgumentParser(
        description=textwrap.dedent("""
            Convert PDF files to 'n-up' file, with multiple input pages per
            destination pages. The output size is a4paper (it will be
            configurable in a later version), and the program compute the page
            layout, to fit as much source pages in per destination pages as
            possible. If necessary, the source pages are repeated to fill all
            destination pages.
            """),
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=textwrap.dedent("""
            # Paper size

            ## Source

            Paper size is get from the following sources (in that order):

            - Argument of "--size" option;
            - LC_PAPER environment variable (read as mm);
            - PAPERSIZE environment variable;
            - content of file specified by the PAPERCONF environment variable;
            - content of file /etc/papersize;
            - output of the paperconf command;
            - if everything else have failed, A4.

            ## Recognized sizes

            Paper size can be either specified by the explicit dimensions, or by the name of the size.

            - Explicit dimensions are of the form WIDTHxHEIGHT, where WIDTH and HEIGHT are floating point numbers in one of the following units (default being pt): {units};
            - Recognized paper size names are: {papersizenames}.
            """).format(
                units=str(", ".join([
                    size
                    for size
                    in sorted(paper.UNITS.keys())
                    if size
                    ])),
                papersizenames=str(", ".join(sorted(paper.PAPERSIZES.keys()))),
                ),
        )

    parser.add_argument(
        '--version',
        help='Show version',
        action='version',
        version='%(prog)s ' + VERSION
        )

    parser.add_argument(
        'files',
        metavar="FILES",
        help='PDF files to merge.',
        nargs='+',
        type=str,
        )

    parser.add_argument(
        '--output', '-o',
        help=(
            'Destination file. Default is "-nup" appended to first source file.'
            ),
        type=str,
        )

    parser.add_argument(
        '--interactive', '-i',
        help='Ask before overwriting destination file if it exists.',
        default=False,
        action='store_true',
        )

    parser.add_argument(
        '--size', '-s',
        dest='target_size',
        help='Target paper size (see below for accepted sizes).',
        default=None,
        nargs=1,
        action='store',
        )

    return parser

def destination_name(output, source):
    """Return the name of the destination file.

    :param str output: Filename, given in command line options. May be
        ``None`` if it was not provided.
    :param str source: Name of the first source file.
    """
    if output is None:
        return "{}-nup.pdf".format(".".join(source.split('.')[:-1]))
    return output
