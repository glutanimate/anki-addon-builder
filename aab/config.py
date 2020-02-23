# -*- coding: utf-8 -*-
# Anki Add-on Builder
#
# Copyright (C)  2016-2020 Aristotelis P. <https://glutanimate.com/>
#                and contributors
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
from collections import UserDict
from pathlib import Path
from typing import Any, Dict, Optional

from packaging.version import Version, InvalidVersion

import jsonschema
from jsonschema.exceptions import ValidationError

from . import PATH_PACKAGE, PATH_ROOT

PATH_CONFIG = PATH_ROOT / "addon.json"


_SCHEMAS: Dict[str, dict] = {}
for schema_name in ("addon", "manifest"):
    with (PATH_PACKAGE / "schemas" / f"{schema_name}.schema.json").open(
        "r", encoding="utf-8"
    ) as schema_file:
        _SCHEMAS[schema_name] = json.loads(schema_file.read())


class ConfigError(Exception):
    pass


class Config(UserDict):

    """
    Simple dictionary-like interface to addon.json
    """

    def __init__(self, path: Optional[Path] = None):
        self._path = path or PATH_CONFIG

        try:
            with self._path.open(encoding="utf-8") as f:
                data = json.loads(f.read())
            jsonschema.validate(data, _SCHEMAS["addon"])
            self.data = data
        except (IOError, OSError, ValueError, ValidationError):
            logging.error(
                "Error: Could not read '{}'. Traceback follows "
                "below:\n".format(self._path.name)
            )
            raise

    # Public API

    def manifest(self, build_props: dict) -> dict:
        _manifest: Dict[str, Any] = {}

        for manifest_key in _SCHEMAS["manifest"]["properties"].keys():
            try:
                getter = getattr(self, f"_{manifest_key}", None)
                value = getter(build_props) if getter else None
            except AttributeError:
                value = self.data[manifest_key]
            except Exception:
                print("Missing mapping between addon.json and manifest.json")
                raise

            if value:
                _manifest[manifest_key] = value

        return _manifest

    # Dictionary interface

    def __setitem__(self, name: str, value: Any):
        self.data[name] = value
        self.__write(self.data)

    # File system access

    def __write(self, data: dict):
        try:
            with self._path.open("w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=False)
        except (IOError, OSError):
            logging.error(
                "Error: Could not write to '{}'. Traceback follows "
                "below:\n".format(self._path.name)
            )
            raise

    # Helper methods

    def __anki_version_to_point_version(self, version: str) -> int:
        return int(version.split(".")[-1])

    def __validate_semver(self, version: str) -> bool:
        try:
            Version(version)
        except InvalidVersion:
            return False
        return True

    # Manifest value getters

    def _name(self, build_props: dict):
        return self.data["display_name"]

    def _package(self, build_props: dict):
        # this is inconsistent, but we can't do much else when
        # ankiweb_id is still unknown (i.e. first upload):
        if build_props["dist"] == "ankiweb" and self.data["module_name"]:
            return self.data.get("ankiweb_id") or self.data["module_name"]

    def _min_point_version(self, build_props: dict):
        key = "min_anki_version"
        if self.data.get(key):
            return self.__anki_version_to_point_version(self.data[key])

    def _max_point_version(self, build_props: dict) -> Optional[int]:
        if self.data.get("max_anki_version"):
            # -version in "max_point_version" specifies a definite max supported version
            return -1 * self.__anki_version_to_point_version(
                self.data["max_anki_version"]
            )
        elif self.data.get("tested_anki_version"):
            # +version in "max_point_version" indicates version tested on
            return self.__anki_version_to_point_version(
                self.data["tested_anki_version"]
            )
        return None

    def _mod(self, build_props: dict):
        return build_props["mod"]

    def _conflicts(self, build_props: dict):
        # Update values for distribution type
        if build_props["dist"] == "local" and self.data.get("ankiweb_id"):
            return [self.data["ankiweb_id"]] + self.data.get("conflicts", [])
        elif build_props["dist"] == "ankiweb" and self.data["module_name"]:
            return [self.data["module_name"]] + self.data.get("conflicts", [])

    def _human_version(self, build_props: dict):
        return self._version(build_props)

    def _version(self, build_props: dict) -> Optional[str]:
        version = self.data.get("version")
        if not version:
            return None

        if not self.__validate_semver(version):
            raise ConfigError(
                f"Version string '{version}' does not conform to semantic versioning"
            )
        return self.data["version"]
