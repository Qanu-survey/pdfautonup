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

"""Paper-size related functions"""

import decimal
import os
import re
import subprocess

from pdfautonup import errors

PAPERSIZES = {
    # http://www.printernational.org/iso-paper-sizes.php
    "4a0": "1682mmx2378mm",
    "2a0": "1189mmx1682mm",
    "a0": "841mmx1189mm",
    "a1": "594mmx841mm",
    "a2": "420mmx594mm",
    "a3": "297mmx420mm",
    "a4": "210mm27mm",
    "a5": "148mmx210mm",
    "a6": "105mmx148mm",
    "a7": "74mmx105mm",
    "a8": "52mmx74mm",
    "a9": "37mmx52mm",
    "a10": "26mmx37mm",

    "b0": "1000mmx1414mm",
    "b1": "707mmx1000mm",
    "b2": "500mmx707mm",
    "b3": "353mmx500mm",
    "b4": "250mmx352mm",
    "b5": "176mmx250mm",
    "b6": "125mmx176mm",
    "b7": "88mmx125mm",
    "b8": "62mmx88mm",
    "b9": "44mmx62mm",
    "b10": "31mmx44mm",

    # http://www.paper-sizes.com/north-american-paper-sizes/north-american-architectural-paper-sizes
    "archA": "9inx12in",
    "archB": "12inx18in",
    "archC": "18inx24in",
    "archD": "24inx36in",
    "archE": "36inx48in",

    # http://www.engineeringtoolbox.com/office-paper-sizes-d_213.html
    "letter": "8.5inx11in",
    "legal": "8.5inx14in",
    "executive": "7inx10in",
    "tabloid": "11inx17in",
    "statement": "5inx8.5in",
    "halfletter": "5inx8.5in",
    "folio": "8inx13in",

    # http://www.paper-sizes.com/north-american-paper-sizes/north-american-loose-paper-sizes
    "ledger": "17inx11in",

    # http://simple.wikipedia.org/wiki/Paper_size
    "quarto": "8inx10in",

    # http://hplipopensource.com/hplip-web/tech_docs/page_sizes.html
    "flsa": "8.5inx13in",

    # http://www.coding-guidelines.com/numbers/ndb/units/area.txt
    "flse": "8.5inx13in",

    # http://jexcelapi.sourceforge.net/resources/javadocs/2_6_10/docs/jxl/format/PaperSize.html
    "note": "8.5inx11in",
    "11x17": "11inx17in",
    "10x14": "10inx14in",

    }

# Source: http://en.wikibooks.org/wiki/LaTeX/Lengths
UNITS = {
    "": 1, # Default is point (pt)
    "pt": 1,
    "mm": 2.84,
    "cm": 28.4,
    "in": 72.27,
    "bp": 1.00375,
    "pc": 12,
    "dd": 1.07,
    "cc": 12.84,
    "sp": 0.000015,
    }

UNITS_RE = r"({})".format("|".join(UNITS.keys()))
SIZE_RE = r"([\d.]+){}".format(UNITS_RE)
PAPERSIZE_RE = r"^(?P<width>{size})[x× ]?(?P<height>{size})$".format(
    size=SIZE_RE
    )

UNITS_COMPILED_RE = re.compile("^{}$".format(UNITS_RE))
SIZE_COMPILED_RE = re.compile("^{}$".format(SIZE_RE).format("size"))
PAPERSIZE_COMPILED_RE = re.compile(PAPERSIZE_RE.format("width", "height"))

def parse_length(string):
    """Return a length corresponding to the string.

    :rtype: :class:`decimal.Decimal`
    :return: The length, in points.
    """
    match = SIZE_COMPILED_RE.match(string).groups()
    return decimal.Decimal(match[0]) * decimal.Decimal(UNITS[match[1]])

def parse_couple(string):
    """Return a tuple of dimensions.

    :param str string: The string to parse, as "LENGTHxLENGTH" (where LENGTH
    are length).
    :return: A tuple of :class:`decimal.Decimal`, reprenting the dimensions,
        in points.
    """
    try:
        match = PAPERSIZE_COMPILED_RE.match(string).groupdict()
        return (
            parse_length(match['width']),
            parse_length(match['height']),
            )
    except AttributeError:
        raise errors.CouldNotParse(string)

def parse_paper_size(string):
    """Return the papersize corresponding to string.
    """
    if string.lower() in PAPERSIZES:
        return parse_paper_size(PAPERSIZES[string])
    return parse_couple(string)

def parse_lc_paper(string):
    """Parse LC_PAPER locale variable

    We assume units are milimeters.
    """
    dimensions = {}
    for line in string.split('\n'):
        if line.startswith("width="):
            dimensions["width"] = parse_length("{}mm".format(line[6:]))
        if line.startswith("height="):
            dimensions["height"] = parse_length("{}mm".format(line[7:]))
    if len(dimensions) == 2:
        return (dimensions["width"], dimensions["height"])
    raise errors.CouldNotParse(string)

def target_paper_size(target_size):
    """Return the target paper size.

    :param str target_size: Target size, if provided by user in command line.
    """
    # pylint: disable=too-many-return-statements

    # Option set by user on command line
    if target_size is not None:
        return parse_paper_size(target_size[0])

    # LC_PAPER environment variable (can be read from "locale -k LC_PAPER"
    try:
        return parse_lc_paper(subprocess.check_output(
            ["locale", "-k", "LC_PAPER"],
            universal_newlines=True,
            ))
    except (subprocess.CalledProcessError, errors.CouldNotParse):
        pass

    # PAPERSIZE environment variable
    try:
        return parse_paper_size(os.environ['PAPERSIZE'].strip())
    except KeyError:
        pass

    # file described by the PAPERCONF environment variable
    try:
        return parse_paper_size(
            open(os.environ['PAPERCONF'], 'r').read().strip()
            )
    except errors.CouldNotParse:
        raise
    except: # pylint: disable=bare-except
        pass

    # content of /etc/papersize
    try:
        return parse_paper_size(open('/etc/papersize', 'r').read().strip())
    except errors.CouldNotParse:
        raise
    except: # pylint: disable=bare-except
        pass

    # stdout of the paperconf command
    try:
        return parse_paper_size(subprocess.check_output(
            ["paperconf"],
            universal_newlines=True,
            ).strip())
    except (subprocess.CalledProcessError, errors.CouldNotParse):
        pass

    # Eventually, if everything else has failed, a4
    return parse_paper_size('a4')
