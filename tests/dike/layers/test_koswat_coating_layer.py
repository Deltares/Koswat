import math

from koswat.dike.layers import KoswatCoatingLayer, KoswatLayerProtocol
from koswat.dike.material.koswat_material import KoswatMaterial


class TestKoswatCoatingLayer:
    def test_initialize(self):
        _layer = KoswatCoatingLayer()
        assert isinstance(_layer, KoswatCoatingLayer)
        assert isinstance(_layer, KoswatLayerProtocol)
        assert not _layer.material
        assert not _layer.geometry
        assert math.isnan(_layer.depth)

    def test_as_dict(self):
        _layer = KoswatCoatingLayer()
        _layer.material = KoswatMaterial()
        _layer.depth = 4.2
        _dict = _layer.as_data_dict()

        assert isinstance(_dict, dict)
        assert _dict["material"] == ""
        assert _dict["depth"] == 4.2
