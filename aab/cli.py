#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Anki Add-on Builder
#
# Copyright (C)  2016-2021 Aristotelis P. <https://glutanimate.com/>
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


from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import logging
import argparse

from six import PY2

from . import PATH_ROOT, COPYRIGHT_MSG, DIST_TYPES
from .config import Config, PATH_CONFIG
from .builder import AddonBuilder, clean_repo
from .ui import UIBuilder, write_qt_shim
from .manifest import ManifestUtils
from .git import Git


# Checks
##############################################################################


def validate_cwd():
    required = (PATH_ROOT / "src", PATH_CONFIG)
    for path in required:
        if not path.exists():
            print(
                "Error: {dir} not found. Please run this script from "
                "the project root.".format(dir=path.name)
            )
            return False
    return True


# Entry points
##############################################################################


def build(args):
    targets = [args.target] if args.target != "all" else Config()["targets"]
    dists = [args.dist] if args.dist != "all" else DIST_TYPES

    builder = AddonBuilder(version=args.version)

    cnt = 1
    total = len(targets) * len(dists)
    for target in targets:
        for dist in dists:
            logging.info("\n=== Build task %s/%s ===", cnt, total)
            builder.build(target=target, disttype=dist)
            cnt += 1
    
    logging.info("\n=== Writing Qt compatibility shim ===")
    write_qt_shim(PATH_ROOT)
    logging.info("Done.")


def ui(args):
    targets = [args.target] if args.target != "all" else Config()["targets"]

    builder = UIBuilder(root=PATH_ROOT)

    cnt = 1
    total = len(targets)
    for target in targets:
        logging.info("\n=== Build task %s/%s ===\n", cnt, total)
        builder.build(target=target)
        cnt += 1
    
    logging.info("\n=== Writing Qt compatibility shim ===")
    write_qt_shim(PATH_ROOT)
    logging.info("Done.")


def manifest(args):
    version = Git().parse_version(vstring=args.version)
    addon_properties = Config()

    dist_type = args.dist

    if args.dist == "all":
        print("'all' is not supported as a dist_type value when building the manifest.")
        return False

    ManifestUtils.generate_and_write_manifest(
        addon_properties=addon_properties,
        version=version,
        dist_type=dist_type,
        target_dir=PATH_ROOT / "src" / addon_properties["module_name"],
    )


# TODO: Deal with all this repetition once we merge this into develop


def create_dist(args):
    builder = AddonBuilder(version=args.version)
    builder.create_dist()


def build_dist(args):
    targets = [args.target] if args.target != "all" else Config()["targets"]
    dists = [args.dist] if args.dist != "all" else DIST_TYPES

    builder = AddonBuilder(version=args.version)

    cnt = 1
    total = len(targets) * len(dists)
    for target in targets:
        for dist in dists:
            logging.info("\n=== Build task %s/%s ===", cnt, total)
            builder.build_dist(target=target, disttype=dist)
            cnt += 1

    logging.info("\n=== Writing Qt compatibility shim ===")
    write_qt_shim(PATH_ROOT)
    logging.info("Done.")

def package_dist(args):
    targets = [args.target] if args.target != "all" else Config()["targets"]
    dists = [args.dist] if args.dist != "all" else DIST_TYPES

    builder = AddonBuilder(version=args.version)

    cnt = 1
    total = len(targets) * len(dists)
    for target in targets:
        for dist in dists:
            logging.info("\n=== Build task %s/%s ===", cnt, total)
            builder.package_dist(target=target, disttype=dist)
            cnt += 1


def clean(args):
    return clean_repo()


# Argument parsing
##############################################################################


def construct_parser():
    parser = argparse.ArgumentParser()
    if not PY2:
        parser.set_defaults(func=lambda x: parser.print_usage())
    subparsers = parser.add_subparsers()

    parser.add_argument(
        "-v",
        "--verbose",
        help="Enable verbose output",
        required=False,
        action="store_true",
    )

    target_parent = argparse.ArgumentParser(add_help=False)
    target_parent.add_argument(
        "-t",
        "--target",
        help="Anki release type to build for. Use 'all' (deprecated alias: 'anki21') to target both Qt5 and Qt6.",
        type=str,
        default="all",
        choices=["qt6", "qt5", "all", "anki21"],
    )

    dist_parent = argparse.ArgumentParser(add_help=False)
    dist_parent.add_argument(
        "-d",
        "--dist",
        help="Distribution channel to build for",
        type=str,
        default="local",
        choices=["local", "ankiweb", "all"],
    )

    build_parent = argparse.ArgumentParser(add_help=False)
    build_parent.add_argument(
        "version",
        nargs="?",
        help="Version to (pre-)build as a git reference "
        "(e.g. 'v1.2.0' or 'd338f6405'). "
        "Special keywords: 'dev' - working directory, "
        "'current' – latest commit, 'release' – latest tag. "
        "Leave empty to build latest tag.",
    )

    build_group = subparsers.add_parser(
        "build",
        parents=[build_parent, target_parent, dist_parent],
        help="Build and package add-on for distribution",
    )
    build_group.set_defaults(func=build)

    ui_group = subparsers.add_parser(
        "ui", parents=[target_parent], help="Compile add-on user interface files"
    )
    ui_group.set_defaults(func=ui)

    manifest_group = subparsers.add_parser(
        "manifest",
        parents=[build_parent, dist_parent],
        help="Generate manifest file from add-on properties in addon.json",
    )
    manifest_group.set_defaults(func=manifest)

    clean_group = subparsers.add_parser("clean", help="Clean leftover build files")
    clean_group.set_defaults(func=clean)

    create_dist_group = subparsers.add_parser(
        "create_dist",
        parents=[build_parent, target_parent, dist_parent],
        help="Prepare source tree distribution for building under build/dist. "
        "This is intended to be used in build scripts and should be run before "
        "`build_dist` and `package_dist`.",
    )
    create_dist_group.set_defaults(func=create_dist)

    build_dist_group = subparsers.add_parser(
        "build_dist",
        parents=[build_parent, target_parent, dist_parent],
        help="Build add-on files from prepared source tree under build/dist. "
        "This step performs all source code post-processing handled by "
        "aab itself (e.g. building the Qt UI and writing the add-on manifest). "
        "As with `create_dist` and `package_dist`, this command is meant to be "
        "used in build scripts where it can provide an avenue for performing "
        "additional processing ahead of packaging the add-on.",
    )
    build_dist_group.set_defaults(func=build_dist)

    package_dist_group = subparsers.add_parser(
        "package_dist",
        parents=[build_parent, target_parent, dist_parent],
        help="Package pre-built distribution of add-on files under build/dist into "
        "a distributable .ankiaddon package. This is inteded to be used in "
        "build scripts and called after both `create_dist` and `build_dist` "
        "have been run.",
    )
    package_dist_group.set_defaults(func=package_dist)

    return parser


# Main
##############################################################################


def main():
    print(COPYRIGHT_MSG)

    # Argument parsing

    parser = construct_parser()
    args = parser.parse_args()

    # Checks
    if not validate_cwd():
        sys.exit(1)

    # Logging

    if args.verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(stream=sys.stdout, level=level, format="%(message)s")

    # Argument aliases

    if hasattr(args, "target") and args.target == "anki21":
        print(
            "WARNING: 'anki21' is deprecated as a target type. Please use 'all' instead "
            "if targeting both qt6 and qt5 Anki builds."
        )
        args.target = "all"

    # Run
    args.func(args)


if __name__ == "__main__":
    main()
