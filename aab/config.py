# -*- coding: utf-8 -*-

# Anki Add-on Builder
#
# Copyright (C)  2016-2021 Aristotelis P. <https://glutanimate.com/>
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
Project config parser
"""

import json
import logging

import jsonschema
from jsonschema.exceptions import ValidationError

from collections import UserDict

from . import PATH_PACKAGE, PATH_PROJECT_ROOT

PATH_CONFIG = PATH_PROJECT_ROOT / "addon.json"


class Config(UserDict):

    """
    Simple dictionary-like interface to the repository config file
    """

    with (PATH_PACKAGE / "schema.json").open("r", encoding="utf-8") as f:
        _schema = json.loads(f.read())

    def __init__(self, path=None):
        self._path = path or PATH_CONFIG
        try:
            with self._path.open(encoding="utf-8") as f:
                data = json.loads(f.read())
            jsonschema.validate(data, self._schema)
            self.data = data
        except (IOError, OSError, ValueError, ValidationError):
            logging.error(
                "Error: Could not read '{}'. Traceback follows "
                "below:\n".format(self._path.name)
            )
            raise

    def __setitem__(self, name, value):
        self.data[name] = value
        self._write(self.data)

    def _write(self, data):
        try:
            with self._path.open("w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=False)
        except (IOError, OSError):
            logging.error(
                "Error: Could not write to '{}'. Traceback follows "
                "below:\n".format(self._path.name)
            )
            raise
