import math

from koswat.dike.layers import KoswatLayerProtocol
from koswat.dike.layers.coating_layer import KoswatCoatingLayer
from koswat.dike.material.koswat_material_type import KoswatMaterialType


class TestKoswatCoatingLayer:
    def test_initialize(self):
        _layer = KoswatCoatingLayer()
        assert isinstance(_layer, KoswatCoatingLayer)
        assert isinstance(_layer, KoswatLayerProtocol)
        assert not _layer.material_type
        assert not _layer.outer_geometry
        assert math.isnan(_layer.depth)

    def test_as_dict(self):
        _layer = KoswatCoatingLayer()
        _layer.material_type = KoswatMaterialType.CLAY
        _layer.depth = 4.2
        _dict = _layer.as_data_dict()

        assert isinstance(_dict, dict)
        assert _dict["material"] == KoswatMaterialType.CLAY
        assert _dict["depth"] == 4.2
