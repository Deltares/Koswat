from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
import logging

from koswat.dike.surroundings.surroundings_infrastructure import SurroundingsInfrastructure
from koswat.dike.surroundings.surroundings_obstacle import SurroundingsObstacle

@dataclass
class SurroundingsEnumType:
    surrounding_type: type[SurroundingsInfrastructure | SurroundingsObstacle]
    dutch_text: str = ""


class SurroundingsEnum(SurroundingsEnumType, Enum):
    # Simple format
    BUILDINGS = SurroundingsObstacle, "bebouwing"
    RAILWAYS = SurroundingsObstacle, "spoorwegen"
    WATERS = SurroundingsObstacle, "water"
    CUSTOM = SurroundingsObstacle, "custom"

    # Extended format
    ROADS_CLASS_2_POLDERSIDE = SurroundingsInfrastructure, "wegen_binnendijks_klasse2"
    ROADS_CLASS_7_POLDERSIDE = SurroundingsInfrastructure, "wegen_binnendijks_klasse7"
    ROADS_CLASS_24_POLDERSIDE = SurroundingsInfrastructure, "wegen_binnendijks_klasse24"
    ROADS_CLASS_47_POLDERSIDE = SurroundingsInfrastructure, "wegen_binnendijks_klasse47"
    ROADS_CLASS_UNKNOWN_POLDERSIDE = SurroundingsInfrastructure, "wegen_binnendijks_klasseonbekend"
    ROADS_CLASS_2_WATERSIDE = SurroundingsInfrastructure, "wegen_buitendijks_klasse2"
    ROADS_CLASS_7_WATERSIDE = SurroundingsInfrastructure, "wegen_buitendijks_klasse7"
    ROADS_CLASS_24_WATERSIDE = SurroundingsInfrastructure, "wegen_buitendijks_klasse24"
    ROADS_CLASS_47_WATERSIDE = SurroundingsInfrastructure, "wegen_buitendijks_klasse47"
    ROADS_CLASS_UNKNOWN_WATERSIDE = SurroundingsInfrastructure, "wegen_buitendijks_klasseonbekend"

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
        _translation = next((item for item in cls if item.dutch_text == normalized), cls.CUSTOM)
        logging.info(f"Surrounding type: {surrounding_type_str} is mapped to {_translation.name.lower()}")
        return _translation

