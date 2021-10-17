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

"""
Project config parser
"""

import json
import logging
from pathlib import Path

from pydantic import ValidationError

from .model import AddonProperties


class AddonPropertiesReader:
    @staticmethod
    def read(properties_path: Path) -> AddonProperties:
        try:
            with properties_path.open("r", encoding="utf-8") as properties_file:
                properties_dict = json.loads(properties_file.read())
                properties = AddonProperties(**properties_dict)
        except (IOError, OSError):
            logging.error(
                f"Error: Could not read '{properties_path}'. Traceback follows below:\n"
            )
            raise
        except (ValueError, ValidationError):
            logging.error(
                f"Error: Could not parse '{properties_path}'. Traceback follows"
                " below:\n"
            )
            raise
        return properties
