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

from __future__ import annotations

import json
import time
from copy import deepcopy
from pathlib import Path
from typing import Literal, Optional, Union

DistType = Union[Literal["local"], Literal["ankiweb"]]


from ..project.model import AddonProperties
from .model import AddonManifest, ExtendedAddonManifest


class ManifestUtility:
    @classmethod
    def create_manifest(
        cls,
        properties: AddonProperties,
        version: str,
        distribution_type: DistType,
        target_directory: Path,
    ):
        manifest = ManifestGenerator.manifest(
            properties=properties, version=version, distribution_type=distribution_type
        )
        cls._write_manifest(manifest, target_directory)

    @classmethod
    def _write_manifest(cls, manifest: AddonManifest, target_directory: Path):
        if not target_directory.is_dir():
            raise ValueError(f"Provided path '{target_directory}' is not a directory ")
        manifest_path = target_directory / f"{manifest.json_name}.json"
        manifest_dict = manifest.dict(exclude_none=True)

        with manifest_path.open("w", encoding="utf-8") as manifest_file:
            manifest_file.write(
                json.dumps(manifest_dict, indent=4, sort_keys=False, ensure_ascii=False)
            )


class ManifestGenerator:
    @classmethod
    def manifest(
        cls, properties: AddonProperties, version: str, distribution_type: DistType
    ) -> ExtendedAddonManifest:
        max_point_version = (
            cls._max_point_version(
                max_anki_version=properties.max_anki_version,
                tested_anki_version=properties.tested_anki_version,
            )
            if properties.max_anki_version or properties.tested_anki_version
            else None
        )

        min_point_version = (
            cls._min_point_version(properties.min_anki_version)
            if properties.min_anki_version
            else None
        )

        manifest = ExtendedAddonManifest(
            package=cls._package(properties, distribution_type),
            name=cls._name(properties, distribution_type),
            author=properties.author,
            version=version,
            human_version=version,
            ankiweb_id=properties.ankiweb_id,
            mod=int(time.time()),
            conflicts=cls._conflicts(properties, distribution_type),
            min_point_version=min_point_version,
            max_point_version=max_point_version,
        )

        return manifest

    @staticmethod
    def _package(properties: AddonProperties, distribution_type: DistType) -> str:
        """Determine package name for specified distribution type

        Using a different package name for local and ankiweb distributions allows
        maintaining multiple release branches of the same add-on without running
        the risk of pre-releases being overwritten by patches served via AnkiWeb.

        As `ankiweb_id` is unknown until the add-on is published, we handle this
        special case by constructing a temporary name from `module_name`
        """
        if distribution_type == "local":
            return properties.module_name
        return properties.ankiweb_id or f"{properties.module_name}_ankiweb"

    @staticmethod
    def _name(properties: AddonProperties, distribution_type: DistType) -> str:
        if distribution_type == "local" and properties.local_name_suffix:
            return f"{properties.display_name}{properties.local_name_suffix}"
        return properties.display_name

    @staticmethod
    def _conflicts(
        properties: AddonProperties, distribution_type: DistType
    ) -> list[str] | None:
        if (conflicts := properties.conflicts) is None:
            return None

        conflicts = deepcopy(conflicts)

        branch_conflict: str | None = None

        if distribution_type == "local":
            if properties.local_conflicts_with_ankiweb and properties.ankiweb_id:
                branch_conflict = properties.ankiweb_id
        elif distribution_type == "ankiweb":
            if properties.ankiweb_conflicts_with_local:
                branch_conflict = properties.module_name

        if branch_conflict:
            conflicts.insert(0, branch_conflict)

        return conflicts

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

    @staticmethod
    def _anki_version_to_point_version(version: str) -> int:
        return int(version.split(".")[-1])
