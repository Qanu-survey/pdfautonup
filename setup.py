#!/usr/bin/env python3

# Copyright 2014 Louis Paternault
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

"""Installateur"""

from setuptools import setup, find_packages

from pdfautonup import VERSION

setup(
        name='PdfAutoNup',
        version=VERSION,
        packages=find_packages(),
        install_requires=[], # TODO
        include_package_data=True,
        author='Louis Paternault',
        author_email='spalax@gresille.org',
        description="Convert PDF files to 'n-up' PDF files, guessing the output layout.",
        #url='http://paternault.fr/informatique/prof', # TODO
        license="GPLv3 or any later version",
        #test_suite="jouets.test:suite",
        entry_points={
            'console_scripts': ['pdfautonup = pdfautonup.main:main']
            },
        #classifiers=[], # TODO
        #long_description="" # TODO
)
