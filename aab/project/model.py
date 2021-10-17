from __future__ import annotations

from typing import ClassVar, List, Optional

from packaging.version import InvalidVersion, Version
from pydantic import AnyHttpUrl, BaseModel, Field, validator


class AddonProperties(BaseModel):
    json_name: ClassVar[str] = "addon"

    class Config:
        title = "Anki Add-on Builder Add-on Specification"
        schema_extra = {
            "description": (
                "JSON schema for the addon.json configuration files used by Anki Add-on"
                " Builder"
            )
        }

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
        None,
        description=(
            "A suffix to the display name to apply when creating builds for non-ankiweb"
            " distribution."
        ),
    )
    ankiweb_id: Optional[str] = Field(None, description="The AnkiWeb upload ID.")
    version: Optional[str] = Field(
        None,
        description=(
            "Add-on version string. Needs to follow semantic versioning guidelines."
        ),
    )
    author: str = Field(
        ..., description="The main author/maintainer/publisher of the add-on."
    )
    contact: Optional[str] = Field(
        None,
        description=(
            "Contact details to list for the author (e.g. either a website or email)"
        ),
    )
    homepage: Optional[AnyHttpUrl] = Field(
        None, description="Homepage of the add-on project (e.g. GitHub repository link)"
    )
    tags: Optional[str] = Field(
        None,
        description=(
            "Space-delimited list of tags that characterize the add-on on AnkiWeb."
        ),
    )
    copyright_start: Optional[int] = Field(
        None,
        description=(
            "Starting year to list for automatically generated copyright headers."
        ),
    )
    conflicts: Optional[List[str]] = Field(
        None,
        description=(
            "A list of other AnkiWeb add-on IDs or package names that conflict with"
            " this add-on."
        ),
        title="Conflicting Add-ons",
    )
    ankiweb_conflicts_with_local: Optional[bool] = Field(True, description="TODO")
    local_conflicts_with_ankiweb: Optional[bool] = Field(True, description="TODO")
    min_anki_version: Optional[str] = Field(
        None,
        description=(
            "SemVer version string describing the minimum required Anki version to run"
            " this add-on."
        ),
    )
    max_anki_version: Optional[str] = Field(
        None,
        description=(
            "SemVer version string describing the maximum supported Anki version of"
            " this add-on"
        ),
    )
    tested_anki_version: Optional[str] = Field(
        None,
        description=(
            "SemVer version string describing the latest Anki version this add-on was"
            " tested on."
        ),
    )

    @validator("min_anki_version", "max_anki_version", "tested_anki_version")
    def check_semver(cls, value: str):
        try:
            _ = Version(value)
        except InvalidVersion:
            raise
        return value
