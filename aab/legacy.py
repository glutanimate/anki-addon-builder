#!/usr/bin/env python
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

"""
Limited support for porting legacy Qt5 features to Qt6
"""

import shutil
import xml.etree.ElementTree as ElementTree
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

TAG_RCC = "RCC"
TAG_RESOURCE = "qresource"
TAG_FILE = "file"

ATTRIBUTE_PREFIX = "prefix"
ATTRIBUTE_ALIAS = "alias"


@dataclass
class QResourceFileDescriptor:
    relative_path: str
    alias: Optional[str] = None


@dataclass
class QResourceDescriptor:
    prefix: str
    parent_path: Path
    files: List[QResourceFileDescriptor]


class QRCParseError(ElementTree.ParseError):
    pass


class QRCParser:
    def __init__(self, qrc_path: Path):
        self._parent_path = qrc_path.parent

        try:
            self._root = ElementTree.parse(qrc_path).getroot()
        except Exception as e:
            raise e

        if self._root.tag != TAG_RCC:
            raise QRCParseError(f"Invalid qrc file: {TAG_RCC} tag not found at root")

    def get_qresources(self) -> List[QResourceDescriptor]:
        resources: List[QResourceDescriptor] = []

        for resource in self._root.findall(TAG_RESOURCE):
            prefix = resource.get(ATTRIBUTE_PREFIX)
            if not prefix:
                raise QRCParseError(
                    "qresource definitions without a prefix attribute are currently not"
                    " supported"
                )
            prefix = self._clean_prefix(prefix)

            files: List[QResourceFileDescriptor] = []

            for file in resource.findall(TAG_FILE):
                relative_path = file.text
                if relative_path is None:
                    raise QRCParseError("file path cannot be None")
                alias = file.get(ATTRIBUTE_ALIAS)
                files.append(
                    QResourceFileDescriptor(relative_path=relative_path, alias=alias)
                )

            resources.append(
                QResourceDescriptor(
                    prefix=prefix, parent_path=self._parent_path, files=files
                )
            )

        return resources

    def _clean_prefix(self, prefix: str) -> str:
        if prefix.startswith("/"):
            prefix = prefix[1:]
        if prefix.endswith("/"):
            prefix = prefix[:-1]
        return prefix


class QRCMigrator:

    _qdir_import = """from aqt.qt import QDir\n"""

    _asset_folder = "assets"

    def __init__(self, gui_path: Path):
        self._target_root_path = gui_path / self._asset_folder

    def migrate_resources(self, resources: List[QResourceDescriptor]) -> str:
        """returns QDir initialization command"""

        qdir_commands: List[str] = [self._qdir_import]

        for resource in resources:
            prefix = resource.prefix
            source_parent_path = resource.parent_path

            for file in resource.files:
                source_relative_path = file.relative_path
                alias = file.alias

                target_relative_path = source_relative_path if not alias else alias

                source_path = source_parent_path / source_relative_path
                target_path = self._target_root_path / target_relative_path

                if target_path.exists():
                    target_path.unlink()

                is_dir = False
                if source_path.is_dir():
                    target_path.mkdir(parents=True, exist_ok=True)
                    is_dir = True
                elif not target_path.parent.exists():
                    target_path.parent.mkdir(parents=True, exist_ok=True)

                if is_dir:
                    shutil.copytree(source_path, target_path)
                else:
                    shutil.copy(source_path, target_path)

            qdir_commands.append(self._build_qdir_command(prefix))

        initialization_snippet = "\n".join(qdir_commands) + "\n"

        return initialization_snippet

    def _build_qdir_command(self, prefix: str):
        prefix_path = self._target_root_path / prefix

        return f"""QDir.addSearchpath("{prefix}", "{prefix_path}")"""
