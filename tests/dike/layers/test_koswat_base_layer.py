from koswat.dike.layers import KoswatLayerProtocol
from koswat.dike.layers.base_layer import KoswatBaseLayer
from koswat.dike.material.koswat_material_type import KoswatMaterialType


class TestKoswatBaseLayer:
    def test_initialize(self):
        _layer = KoswatBaseLayer()
        assert isinstance(_layer, KoswatBaseLayer)
        assert isinstance(_layer, KoswatLayerProtocol)
        assert not _layer.material_type
        assert not _layer.outer_geometry

    def test_as_dict(self):
        _layer = KoswatBaseLayer()
        _layer.material_type = KoswatMaterialType.SAND

        _dict = _layer.as_data_dict()

        assert isinstance(_dict, dict)
        assert _dict["material"] == KoswatMaterialType.SAND
