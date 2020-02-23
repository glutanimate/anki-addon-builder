# -*- coding: utf-8 -*-
# Anki Add-on Builder
#
# Copyright (C)  2016-2020 Aristotelis P. <https://glutanimate.com/>
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

from pathlib import Path

import py
import pytest
from jsonschema.exceptions import ValidationError

from aab.config import Config

SAMPLE_CONFIGS_PATH = str(Path(".") / "tests" / "test-data" / "configs")


@pytest.mark.datafiles(SAMPLE_CONFIGS_PATH)
def test_config_init(datafiles: py.path):
    correct_configs_path = Path(datafiles) / "correct"

    for config_path in correct_configs_path.iterdir():
        assert Config(path=config_path)


@pytest.mark.datafiles(SAMPLE_CONFIGS_PATH)
def test_config_validates_schema(datafiles: py.path):
    incorrect_configs_path = Path(datafiles) / "incorrect"

    for config_path in incorrect_configs_path.iterdir():
        with pytest.raises(ValidationError):
            Config(path=config_path)


@pytest.mark.datafiles(SAMPLE_CONFIGS_PATH)
def test_generate_manifest(datafiles: py.path):
    config_path = Path(datafiles) / "correct" / "full.json"

    config = Config(path=config_path)
    
    build_props = {
        "dist": "ankiweb",
        "mod": 0
    }
    
    print(config.manifest(build_props))
