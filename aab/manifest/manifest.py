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

import json
import logging
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, Literal, Optional, Union

from .config import Config
from .git import Git

DistType = Union[Literal["local"], Literal["ankiweb"]]


class ManifestUtils:
    @classmethod
    def generate_and_write_manifest(
        cls,
        addon_properties: Config,
        version: str,
        dist_type: DistType,
        target_dir: Path,
    ):
        logging.info("Writing manifest...")
        manifest = cls.generate_manifest_from_properties(
            addon_properties=addon_properties, version=version, dist_type=dist_type
        )
        cls.write_manifest(manifest=manifest, target_dir=target_dir)

    @classmethod
    def generate_manifest_from_properties(
        cls,
        addon_properties: Config,
        version: str,
        dist_type: DistType,
    ) -> Dict[str, Any]:
        manifest = {
            "name": addon_properties["display_name"],
            "package": addon_properties["module_name"],
            "ankiweb_id": addon_properties["ankiweb_id"],
            "author": addon_properties["author"],
            "version": version,
            "homepage": addon_properties.get("homepage", ""),
            "conflicts": deepcopy(addon_properties["conflicts"]),
            "mod": Git().modtime(version),
        }

        # Add version specifiers:

        min_anki_version = addon_properties.get("min_anki_version")
        max_anki_version = addon_properties.get("max_anki_version")
        tested_anki_version = addon_properties.get("tested_anki_version")

        if min_anki_version:
            manifest["min_point_version"] = cls._min_point_version(min_anki_version)

        if max_anki_version or tested_anki_version:
            manifest["max_point_version"] = cls._max_point_version(
                max_anki_version, tested_anki_version
            )

        # Update values for distribution type
        if dist_type == "local":
            if (
                addon_properties.get("local_conflicts_with_ankiweb", True)
                and addon_properties["ankiweb_id"]
            ):
                manifest["conflicts"].insert(0, addon_properties["ankiweb_id"])
        elif dist_type == "ankiweb":
            if (
                addon_properties.get("ankiweb_conflicts_with_local", True)
                and addon_properties["module_name"]
            ):
                manifest["conflicts"].insert(0, addon_properties["module_name"])

            # This is inconsistent, but we can't do much else when
            # ankiweb_id is still unknown (i.e. first upload):
            manifest["package"] = (
                addon_properties["ankiweb_id"] or addon_properties["module_name"]
            )

        return manifest

    @classmethod
    def write_manifest(cls, manifest: Dict[str, Any], target_dir: Path):
        target_path = target_dir / "manifest.json"
        with target_path.open("w", encoding="utf-8") as manifest_file:
            manifest_file.write(
                json.dumps(manifest, indent=4, sort_keys=False, ensure_ascii=False)
            )

    @classmethod
    def _anki_version_to_point_version(cls, version: str) -> int:
        return int(version.split(".")[-1])

    @classmethod
    def _min_point_version(cls, min_anki_version: str) -> int:
        return cls._anki_version_to_point_version(min_anki_version)

    @classmethod
    def _max_point_version(
        cls, max_anki_version: Optional[str], tested_anki_version: Optional[str]
    ) -> Optional[int]:
        if max_anki_version:
            # -version in "max_point_version" specifies a definite max supported version
            return -1 * cls._anki_version_to_point_version(max_anki_version)
        elif tested_anki_version:
            # +version in "max_point_version" indicates version tested on
            return cls._anki_version_to_point_version(tested_anki_version)
        return None


####



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
        self.data = self.__read()

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

    def __read(self) -> dict:
        try:
            with self._path.open(encoding="utf-8") as f:
                data = json.loads(f.read())
            jsonschema.validate(data, _SCHEMAS["addon"])
            return data
        except (IOError, OSError, ValueError, ValidationError):
            logging.error(
                "Error: Could not read '{}'. Traceback follows below:\n".format(
                    self._path.name
                )
            )
            raise

    def __write(self, data: dict):
        try:
            with self._path.open("w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=False)
        except (IOError, OSError):
            logging.error(
                "Error: Could not write to '{}'. Traceback follows below:\n".format(
                    self._path.name
                )
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
        name = self.data["display_name"]
        if self.data.get("local_dist_suffix"):
            name += self.data["local_name_suffix"]
        return name

    def _package(self, build_props: dict):
        # this is inconsistent, but we can't do much else when
        # ankiweb_id is still unknown (i.e. first upload):
        if build_props["dist"] == "ankiweb" and self.data["module_name"]:
            return self.data.get("ankiweb_id") or self.data["module_name"] + "_ankiweb"

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

    def _mod(self, build_props: dict) -> int:
        return build_props["mod"]

    def _conflicts(self, build_props: dict) -> List[str]:
        # Update values for distribution type
        conflicts = copy.copy(self.data.get("conflicts", []))
        self_conflict = None

        if build_props["dist"] == "local":
            if self.data.get("local_conflicts_with_ankiweb", True) and self.data.get(
                "ankiweb_id"
            ):
                self_conflict = self.data.get("ankiweb_id")
        elif build_props["dist"] == "ankiweb":
            if self.data.get("ankiweb_conflicts_with_local", True) and self.data.get(
                "module_name"
            ):
                self_conflict = self.data.get("module_name")

            self_conflict = self.data["module_name"]

        if self_conflict:
            conflicts.insert(0, self_conflict)

        return conflicts

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