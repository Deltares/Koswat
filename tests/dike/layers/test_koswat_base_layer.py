from koswat.dike.layers import KoswatLayerProtocol
from koswat.dike.layers.base_layer import KoswatBaseLayer
from koswat.dike.material.koswat_material import KoswatMaterial


class TestKoswatBaseLayer:
    def test_initialize(self):
        _layer = KoswatBaseLayer()
        assert isinstance(_layer, KoswatBaseLayer)
        assert isinstance(_layer, KoswatLayerProtocol)
        assert not _layer.material
        assert not _layer.outer_geometry

    def test_as_dict(self):
        _layer = KoswatBaseLayer()
        _layer.material = KoswatMaterial()

        _dict = _layer.as_data_dict()

        assert isinstance(_dict, dict)
        assert _dict["material"] == ""
