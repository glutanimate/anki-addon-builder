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


from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import sys
import logging
import argparse

from . import PATH_ROOT, COPYRIGHT_MSG, DIST_TYPES
from .config import Config, PATH_CONFIG
from .builder import AddonBuilder, clean_repo
from .ui import UIBuilder
from .utils import PY2K


# Checks
##############################################################################

def validate_cwd():
    required = (PATH_ROOT / "src", PATH_CONFIG)
    for path in required:
        if not path.exists():
            print("Error: {dir} not found. Please run this script from "
                  "the project root.".format(dir=path.name))
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


def ui(args):
    targets = [args.target] if args.target != "all" else Config()["targets"]

    builder = UIBuilder(root=PATH_ROOT)

    cnt = 1
    total = len(targets)
    for target in targets:
        logging.info("\n=== Build task %s/%s ===\n", cnt, total)
        builder.build(target=target)
        cnt += 1


def clean(args):
    return clean_repo()


# Argument parsing
##############################################################################

def construct_parser():
    parser = argparse.ArgumentParser()
    if not PY2K:
        parser.set_defaults(func=lambda x: parser.print_usage())
    subparsers = parser.add_subparsers()

    parser.add_argument("-v", "--verbose",
                        help="Enable verbose output",
                        required=False, action="store_true")

    target_parent = argparse.ArgumentParser(add_help=False)
    target_parent.add_argument("-t", "--target",
                               help="Anki version to build for",
                               type=str, default="anki21",
                               choices=["anki21", "anki20", "all"])

    dist_parent = argparse.ArgumentParser(add_help=False)
    dist_parent.add_argument("-d", "--dist",
                             help="Distribution channel to build for",
                             type=str, default="local",
                             choices=["local", "ankiweb", "all"])

    build_group = subparsers.add_parser(
        "build", parents=[target_parent, dist_parent],
        help="Build and package add-on for distribution"
    )
    build_group.add_argument(
        "version", nargs="?", help="Version to build as a git reference "
        "(e.g. 'v1.2.0' or 'd338f6405'). "
        "Special keywords: 'current' – latest commit, 'release' – latest tag. "
        "Leave empty to build latest tag.")
    build_group.set_defaults(func=build)

    ui_group = subparsers.add_parser(
        "ui", parents=[target_parent],
        help="Compile add-on user interface files"
    )
    ui_group.set_defaults(func=ui)

    clean_group = subparsers.add_parser(
        "clean", help="Clean leftover build files")
    clean_group.set_defaults(func=clean)

    return parser


# Main
##############################################################################

def main():
    print(COPYRIGHT_MSG)

    # Checks
    if not validate_cwd():
        sys.exit(1)

    # Argument parsing

    parser = construct_parser()
    args = parser.parse_args()

    # Logging

    if args.verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(stream=sys.stdout, level=level, format="%(message)s")

    # Run
    args.func(args)

if __name__ == "__main__":
    main()
