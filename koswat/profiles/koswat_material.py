import math


class KoswatMaterial:
    name: str
    cost: float

    def __init__(self) -> None:
        self.name = ""
        self.cost = math.nan


class KoswatMaterialFactory:
    @staticmethod
    def get_material(material_name: str) -> KoswatMaterial:
        def _build_material(name: str, cost: float) -> KoswatMaterial:
            _material = KoswatMaterial()
            _material.name = name
            _material.cost = cost
            return _material

        _available_materials = dict(
            zand=_build_material("zand", 2.4),
            klei=_build_material("klei", 24.42),
            gras=_build_material("gras", 4.2),
        )
        _material = _available_materials.get(material_name.lower().strip(), None)
        if not _material:
            raise ValueError(f"No information available for material {material_name}")
        return _material
