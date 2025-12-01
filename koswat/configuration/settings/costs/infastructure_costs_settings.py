"""
                    GNU GENERAL PUBLIC LICENSE
                      Version 3, 29 June 2007

    KOSWAT, from the dutch combination of words `Kosts-Wat` (what are the costs)
    Copyright (C) 2024 Stichting Deltares

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import math
from dataclasses import dataclass

from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol


def _valid_float_prop(config_property: float) -> bool:
    return config_property is not None and not math.isnan(config_property)


@dataclass
class InfrastructureCostsSettings(KoswatConfigProtocol):
    removing_roads_klasse2: float = math.nan
    removing_roads_klasse24: float = math.nan
    removing_roads_klasse47: float = math.nan
    removing_roads_klasse7: float = math.nan
    removing_roads_unknown: float = math.nan
    adding_roads_klasse2: float = math.nan
    adding_roads_klasse24: float = math.nan
    adding_roads_klasse47: float = math.nan
    adding_roads_klasse7: float = math.nan
    adding_roads_unknown: float = math.nan

    def is_valid(self) -> bool:
        return all(_valid_float_prop(_prop) for _prop in self.__dict__.values())
