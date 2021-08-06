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
