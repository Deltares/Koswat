from enum import Enum
from dataclasses import dataclass

from koswat.dike.surroundings.koswat_surroundings_protocol import KoswatSurroundingsProtocol
from koswat.dike.surroundings.surroundings_infrastructure import SurroundingsInfrastructure
from koswat.dike.surroundings.surroundings_obstacle import SurroundingsObstacle

@dataclass
class SurroundingEnumType:
    surrounding_type: type[KoswatSurroundingsProtocol]

class SurroundingsEnum(SurroundingEnumType, Enum):
    BUILDINGS_POLDERSIDE = SurroundingsObstacle
    RAILWAYS_POLDERSIDE = SurroundingsInfrastructure
    WATERS_POLDERSIDE = SurroundingsInfrastructure
    ROADS_CLASS_2_POLDERSIDE = SurroundingsInfrastructure
    ROADS_CLASS_7_POLDERSIDE = SurroundingsInfrastructure
    ROADS_CLASS_24_POLDERSIDE = SurroundingsInfrastructure
    ROADS_CLASS_47_POLDERSIDE = SurroundingsInfrastructure
    ROADS_CLASS_UNKNOWN_POLDERSIDE = SurroundingsInfrastructure

    BUILDINGS_WATERSIDE = SurroundingsObstacle
    RAILWAYS_WATERSIDE = SurroundingsInfrastructure    
    WATERS_WATERSIDE = SurroundingsInfrastructure
    ROADS_CLASS_2_WATERSIDE = SurroundingsInfrastructure
    ROADS_CLASS_7_WATERSIDE = SurroundingsInfrastructure
    ROADS_CLASS_24_WATERSIDE = SurroundingsInfrastructure
    ROADS_CLASS_47_WATERSIDE = SurroundingsInfrastructure
    ROADS_CLASS_UNKNOWN_WATERSIDE = SurroundingsInfrastructure

    @classmethod
    def translate(cls, surrounding_type_str: str) -> "SurroundingsEnum":
        normalized = surrounding_type_str.lower().strip()
        translations = {
            "bebouwing_binnendijks": cls.BUILDINGS_POLDERSIDE,
            "bebouwing_buitendijks": cls.BUILDINGS_WATERSIDE,
            "spoor_binnendijks": cls.RAILWAYS_POLDERSIDE,
            "spoor_buitendijks": cls.RAILWAYS_WATERSIDE,
            "water_binnendijks": cls.WATERS_POLDERSIDE,
            "water_buitendijks": cls.WATERS_WATERSIDE,
            "wegen_binnendijks_klasse2": cls.ROADS_CLASS_2_POLDERSIDE,
            "wegen_binnendijks_klasse7": cls.ROADS_CLASS_7_POLDERSIDE,
            "wegen_binnendijks_klasse24": cls.ROADS_CLASS_24_POLDERSIDE,
            "wegen_binnendijks_klasse47": cls.ROADS_CLASS_47_POLDERSIDE,
            "wegen_binnendijks_klasseonbekend": cls.ROADS_CLASS_UNKNOWN_POLDERSIDE,
            "wegen_buitendijks_klasse2": cls.ROADS_CLASS_2_WATERSIDE,
            "wegen_buitendijks_klasse7": cls.ROADS_CLASS_7_WATERSIDE,
            "wegen_buitendijks_klasse24": cls.ROADS_CLASS_24_WATERSIDE,
            "wegen_buitendijks_klasse47": cls.ROADS_CLASS_47_WATERSIDE,
            "wegen_buitendijks_klasseonbekend": cls.ROADS_CLASS_UNKNOWN_WATERSIDE,
        }
        translation = translations.get(normalized, None)
        if not translation:
            error = f"No mapping found for {surrounding_type_str}"
            raise ValueError(error)
        return translation

