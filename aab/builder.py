#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Anki Add-on Builder
#
# Copyright (C)  2016-2019 Aristotelis P. <https://glutanimate.com/>
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

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import os
import sys
import shutil
import json
import zipfile
import logging

from . import PATH_DIST, PATH_ROOT
from .config import Config
from .git import Git
from .ui import UIBuilder
from .utils import purge, unicode, copy_recursively

_trash_patterns = ["*.pyc", "*.pyo", "__pycache__"]

def clean_repo():
    logging.info("Cleaning repository...")
    if PATH_DIST.exists():
        shutil.rmtree(unicode(PATH_DIST))
    purge(".", _trash_patterns, recursive=True)

class AddonBuilder(object):

    _paths_licenses = [PATH_DIST, PATH_DIST / "resources"]
    _path_optional_icons = PATH_ROOT / "resources" / "icons" / "optional"
    _path_changelog = PATH_DIST / "CHANGELOG.md"

    def __init__(self, version=None, callback_archive=None):
        self._version = self._get_version(version)
        if not self._version:
            logging.error("Error: Version could not be determined from Git")
            sys.exit(1)
        self._callback_archive = callback_archive
        self._config = Config()
        self._path_dist_module = PATH_DIST / \
            "src" / self._config["module_name"]

    def build(self, target="anki21", disttype="local", pyenv=None):
        
        logging.info("\n--- Building %s %s for %s/%s ---\n",
                     self._config["display_name"], self._version,
                     target, disttype)
        
        clean_repo()

        PATH_DIST.mkdir(parents=True)
        Git().archive(self._version, PATH_DIST)

        self._copy_licenses()
        if self._path_changelog.exists():
            self._copy_changelog()
        if self._path_optional_icons.exists():
            self._copy_optional_icons()
        if self._callback_archive:
            self._callback_archive()

        self._write_manifest(disttype)
        self._build_ui(target, pyenv)
        
        return self._package(target, disttype)

    def _build_ui(self, target, pyenv):
        logging.info("Building UI...")
        UIBuilder(root=PATH_DIST).build(target=target, pyenv=pyenv)

    def _get_version(self, version):
        if version is None or version == "release":
            return Git().version()
        elif version == "current":
            return Git().version(commit=True)
        return version

    def _package(self, target, disttype):
        logging.info("Packaging add-on...")
        config = self._config

        if target == "anki21":
            to_zip = self._path_dist_module
            ext = "ankiaddon"
        else:
            to_zip = PATH_DIST / "src"
            ext = "zip"

        out_name = "{repo_name}-{version}-{target}{dist}.{ext}".format(
            repo_name=config["repo_name"], version=self._version,
            target=target,
            dist="" if disttype == "local" else "-" + disttype,
            ext=ext
        )

        out_path = PATH_ROOT / "build" / out_name

        if out_path.exists():
            out_path.unlink()

        with zipfile.ZipFile(unicode(out_path),
                             "w", zipfile.ZIP_DEFLATED) as myzip:
            rootlen = len(unicode(to_zip)) + 1
            for root, dirs, files in os.walk(unicode(to_zip)):
                for file in files:
                    path = os.path.join(root, file)
                    myzip.write(path, path[rootlen:])

        logging.info("Package saved as {out_name}".format(out_name=out_name))
        logging.info("Done.")
        
        return out_path

    def _write_manifest(self, disttype):
        logging.info("Writing manifest...")
        contents = self._config.manifest(self._version, disttype=disttype)
        path = self._path_dist_module / "manifest.json"
        with path.open("w", encoding="utf-8") as f:
            f.write(unicode(json.dumps(contents, indent=4,
                                       sort_keys=False,
                                       ensure_ascii=False)))

    def _copy_licenses(self):
        logging.info("Copying licenses...")
        for path in self._paths_licenses:
            if not path.is_dir():
                continue
            for file in path.glob("LICENSE*"):
                target = (self._path_dist_module /
                          "{stem}.txt".format(stem=file.stem))
                shutil.copyfile(unicode(file), unicode(target))

    def _copy_changelog(self):
        logging.info("Copying changelog...")
        target = self._path_dist_module / "CHANGELOG.md"
        shutil.copy(unicode(self._path_changelog), unicode(target))

    def _copy_optional_icons(self):
        logging.info("Copying additional icons...")
        copy_recursively(self._path_optional_icons,
                         PATH_DIST / "resources" / "icons" / "")
