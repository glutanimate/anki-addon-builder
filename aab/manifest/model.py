from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field, validator


class AddonManifest(BaseModel):
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


class ExtendedAddonManifest(AddonManifest):
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
