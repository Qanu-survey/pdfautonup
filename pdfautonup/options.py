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

import argparse

from pdfautonup import VERSION

def commandline_parser():
    """Return a command line parser."""

    parser = argparse.ArgumentParser(
        description="TODO",
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
        help='TODO',
        nargs='+',
        type=str,
        )

    parser.add_argument(
        '--output', '-o',
        help='Destination file. Default is "-nup" appended to first source file.',
        type=str,
        )

    parser.add_argument(
        '--interactive', '-i',
        help='Ask before overwriting destination file if it exists.',
        default=False,
        action='store_true',
        )

    # TODO
    # Add an option to specify a custom target paper size


    # TODO
    # Add an option to list available paper size names

    return parser

def destination_name(output, source):
    if output is None:
        return "{}-nup.pdf".format(".".join(source.split('.')[:-1]))
    return output

