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
Project config parser
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import json
import logging
from copy import copy
from typing import Optional

import jsonschema
from jsonschema.exceptions import ValidationError
from six.moves import UserDict

from . import PATH_PACKAGE, PATH_ROOT
from .git import Git

PATH_CONFIG = PATH_ROOT / "addon.json"


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

    def manifest(self, version, disttype="local"):
        config = self.data
        manifest = {
            "name": config["display_name"],
            "package": config["module_name"],
            "ankiweb_id": config["ankiweb_id"],
            "author": config["author"],
            "version": version,
            "homepage": config.get("homepage", ""),
            "conflicts": copy(config["conflicts"]),
            "mod": Git().modtime(version),
        }

        # Add version specifiers:

        min_anki_version = config.get("min_anki_version")
        max_anki_version = config.get("max_anki_version")
        tested_anki_version = config.get("tested_anki_version")

        if min_anki_version:
            manifest["min_point_version"] = self._min_point_version(min_anki_version)

        if max_anki_version or tested_anki_version:
            manifest["max_point_version"] = self._max_point_version(
                max_anki_version, tested_anki_version
            )

        # Update values for distribution type
        if disttype == "local":
            if (
                config.get("local_conflicts_with_ankiweb", True)
                and config["ankiweb_id"]
            ):
                manifest["conflicts"].insert(0, config["ankiweb_id"])
        elif disttype == "ankiweb":
            if (
                config.get("ankiweb_conflicts_with_local", True)
                and config["module_name"]
            ):
                manifest["conflicts"].insert(0, config["module_name"])

            # This is inconsistent, but we can't do much else when
            # ankiweb_id is still unknown (i.e. first upload):
            manifest["package"] = config["ankiweb_id"] or config["module_name"]

        return manifest

    def _anki_version_to_point_version(self, version: str) -> int:
        return int(version.split(".")[-1])

    def _min_point_version(self, min_anki_version: str) -> int:
        return self._anki_version_to_point_version(min_anki_version)

    def _max_point_version(
        self, max_anki_version: Optional[str], tested_anki_version: Optional[str]
    ) -> Optional[int]:
        if max_anki_version:
            # -version in "max_point_version" specifies a definite max supported version
            return -1 * self._anki_version_to_point_version(max_anki_version)
        elif tested_anki_version:
            # +version in "max_point_version" indicates version tested on
            return self._anki_version_to_point_version(tested_anki_version)
        return None
