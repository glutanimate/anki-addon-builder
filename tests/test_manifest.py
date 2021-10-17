from __future__ import annotations

from copy import deepcopy
from typing import Any

import pytest
from pydantic import ValidationError

from aab.manifest.model import AddonManifest, ExtendedAddonManifest

_core_manifest: dict[str, Any] = {
    "package": "sample_addon",
    "name": "Sample Add-on",
}

def test_model_construction():
    assert AddonManifest(**_core_manifest)


def test_fails_on_self_conflict():
    manifest = deepcopy(_core_manifest)
    manifest["conflicts"] = [manifest["package"]]
    with pytest.raises(ValidationError) as exception_info:
        AddonManifest(**manifest)
    assert "conflict with itself" in str(exception_info.value)


def test_fails_on_empty_required_fields():
    manifest = deepcopy(_core_manifest)
    for key in manifest.keys():
        manifest[key] = ""
        with pytest.raises(ValidationError) as exception_info:
            AddonManifest(**manifest)
        assert "at least 1 characters" in str(exception_info.value)


def test_ankiweb_id_constrained():
    manifest = deepcopy(_core_manifest)
    manifest["ankiweb_id"] = "10398301324"
    assert ExtendedAddonManifest(**manifest)
    manifest["ankiweb_id"] = "foo"
    with pytest.raises(ValidationError) as exception_info:
        ExtendedAddonManifest(**manifest)
    assert "does not match regex" in str(exception_info.value)