"""
                GNU GENERAL PUBLIC LICENSE
                  Version 3, 29 June 2007

KOSWAT, from the dutch combination of words `Kosts-Wat` (what are the costs)
Copyright (C) 2025 Stichting Deltares

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

from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import Enum

from koswat.dike.surroundings.road_class import RoadsClass
from koswat.dike.surroundings.road_classes import (
    RoadClass2,
    RoadClass7,
    RoadClass24,
    RoadClass47,
    RoadClassProtocol,
    RoadClassUnknown,
)
from koswat.dike.surroundings.surroundings_infrastructure import (
    SurroundingsInfrastructure,
)
from koswat.dike.surroundings.surroundings_obstacle import SurroundingsObstacle


@dataclass
class SurroundingsEnumType:
    surrounding_type: type[SurroundingsInfrastructure | SurroundingsObstacle]
    surroundings_class: type[RoadClassProtocol] | None


class SurroundingsEnum(SurroundingsEnumType, Enum):
    # Simple format
    OBSTACLE = SurroundingsObstacle, None

    # Extended format
    ROADS_CLASS_2_POLDERSIDE = SurroundingsInfrastructure, RoadClass2
    ROADS_CLASS_7_POLDERSIDE = SurroundingsInfrastructure, RoadClass7
    ROADS_CLASS_24_POLDERSIDE = SurroundingsInfrastructure, RoadClass24
    ROADS_CLASS_47_POLDERSIDE = SurroundingsInfrastructure, RoadClass47
    ROADS_CLASS_UNKNOWN_POLDERSIDE = (
        SurroundingsInfrastructure,
        RoadClassUnknown,
    )
    ROADS_CLASS_2_WATERSIDE = SurroundingsInfrastructure, RoadClass2
    ROADS_CLASS_7_WATERSIDE = SurroundingsInfrastructure, RoadClass7
    ROADS_CLASS_24_WATERSIDE = SurroundingsInfrastructure, RoadClass24
    ROADS_CLASS_47_WATERSIDE = SurroundingsInfrastructure, RoadClass47
    ROADS_CLASS_UNKNOWN_WATERSIDE = (
        SurroundingsInfrastructure,
        RoadClassUnknown,
    )

    @classmethod
    def translate(cls, surrounding_type_str: str) -> SurroundingsEnum:
        """
        Translates a string representation of a surrounding type into a SurroundingsEnum.
        When not found, it defaults to CUSTOM.

        Args:
            surrounding_type_str (str): The string representation of the surrounding type.

        Returns:
            SurroundingsEnum: The corresponding SurroundingsEnum member.
        """
        normalized = surrounding_type_str.lower().strip()
        _translation = next(
            (item for item in cls if item.dutch_text == normalized), cls.OBSTACLE
        )
        logging.info(
            f"Surrounding type: {surrounding_type_str} is mapped to {_translation.name.lower()}"
        )
        return _translation

    def __hash__(self):
        return hash(self.name)

    @classmethod
    def get_infra_types(
        cls, road_class: RoadsClass
    ) -> tuple[SurroundingsEnum, SurroundingsEnum]:
        mapping = {
            RoadsClass.CLASS_2: (
                cls.ROADS_CLASS_2_POLDERSIDE,
                cls.ROADS_CLASS_2_WATERSIDE,
            ),
            RoadsClass.CLASS_7: (
                cls.ROADS_CLASS_7_POLDERSIDE,
                cls.ROADS_CLASS_7_WATERSIDE,
            ),
            RoadsClass.CLASS_24: (
                cls.ROADS_CLASS_24_POLDERSIDE,
                cls.ROADS_CLASS_24_WATERSIDE,
            ),
            RoadsClass.CLASS_47: (
                cls.ROADS_CLASS_47_POLDERSIDE,
                cls.ROADS_CLASS_47_WATERSIDE,
            ),
            RoadsClass.CLASS_UNKNOWN: (
                cls.ROADS_CLASS_UNKNOWN_POLDERSIDE,
                cls.ROADS_CLASS_UNKNOWN_WATERSIDE,
            ),
        }
        return tuple(mapping.get(road_class, (None, None)))
