from copy import deepcopy

import pytest
from pydantic import ValidationError

from aab.project.model import AddonProperties

_valid_required_properties = {
    "display_name": "Sample Add-on",
    "module_name": "sample_addon",
    "repo_name": "sample-addon",
    "author": "author",
}


def test_model_construction():
    assert AddonProperties(**_valid_required_properties)


def test_fails_on_missing_requirement():
    for key in _valid_required_properties:
        properties = deepcopy(_valid_required_properties)
        del properties[key]
        with pytest.raises(ValidationError) as exception_info:
            AddonProperties(**properties)
        assert "field required" in str(exception_info.value)
        assert key in str(exception_info.value)


@pytest.mark.parametrize(
    "version_key", ("min_anki_version", "max_anki_version", "tested_anki_version")
)
def test_validates_semver(version_key):
    properties = deepcopy(_valid_required_properties)
    properties[version_key] = "first"
    with pytest.raises(ValidationError) as exception_info:
        AddonProperties(**properties)
    assert "Invalid version" in str(exception_info.value)
    assert version_key in str(exception_info.value)
