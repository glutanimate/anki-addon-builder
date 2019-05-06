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
Utility functions
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import sys
import subprocess
import logging

from . import PATH_ROOT

# Python 2 is needed to support Anki 2.0 development environments
PY2K = sys.version_info < (3, 0)
unicode = unicode if PY2K else str  # noqa:F821

def call_shell(command, echo=False, error_exit=True, **kwargs):
    try:
        out = subprocess.check_output(command, shell=True, **kwargs)
        decoded = out.decode("utf-8").strip()
        if echo:
            logging.info(decoded)
        return decoded
    except subprocess.CalledProcessError as e:
        logging.error("Error while running command: '{command}'".format(
                      command=command))
        logging.error(e.output.decode("utf-8"))
        if error_exit:
            sys.exit(1)
        return False


def purge(path, patterns, recursive=False):
    """Wrapper for GNU find that deletes files matching pattern

    Arguments:
        path {str} -- Path to look through
        patterns {list} -- List of patterns to delete

    Keyword Arguments:
        recursive {bool} -- Whether to search recursively (default: {False})
    """
    if not path or not patterns:
        return False
    pattern_string = " -o ".join("-name '{}'".format(p) for p in patterns)
    pattern_string = "\( {} \)".format(pattern_string)
    depth = "-maxdepth 1" if not recursive else ""
    cmd = 'find "{path}" {depth} {pattern_string} -delete'.format(
        path=path, depth=depth, pattern_string=pattern_string)
    return call_shell(cmd)


def copy_recursively(source, target):
    if not source or not target:
        return False
    return call_shell('cp -r "{source}" "{target}"'.format(
                      source=source, target=target))


def relpath(path):
    return path.relative_to(PATH_ROOT)
