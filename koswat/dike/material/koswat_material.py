import math


class KoswatMaterial:
    name: str

    def __init__(self) -> None:
        self.name = ""


class KoswatMaterialFactory:
    @staticmethod
    def get_material(material_name: str) -> KoswatMaterial:
        def _build_material(name: str) -> KoswatMaterial:
            _material = KoswatMaterial()
            _material.name = name
            return _material

        _available_materials = dict(
            zand=_build_material("zand"),
            klei=_build_material("klei"),
            gras=_build_material("gras"),
        )
        _material = _available_materials.get(material_name.lower().strip(), None)
        if not _material:
            raise ValueError(f"No information available for material {material_name}")
        return _material
