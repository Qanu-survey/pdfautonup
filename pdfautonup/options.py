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

from pdfautonup import VERSION

def commandline_parser():
    """Return a command line parser."""

    parser = argparse.ArgumentParser(
        description=(
            "Convert PDF files to 'n-up' file, with multiple input pages per "
            "destination pages. The output size is a4paper (it will be "
            "configurable in a later version), and the program compute the "
            "page layout, to fit as much source pages in per destination pages "
            "as possible. If necessary, the source pages are repeated to fill "
            "all destination pages."
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
        help='Target paper size (TODO not implemented)',
        # TODO list available sizes in help
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

