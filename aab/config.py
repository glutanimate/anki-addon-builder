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

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import json
import logging

import jsonschema
from jsonschema.exceptions import ValidationError

from . import PATH_ROOT, PATH_PACKAGE
from .git import Git

PATH_CONFIG = PATH_ROOT / "addon.json"

class Config(object):

    """
    Initialize a read-only add-on config object
    """
    
    with (PATH_PACKAGE / "schema.json").open("r", encoding="utf-8") as f:
        _schema = json.loads(f.read())

    def __init__(self):
        try:
            with PATH_CONFIG.open(encoding="utf-8") as f:
                self._dict = json.loads(f.read())
            jsonschema.validate(self._dict, self._schema)
        except (IOError, OSError, ValueError, ValidationError):
            self._dict = None
            logging.error("Error: Could not read '{}'. Traceback follows "
                          "below:\n".format(PATH_CONFIG.name))
            raise

    def get(self, name):
        return self._dict.get(name)

    def __getitem__(self, name):
        return self._dict[name]

    def __str__(self):
        return self._dict.__str__()

    def __repr__(self):
        return self._dict.__repr__()

    def manifest(self, version, disttype="local"):
        config = self._dict
        manifest = {
            "name": config["display_name"],
            "package": config["module_name"],
            "ankiweb_id": config["ankiweb_id"],
            "author": config["author"],
            "version": version,
            "homepage": config.get("homepage", ""),
            "conflicts": config["conflicts"],
            "mod": Git().modtime(version)
        }

        # Update values for distribution type
        if disttype == "local" and config["ankiweb_id"]:
            manifest["conflicts"].insert(0, config["ankiweb_id"])
        elif disttype == "ankiweb" and config["module_name"]:
            manifest["conflicts"].insert(0, config["module_name"])
            # this is inconsistent, but we can't do much else when
            # ankiweb_id is still unknown (i.e. first upload):
            manifest["package"] = config["ankiweb_id"] or config["module_name"]

        return manifest
