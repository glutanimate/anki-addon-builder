# -*- coding: utf-8 -*-

# Anki Add-on Builder
#
# Copyright (C)  2016-2022 Aristotelis P. <https://glutanimate.com/>
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

import contextlib
import os
from pathlib import Path
from shutil import copytree
from typing import Union

from aab.config import Config
from aab.ui import QtVersion, UIBuilder

from . import SAMPLE_PROJECT_NAME, SAMPLE_PROJECT_ROOT, SAMPLE_PROJECTS_FOLDER
from .util import list_files


@contextlib.contextmanager
def change_dir(path: Union[Path, str]):
    current = os.getcwd()
    os.chdir(str(path))
    try:
        yield
    finally:
        os.chdir(current)


def test_ui_builder(tmp_path: Path):
    test_project_root = tmp_path / SAMPLE_PROJECT_NAME
    copytree(SAMPLE_PROJECT_ROOT, test_project_root)

    gui_src_path = test_project_root / "src" / "sample_project" / "gui"

    expected_file_structure = """\
gui/
    resources/
        __init__.py
        sample-project/
            icons/
                coffee.svg
                heart.svg
                email.svg
                help.svg
    forms/
        __init__.py
        qt6/
            __init__.py
            dialog.py
        qt5/
            __init__.py
            dialog.py\
"""

    config = Config(test_project_root / "addon.json")

    with change_dir(test_project_root):
        ui_builder = UIBuilder(dist=test_project_root, config=config)

        ui_builder.build(QtVersion.qt5)
        ui_builder.build(QtVersion.qt6)
        ui_builder.create_qt_shim()

    assert (
        list_files(gui_src_path) == expected_file_structure
    ), "Issue with GUI file structure"

    with (gui_src_path / "forms" / "qt6" / "dialog.py").open("r") as f:
        qt6_form_contents = f.read()
    with (gui_src_path / "forms" / "qt5" / "dialog.py").open("r") as f:
        qt5_form_contents = f.read()

    assert (
        '"sample-project:icons/help.svg"' in qt6_form_contents
    ), "Base icon not properly remapped"
    assert (
        '"sample-project:icons/coffee.svg"' in qt6_form_contents
    ), "Optional icon not properly remapped"

    assert "icons_rc" not in qt5_form_contents

    expected_shim_snippet = """\
from typing import TYPE_CHECKING

from aqt.qt import qtmajor

if TYPE_CHECKING or qtmajor >= 6:
    from .qt6 import *  # noqa: F401
else:
    from .qt5 import *  # noqa: F401\
"""

    with (gui_src_path / "forms" / "__init__.py").open("r") as f:
        shim_contents = f.read()

    assert expected_shim_snippet in shim_contents, "Qt shim not properly constructed"


def test_resources_only_no_forms(tmp_path: Path):
    test_project_root = tmp_path / "project-with-no-forms"
    sample_project_root = SAMPLE_PROJECTS_FOLDER / "project-with-no-forms"
    copytree(sample_project_root, test_project_root)

    gui_src_path = test_project_root / "src" / "sample_project" / "gui"

    expected_file_structure = """\
gui/
    resources/
        __init__.py
        sample-project/
            icons/
                coffee.svg
                heart.svg
                email.svg
                help.svg\
"""

    config = Config(test_project_root / "addon.json")

    with change_dir(test_project_root):
        ui_builder = UIBuilder(dist=test_project_root, config=config)

        assert ui_builder.build(QtVersion.qt5) is False
        assert ui_builder.build(QtVersion.qt6) is False
        assert ui_builder.create_qt_shim() is False

    assert (
        list_files(gui_src_path) == expected_file_structure
    ), "Issue with GUI file structure"
