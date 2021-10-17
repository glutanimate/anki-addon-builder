from packaging.version import InvalidVersion, Version


def validate_semver(version: str) -> str:
    try:
        _ = Version(version)
    except InvalidVersion:
        raise
    return version
