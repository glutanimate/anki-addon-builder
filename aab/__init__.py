#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Anki Add-on Builder
#
# Copyright (C)  2016-2019 Aristotelis P. <https://glutanimate.com/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version, with the additions
# listed at the end of the license file that accompanied this program.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# NOTE: This program is subject to certain additional terms pursuant to
# Section 7 of the GNU Affero General Public License.  You should have
# received a copy of these additional terms immediately following the
# terms and conditions of the GNU Affero General Public License that
# accompanied this program.
#
# If not, please request a copy through one of the means of contact
# listed here: <https://glutanimate.com/contact/>.
#
# Any modifications to this file must keep this entire header intact.

"""
Handles build tasks for Anki add-ons, including packaging them
to be distributed through AnkiWeb or other channels.

This script presupposes that you have a proper development environment
set up for the Anki version you are targeting, including having tools
like pyrcc4 and pyuic4 (Anki 2.0) or pyrcc5 and pyuic5 (Anki 2.1) in
your PATH.

For instructions on how to set up a development environment for Anki
please refer to Anki's documentation.
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from pathlib import Path

# Meta

__version__ = "0.1.3"
__author__ = "Aristotelis P. (Glutanimate)"
__title__ = "Anki Add-on Builder"
__homepage__ = "https://glutanimate.com"

COPYRIGHT_MSG = """\
{title} v{version}

Copyright (C) 2016-2019  {author}  <{homepage}>

This program comes with ABSOLUTELY NO WARRANTY;
This is free software, and you are welcome to redistribute it
under certain conditions; For details please see the LICENSE file.
""".format(title=__title__, version=__version__, author=__author__,
           homepage=__homepage__)

# Global variables

PATH_ROOT = Path.cwd()
PATH_DIST = PATH_ROOT / "build" / "dist"
PATH_PACKAGE = Path(__file__).resolve().parent
DIST_TYPES = ["local", "ankiweb"]
