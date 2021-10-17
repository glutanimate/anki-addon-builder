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

from pydantic import BaseModel, Field, validator

from ..shared.validators import validate_semver


class AddonManifest(BaseModel, title="Anki add-on manifest"):

    json_name: ClassVar[str] = "manifest"  # json file name stem

    package: str = Field(
        ...,
        description=(
            "The package the add-on is imported as, i.e. the name of the add-on folder."
        ),
        min_length=1,
    )
    name: str = Field(
        ...,
        description="The name displayed in Anki's GUI (e.g. in the add-on list)",
        min_length=1,
    )
    mod: Optional[int] = Field(
        default=None,
        description="The time the add-on was last modified (unix timestamp in seconds)",
        gt=0,
    )
    conflicts: Optional[List[str]] = Field(
        default=None,
        description="A list of other packages that conflict with the add-on",
    )
    min_point_version: Optional[int] = Field(
        default=None, description="the minimum 2.1.x version this add-on supports", gt=0
    )
    max_point_version: Optional[int] = Field(
        default=None,
        description=(
            "If negative, abs(n) is the maximum 2.1.x version this add-on supports. If"
            " positive, indicates version tested on, and is ignored"
        ),
    )
    branch_index: Optional[int] = Field(
        default=None,
        description="AnkiWeb sends this to indicate which branch the user downloaded",
    )
    human_version: Optional[str] = Field(
        default=None,
        description="Human-readable version string set by the add-on creator",
    )
    homepage: Optional[str] = Field(
        default=None,
        description="Homepage of the add-on project (e.g. GitHub repository link)",
    )

    @validator("conflicts", each_item=True)
    def check_conflicts(cls, conflict: str, values: dict):
        if len(conflict) < 1:
            raise ValueError("Conflict specifier cannot be an empty string.")
        if conflict == values.get("package"):
            raise ValueError("Add-on can not conflict with itself.")
        return conflict


class ExtendedAddonManifest(
    AddonManifest, title="Extended Anki add-on manifest, as used by Anki Add-on Builder"
):
    version: Optional[str] = Field(
        default=None,
        description="[aab] Version string, set to the same value as human_version",
    )
    ankiweb_id: Optional[str] = Field(
        default=None, description="[aab] The AnkiWeb upload ID.", regex=r"[0-9]+"
    )
    author: Optional[str] = Field(
        default=None,
        description="[aab] The main author/maintainer/publisher of the add-on.",
    )

    _validate_versions = validator("version", allow_reuse=True)(validate_semver)
