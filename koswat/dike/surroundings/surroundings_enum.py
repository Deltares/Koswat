from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto

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
        normalized = surrounding_type_str.lower().strip()
        _translation = next((item for item in cls if item.dutch_text == normalized), None)
        if not _translation:
            error = f"No mapping found for {surrounding_type_str}"
            raise ValueError(error)
        return _translation

