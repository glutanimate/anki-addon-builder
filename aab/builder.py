# -*- coding: utf-8 -*-
#
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

"""
Main Add-on Builder
"""


import json
import logging
import os
import shutil
import sys
import zipfile
from pathlib import Path
from shutil import which
from typing import Callable, Optional

from . import PATH_DIST, PATH_ROOT
from .config import Config
from .git import Git
from .ui import UIBuilder
from .utils import call_shell, copy_recursively, purge

# these patters will be used by a 'find' command and are case sensitive,
# thus '*', '?', '[]' etc. have a special meaning and maybe must be escaped
_trash_patterns = ["*.pyc", "*.pyo", "__pycache__"]


def clean_repo():
    logging.info("Cleaning repository...")
    if PATH_DIST.exists():
        shutil.rmtree(str(PATH_DIST))
    purge(".", _trash_patterns, recursive=True)


class AddonBuilder:

    _paths_licenses = [PATH_DIST, PATH_DIST / "resources"]
    _path_optional_icons = PATH_ROOT / "resources" / "icons" / "optional"
    _path_changelog = PATH_DIST / "CHANGELOG.md"

    def __init__(
        self,
        version: Optional[str] = None,
        special: Optional[str] = None,
        callback_archive: Callable = None,
    ):
        self._version = version
        self._special = special
        if special:
            if version:
                logging.warning(
                    "Warning: A special option is given. Given version name will be ignored!"
                )
            self._version = Git().parse_version(special)
        elif not version:
            self._version = Git().parse_version(version)  # if version is empty
        # git stash create comes up empty when no changes were made since the
        # last commit. Don't use 'dev' as version in these cases.
        git_status = call_shell("git status --porcelain")
        if self._special == "dev" and git_status == "":
            self._special = "current"
            self._version = Git().parse_version(self._special)
        if not self._version:
            logging.error("Error: Version could not be determined through Git")
            sys.exit(1)
        self._callback_archive = callback_archive
        self._config = Config()
        self._path_dist_module = PATH_DIST / "src" / self._config["module_name"]
        self._path_locales = self._path_dist_module / "locale"

    def build(
        self,
        target: str = "anki21",
        disttype: str = "local",
        pyenv: Optional[str] = None,
    ) -> Path:

        if target != "anki21":
            print("'target' option is deprecated. Only Anki 2.1 builds are supported.")
            target = "anki21"

        logging.info(
            "\n--- Building %s %s for %s ---\n",
            self._config["display_name"],
            self._version,
            disttype,
        )

        self.prebuild()
        
        return self.build_and_package(target=target, disttype=disttype, pyenv=pyenv)
        
    def prebuild(self):
        logging.info(
            "Preparing source tree for %s %s ...",
            self._config["display_name"],
            self._version,
        )

        clean_repo()

        PATH_DIST.mkdir(parents=True)
        Git().archive(self._version, self._special, PATH_DIST)

    def build_and_package(self, target="anki21", disttype="local", pyenv=None):
        self._build(target=target, disttype=disttype, pyenv=pyenv)

        return self._package(target, disttype)

    def _build(self, target="anki21", disttype="local", pyenv=None):
        self._copy_licenses()
        if self._path_changelog.exists():
            self._copy_changelog()
        if self._path_optional_icons.exists():
            self._copy_optional_icons()
        if self._callback_archive:
            self._callback_archive()
        if self._path_locales.exists():
            self._build_locales()

        self._write_manifest(disttype)
        self._build_ui(pyenv)

        return self._package(disttype)

    def _build_ui(self, pyenv: Optional[str]):
        logging.info("Building UI...")
        UIBuilder(root=PATH_DIST).build(pyenv=pyenv)

    def _package(self, disttype: str) -> Path:
        logging.info("Packaging add-on...")
        config = self._config

        to_zip = self._path_dist_module
        ext = "ankiaddon"

        out_name = "{repo_name}-{version}{dist}.{ext}".format(
            repo_name=config["repo_name"],
            version=self._version,
            dist="" if disttype == "local" else "-" + disttype,
            ext=ext,
        )

        out_path = PATH_ROOT / "build" / out_name

        if out_path.exists():
            out_path.unlink()

        with zipfile.ZipFile(str(out_path), "w", zipfile.ZIP_DEFLATED) as myzip:
            rootlen = len(str(to_zip)) + 1
            for root, dirs, files in os.walk(str(to_zip)):
                for file in files:
                    path = os.path.join(root, file)
                    myzip.write(path, path[rootlen:])

        logging.info("Package saved as {out_name}".format(out_name=out_name))
        logging.info("Done.")

        return out_path

    def _write_manifest(self, disttype: str):
        logging.info("Writing manifest...")
        contents = self._config.manifest(
            self._version, self._special, disttype=disttype
        )
        path = self._path_dist_module / "manifest.json"
        with path.open("w", encoding="utf-8") as f:
            f.write(
                str(json.dumps(contents, indent=4, sort_keys=False, ensure_ascii=False))
            )

    def _copy_licenses(self):
        logging.info("Copying licenses...")
        for path in self._paths_licenses:
            if not path.is_dir():
                continue
            for file in path.glob("LICENSE*"):
                target = self._path_dist_module / "{stem}.txt".format(stem=file.stem)
                shutil.copyfile(str(file), str(target))

    def _copy_changelog(self):
        logging.info("Copying changelog...")
        target = self._path_dist_module / "CHANGELOG.md"
        shutil.copy(str(self._path_changelog), str(target))

    def _copy_optional_icons(self):
        logging.info("Copying additional icons...")
        copy_recursively(
            self._path_optional_icons, PATH_DIST / "resources" / "icons" / ""
        )

    def _build_locales(self):
        """
        Tries to compile the '.po' found in the locale directory and replaces them
        by their compiled '.mo' file (the original file will be deleted in the process.

        Does not do anything if the program 'msgfmt' is not found.
        """
        from pipes import quote  # 2.7 compatibility

        logging.info("Compiling locale files...")
        # check whether 'msgfmt' exists, else abort immediately
        if not which("msgfmt"):
            logging.warning("Warning: Could not compile. 'msgfmt' not found.")
            return

        for root, dirs, files in os.walk(str(self._path_locales)):
            for file in files:
                filename, ext = os.path.splitext(self._path_locales / root / file)
                # Only compile files ending with '.po' for now
                if ext == ".po":
                    call_shell(
                        "msgfmt {filename}.po -o {filename}.mo".format(
                            filename=quote(filename)
                        )
                    )
                    os.unlink("{filename}.po".format(filename=filename))
                # and remove .pot files completely
                elif ext == ".pot":
                    os.unlink("{filename}.pot".format(filename=filename))
