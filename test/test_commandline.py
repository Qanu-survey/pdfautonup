# Copyright 2017 Louis Paternault
#
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Tests"""

import os
import subprocess
import sys
import unittest

from wand.image import Image
import pkg_resources

if sys.version_info < (3, 5):
    raise RuntimeError("Tests require python version 3.5 or higher.")

TEST_DATA_DIR = pkg_resources.resource_filename(__name__, "test_commandline-data")

FIXTURES = [
    {
        "command": ["--algorithm", "panel", "--gap", ".5cm", "--margin", "1cm", "pcb.pdf"],
        "returncode": 0,
        "diff": ("pcb-nup.pdf", "pcb-control.pdf")
    },
    {
        "command": ["trigo.pdf"],
        "returncode": 0,
        "diff": ("trigo-nup.pdf", "trigo-control.pdf")
    },
    {
        "command": ["three-pages.pdf"],
        "returncode": 0,
        "diff": ("three-pages-nup.pdf", "three-pages-control.pdf")
    },
    # TODO Add/Change tests to test failure and command line arguments
]

class TestCommandLine(unittest.TestCase):
    """Run binary, and check produced files."""

    def assertPdfEqual(self, filea, fileb):
        """Test whether PDF files given in argument (as file names) are equal.

        Equal means: they look the same.
        """
        # pylint: disable=invalid-name
        images = (
            Image(filename=filea),
            Image(filename=fileb),
            )
        # TODO Check page number
        for (pagea, pageb) in zip(images[0].sequence, images[1].sequence):
            self.assertEqual(
                pagea.compare(pageb, metric="absolute")[1],
                0,
                )

    def test_commandline(self):
        """Test binary, from command line to produced files."""
        for data in FIXTURES:
            with self.subTest(**data):
                completed = subprocess.run(
                    [sys.executable, "-m", "pdfautonup"] + data['command'],
                    cwd=TEST_DATA_DIR,
                    )
                self.assertEqual(completed.returncode, data['returncode'])
                self.assertPdfEqual(*(
                    os.path.join(TEST_DATA_DIR, filename)
                    for filename in data['diff']
                    ))
