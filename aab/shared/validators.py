from packaging.version import InvalidVersion, Version


def validate_semver(version: str) -> str:
    try:
        _ = Version(version)
    except InvalidVersion:
        raise ValueError(
            f"Version string '{version}' does not conform to semantic versioning"
        )
    return version
