#!/usr/bin/env python
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


import argparse
import logging
import sys
from argparse import ArgumentParser, Namespace

from . import COPYRIGHT_MSG, DIST_TYPES, PATH_ROOT
from .builder import AddonBuilder, clean_repo
from .config import PATH_CONFIG
from .ui import UIBuilder

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


def build(args: Namespace, continued=False):
    dists = [args.dist] if args.dist != "all" else DIST_TYPES
    special = None
    if args.release:
        special = "release"
    elif args.current_commit:
        special = "current"
    elif args.working_directory:
        special = "dev"

    builder = AddonBuilder(version=args.version, special=special)
    build_method = builder.build if not continued else builder.build_and_package

    cnt = 1
    total = len(dists)
    for dist in dists:
        logging.info("\n=== Build task %s/%s ===", cnt, total)
        build_method(disttype=dist)
        cnt += 1

def ui(args: Namespace):
    builder = UIBuilder(root=PATH_ROOT)

    logging.info("\n=== Build task 1/1 ===\n")
    builder.build()

def prebuild(args):
    builder = AddonBuilder(version=args.version)
    builder.prebuild()

def continue_build(args):
    return build(args, continued=True)


def clean(args):
    return clean_repo()


# Argument parsing
##############################################################################


class DeprecationAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        option_string = ", ".join(f"'{i}'" for i in self.option_strings)
        print(f"Warning: Arguments {option_string} are deprecated")


def construct_parser() -> ArgumentParser:
    parser = argparse.ArgumentParser()
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
        "-t", "--target", help="DEPRECATED: has no effect", action=DeprecationAction
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
        "Special instructions can be given with the mutually "
        "exclusive '-c', '-w' or '-r' options. "
        "Leave empty to build latest tag ('-r').",
    )

    build_group = subparsers.add_parser(
        "build",
        parents=[build_parent, target_parent, dist_parent],
        help="Build and package add-on for distribution",
    )
    build_group.set_defaults(func=build)

    build_group_options = build_group.add_mutually_exclusive_group()
    build_group_options.add_argument(
        "-c",
        "--current-commit",
        action="store_true",
        help="Build the currently checked out commit.",
    )
    build_group_options.add_argument(
        "-w",
        "--working-directory",
        action="store_true",
        help="Build the current working directory without "
        "the need of a commit. Useful for development.",
    )
    build_group_options.add_argument(
        "-r", "--release", action="store_true", help="Build the latest tag."
    )

    prebuild_group = subparsers.add_parser(
        "prebuild",
        parents=[build_parent, target_parent, dist_parent],
        help="Prepare source tree for building. Useful for scripting aab.",
    )
    prebuild_group.set_defaults(func=prebuild)
    
    continue_build_group = subparsers.add_parser(
        "continue_build",
        parents=[build_parent, target_parent, dist_parent],
        help="Build and package add-on for distribution, given a pre-built source tree."
        " Useful for scripting aab.",
    )
    continue_build_group.set_defaults(func=continue_build)

    ui_group = subparsers.add_parser(
        "ui", parents=[target_parent], help="Compile add-on user interface files"
    )
    ui_group.set_defaults(func=ui)

    clean_group = subparsers.add_parser("clean", help="Clean leftover build files")
    clean_group.set_defaults(func=clean)

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

    # Run
    args.func(args)


if __name__ == "__main__":
    main()
