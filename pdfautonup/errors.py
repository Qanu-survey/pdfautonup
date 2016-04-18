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

"""Errors and exceptions"""

class PdfAutoNupError(Exception):
    """Generic error for pdfautonup"""
    pass

class UserCancel(PdfAutoNupError):
    """Action cancelled by user."""

    def __str__(self):
        return ""

class CouldNotParse(PdfAutoNupError):
    """Could not parse string as a paper size."""

    def __init__(self, string):
        super().__init__()
        self.string = string

    def __str__(self):
        return "Could not parse paper size '{}'.".format(self.string)

class InputFileError(PdfAutoNupError):
    """Error while reading input file."""

    def __init__(self, filename, error):
        super().__init__()
        self.filename = filename
        self.error = error

    def __str__(self):
        return "Error while reading file '{}': {}".format(self.filename, str(self.error))

class GeometryError(PdfAutoNupError):
    """Error about page or file geometry."""

    def __init__(self, string):
        super().__init__()
        self.string = string

    def __str__(self):
        return "[Geometry error] " + self.string
