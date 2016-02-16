# Copyright Louis Paternault 2011-2016
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

"""Different algorithm to fit source files into destination files."""

from collections import namedtuple
import os

from PyPDF2.generic import NameObject, createStringObject
import PyPDF2
import papersize

from pdfautonup import LOGGER
from pdfautonup import errors

def _dist_to_round(x):
    """Return distance of ``x`` to ``round(x)``."""
    return abs(x - round(x))


class _FitMethod:

    def __init__(self, target_size, arguments, metadata=None):
        self.target_size = target_size
        self.interactive = arguments.interactive

        self.pdf = PyPDF2.PdfFileWriter()
        self.current_pagenum = 0
        self.current_page = None

        if metadata is not None:
            self._set_metadata(metadata)

    def add_page(self, page):
        """Add ``page`` to the destination file.

        It is added at the right place, and a new blank page is created if
        necessary.
        """
        if self.current_pagenum == 0:
            self.current_page = self.pdf.addBlankPage(
                width=self.target_size[0],
                height=self.target_size[1],
                )
        (x, y) = self.cell_topleft(self.current_pagenum)
        self.current_page.mergeTranslatedPage(
            page,
            x,
            y,
            )
        self.current_pagenum = (self.current_pagenum + 1) % self.pages_per_page

    def write(self, filename):
        """Write destination file."""
        if self.interactive and os.path.exists(filename):
            question = "File {} already exists. Overwrite (y/[n])? ".format(
                filename
                )
            if input(question).lower() != "y":
                raise errors.UserCancel()
        self.pdf.write(open(filename, 'w+b'))

    def _set_metadata(self, metadata):
        """Set metadata on current pdf."""
        #Source:
        #    http://two.pairlist.net/pipermail/reportlab-users/2009-November/009033.html
        try:
            # pylint: disable=protected-access, no-member
            # Since we are accessing to a protected membre, which can no longer exist
            # in a future version of PyPDF2, we prevent errors.
            infodict = self.pdf._info.getObject()
            infodict.update(metadata)
            infodict.update({
                NameObject('/Producer'): createStringObject(
                    'PdfAutoNup, using the PyPDF2 library — '
                    'http://git.framasoft.org/spalax/pdfautonup'
                    )
            })
        except AttributeError:
            LOGGER.warning("Could not copy metadata from source document.")

    def cell_topleft(self, num):
        """Return the top left coordinate of ``num``th cell of page."""
        raise NotImplementedError()

    @property
    def pages_per_page(self):
        """Return the number of source pages per destination page."""
        raise NotImplementedError()


class FuzzyFit(_FitMethod):
    """Documents can overlap, and space can be wasted, but not too much."""

    #: A target size, associated with the number of source pages that will fit
    #: in it, per width and height (``cell_number[0]`` and ``cell_number[1]``).
    Fit = namedtuple('Fit', ['cell_number', 'target_size'])

    def __init__(self, source_size, target_size, arguments, metadata=None):
        self.source_size = source_size
        self.cell_number, target_size = min(
            self.fit(source_size, target_size),
            self.fit(source_size, (target_size[1], target_size[0])),
            key=self.ugliness,
            )
        super().__init__(target_size, arguments, metadata)


    def ugliness(self, fit):
        """Return the "ugliness" of this ``fit``.

        - A layout that fits perfectly has an ugliness of 0.
        - The maximum ugliness is 1.
        """
        target_width, target_height = fit.target_size
        source_width, source_height = self.source_size
        return (
            _dist_to_round(target_width / source_width)**2
            +
            _dist_to_round(target_height / source_height)**2
            )

    def fit(self, source_size, target_size):
        """Return a :class:`self.Fit` object for arguments.

        The main function is computing the number of source pages per
        destination pages.
        """
        cell_number = (
            max(1, round(target_size[0] / source_size[0])),
            max(1, round(target_size[1] / source_size[1])),
            )
        return self.Fit(cell_number, target_size)

    def cell_topleft(self, num):
        width, height = self.cell_number
        return (
            self.target_size[0] * (num % width) / width,
            self.target_size[1] * (height - 1 - num // width) / height,
            )

    @property
    def pages_per_page(self):
        return self.cell_number[0] * self.cell_number[1]


class Panelize(_FitMethod):
    """Minimum margin is defined, as well as fixed gap."""

    #: Define how the source page will fit into the destination page.
    #: - `margin` is the destination margin (including wasted space);
    #: - `sourcex` is the 'extended' source size (source size, together with gap).
    Fit = namedtuple('Fit', ['margin', 'sourcex'])

    def __init__(self, source_size, target_size, arguments, metadata=None):
        # pylint: disable=too-many-arguments
        if arguments.gap[0] is None:
            self.gap = papersize.parse_length("0")
        else:
            self.gap = arguments.gap[0]
        if arguments.margin[0] is None:
            self.margin = papersize.parse_length("0")
        else:
            self.margin = arguments.margin[0]
        self.cell_number = (
            self._num_fit(target_size[0], source_size[0]),
            self._num_fit(target_size[1], source_size[1]),
            )

        wasted = (
            self._wasted(target_size[0], self.cell_number[0], source_size[0]),
            self._wasted(target_size[1], self.cell_number[1], source_size[1]),
            )
        self.fit = (
            self.Fit(
                self.margin + wasted[0],
                source_size[0] + self.gap,
                ),
            self.Fit(
                self.margin + wasted[1],
                source_size[1] + self.gap,
                ),
            )

        super().__init__(target_size, arguments, metadata)

    def _wasted(self, dest, num, source):
        return (dest - num * (source + self.gap) - 2 * self.margin + self.gap) / 2

    def _num_fit(self, target, source):
        return int((target - 2 * self.margin + self.gap) // (source + self.gap))

    @property
    def pages_per_page(self):
        return self.cell_number[0] * self.cell_number[1]

    def cell_topleft(self, num):
        width, height = self.cell_number
        return (
            self.fit[0].margin + self.fit[0].sourcex * (num % width),
            self.fit[1].margin + self.fit[1].sourcex * (height - 1 - num // width),
            )
