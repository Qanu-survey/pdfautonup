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

import decimal

def default_paper_size():
    # TODO
    # What should be done: find the default papersize value from (in that order)
    # - LC_PAPER environment variable (can be read from "locale -k LC_PAPER"
    # - PAPERSIZE environment variable
    # - file described by the PAPERCONF environment variable
    # - content of /etc/papersize
    # - stdout of the paperconf command

    return (decimal.Decimal(595), decimal.Decimal(842)) # Temporary return a4
