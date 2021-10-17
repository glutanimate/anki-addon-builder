from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class AddonManifest(BaseModel):
    package: str = Field(
        ...,
        description=(
            "The module/package the add-on is imported as, i.e. the name of the add-on"
            " folder."
        ),
    )
    name: str = Field(
        ..., description="The name displayed in Anki's UI (e.g. in the add-on list)"
    )
    mod: Optional[float] = Field(
        None, description="The time the add-on was last modified (unix epoch)"
    )
    conflicts: Optional[List[str]] = Field(
        None,
        description="A list of other packages that conflict",
        title="Conflicting Add-ons",
    )
    min_point_version: Optional[float] = Field(
        None, description="the minimum 2.1.x version this add-on supports"
    )
    max_point_version: Optional[float] = Field(
        None,
        description=(
            "If negative, abs(n) is the maximum 2.1.x version this add-on supports. If"
            " positive, indicates version tested on, and is ignored"
        ),
    )
    branch_index: Optional[float] = Field(
        None,
        description="AnkiWeb sends this to indicate which branch the user downloaded",
    )
    human_version: Optional[str] = Field(
        None, description="Human-readable version string set by the add-on creator"
    )
    homepage: Optional[str] = Field(
        None,
        description="Homepage of the add-on project (e.g. GitHub repository link)",
    )


class ExtendedAddonManifest(AddonManifest):
    version: Optional[str] = Field(
        None, description="[aab] Version string, set to the same value as human_version"
    )
    ankiweb_id: Optional[str] = Field(None, description="[aab] The AnkiWeb upload ID.")
    author: Optional[str] = Field(
        None, description="[aab] The main author/maintainer/publisher of the add-on."
    )