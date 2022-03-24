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

from pathlib import Path
from shutil import copytree

from aab.legacy import (
    QRCMigrator,
    QRCParser,
    QResourceDescriptor,
    QResourceFileDescriptor,
)

from .util import list_files

SAMPLE_PROJECT_NAME = "sample-project"

_sample_project_root = Path(__file__).parent / "data" / SAMPLE_PROJECT_NAME

_qrc_sample_resources = [
    QResourceDescriptor(
        prefix="sample-project",
        parent_path=(_sample_project_root / "resources").resolve(),
        files=[
            QResourceFileDescriptor(relative_path="icons/help.svg", alias=None),
            QResourceFileDescriptor(relative_path="icons/heart.svg", alias=None),
            QResourceFileDescriptor(
                relative_path="icons/optional/coffee.svg", alias="icons/coffee.svg"
            ),
            QResourceFileDescriptor(
                relative_path="icons/optional/email.svg", alias="icons/email.svg"
            ),
        ],
    )
]


def test_qrc_parser():
    qrc_path = _sample_project_root / "resources" / "icons.qrc"
    parser = QRCParser(qrc_path=qrc_path)

    expected = _qrc_sample_resources

    actual = parser.get_qresources()

    assert actual == expected


def test_qrc_migrator(tmp_path: Path):
    test_project_root = tmp_path / SAMPLE_PROJECT_NAME
    copytree(_sample_project_root, test_project_root)

    gui_src_path = test_project_root / "src" / "sample_project" / "gui"

    migrator = QRCMigrator(gui_path=gui_src_path)

    expected_integration_snippet = """
from pathlib import Path
from aqt.qt import QDir

def initialize_qt_resources():
    QDir.addSearchPath("sample-project", str(Path(__file__).parent / "sample-project"))

initialize_qt_resources()
"""

    actual_migration_snippet = migrator.migrate_resources(
        resources=_qrc_sample_resources
    )

    assert actual_migration_snippet == expected_integration_snippet

    expected_file_structure = """\
gui/
    resources/
        sample-project/
            icons/
                coffee.svg
                heart.svg
                email.svg
                help.svg\
"""

    assert expected_file_structure == list_files(gui_src_path)
