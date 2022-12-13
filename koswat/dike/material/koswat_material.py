import enum


class KoswatMaterialType(enum.Enum):
    SAND = 0
    CLAY = 1
    GRASS = 2


class KoswatMaterialFactory:
    @staticmethod
    def get_material(material_name: str) -> KoswatMaterialType:
        _material = KoswatMaterialType.__dict__.get(material_name.upper(), None)
        if not _material:
            raise ValueError(f"No information available for material {material_name}")
        return _material
