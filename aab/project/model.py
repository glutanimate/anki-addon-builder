# -*- coding: utf-8 -*-
# Anki Add-on Builder
#
# Copyright (C)  2016-2021 Aristotelis P. <https://glutanimate.com/>
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

from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic import AnyHttpUrl, BaseModel, Field, validator

from ..shared.validators import validate_semver


class AddonProperties(
    BaseModel, title="Add-on properties, as managed by Anki Add-on Builder"
):
    json_name: ClassVar[str] = "addon"  # json file name stem

    display_name: str = Field(
        ..., description="The name displayed in Anki's UI (e.g. in the add-on list)"
    )
    module_name: str = Field(
        ...,
        description=(
            "The module/package the add-on is imported as, i.e. the name of the add-on"
            " folder."
        ),
    )
    repo_name: str = Field(
        ...,
        description=(
            "The name of the git repository the add-on is hosted in. Currently only"
            " used for build names."
        ),
    )
    local_name_suffix: Optional[str] = Field(
        default=None,
        description=(
            "A suffix to the display name to apply when creating builds for non-ankiweb"
            " distribution."
        ),
        min_length=1
    )
    ankiweb_id: Optional[str] = Field(
        default=None, description="The AnkiWeb upload ID."
    )
    version: Optional[str] = Field(
        default=None,
        description=(
            "Add-on version string. Needs to follow semantic versioning guidelines."
        ),
    )
    author: str = Field(
        ..., description="The main author/maintainer/publisher of the add-on."
    )
    contact: Optional[str] = Field(
        default=None,
        description=(
            "Contact details to list for the author (e.g. either a website or email)"
        ),
    )
    homepage: Optional[AnyHttpUrl] = Field(
        default=None,
        description="Homepage of the add-on project (e.g. GitHub repository link)",
    )
    tags: Optional[str] = Field(
        default=None,
        description=(
            "Space-delimited list of tags that characterize the add-on on AnkiWeb."
        ),
    )
    copyright_start: Optional[int] = Field(
        default=None,
        description=(
            "Starting year to list for automatically generated copyright headers."
        ),
    )
    conflicts: Optional[List[str]] = Field(
        default=None,
        description=(
            "A list of other AnkiWeb add-on IDs or package names that conflict with"
            " this add-on."
        ),
        title="Conflicting Add-ons",
    )
    ankiweb_conflicts_with_local: Optional[bool] = Field(
        default=True, description="TODO"
    )
    local_conflicts_with_ankiweb: Optional[bool] = Field(
        default=True, description="TODO"
    )
    min_anki_version: Optional[str] = Field(
        default=None,
        description=(
            "SemVer version string describing the minimum required Anki version to run"
            " this add-on."
        ),
    )
    max_anki_version: Optional[str] = Field(
        default=None,
        description=(
            "SemVer version string describing the maximum supported Anki version of"
            " this add-on"
        ),
    )
    tested_anki_version: Optional[str] = Field(
        default=None,
        description=(
            "SemVer version string describing the latest Anki version this add-on was"
            " tested on."
        ),
    )

    _validate_versions = validator(
        "min_anki_version", "max_anki_version", "tested_anki_version", allow_reuse=True
    )(validate_semver)
