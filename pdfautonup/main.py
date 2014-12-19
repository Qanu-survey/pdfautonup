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

"""TODO"""

import argparse
import logging
import sys

from pdfautonup import VERSION

LOGGER = logging.getLogger(__name__)

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
        'FILES',
        help='TODO',
        nargs='+',
        #type=argparse.FileType('r'),
        #default=sys.stdin,
        )

    return parser

def main():
    """Main function"""
    options = commandline_parser().parse_args(sys.argv[1:])
    TODO

if __name__ == "__main__":
    main()
