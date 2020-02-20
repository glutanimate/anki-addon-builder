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
Basic Git interface
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import os.path

from .utils import call_shell, quote


class Git(object):
    def parse_version(self, vstring=None):
        if vstring and vstring not in ("release", "current"):
            return vstring

        logging.info("Getting Git version info...")

        cmd = "git describe HEAD --tags"
        if vstring is None or vstring == "release":
            cmd += " --abbrev=0"

        version = call_shell(cmd, error_exit=False)

        if version is False:
            # Perhaps no tag has been set yet. Try to grab commit ID before
            # giving up and exiting
            version = call_shell("git rev-parse --short HEAD")

        return version

    def archive(self, version, special, outdir):
        logging.info("Exporting Git archive...")
        if not outdir or not (version or special):
            return False
        if special == "dev":
            # https://stackoverflow.com/a/12010656
            cmd = (
                "stash=`git stash create`; git archive --format tar $stash |"
                " tar -x -C {outdir}/".format(outdir=quote(outdir))
            )
        else:
            cmd = "git archive --format tar -- {vers} | tar -x -C {outdir}/".format(
                vers=quote(version), outdir=quote(outdir)
            )
        return call_shell(cmd)

    def modtime(self, version, special):
        if special == "dev":
            # Get timestamps of uncommitted changes and return the most recent.
            cmd = "git status -z"  # -z formats the file names in a parsing friendly way
            # get all files from git, separate the mode and get the mtime for every file if it exists;
            # git uses '\0' line endings, thus the last split field is empty;
            # if a file was moved or copied git uses two lines ('XY to\0from') and we have to discard the second
            modtimes = []
            it = iter(call_shell(cmd).split("\0")[0:-1])
            for x in it:
                mode, file = x[0:2], x[3:]
                if "R" in mode or "C" in mode:
                    next(it)  # skip 'from'
                modtimes.append(file)
            modtimes[:] = [os.path.getmtime(x) for x in modtimes if os.path.exists(x)]
            return int(max(modtimes))
        else:
            return int(
                call_shell(
                    "git log -1 --no-patch --format=%ct {}".format(quote(version))
                )
            )
