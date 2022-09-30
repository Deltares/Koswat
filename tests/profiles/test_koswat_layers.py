import math

from koswat.profiles.koswat_layers import KoswatLayer, KoswatLayers
from koswat.profiles.koswat_material import KoswatMaterial


class TestKoswatLayer:
    def test_initialize(self):
        _layer = KoswatLayer()
        assert isinstance(_layer, KoswatLayer)
        assert not _layer.material
        assert math.isnan(_layer.depth)

    def test_initialize_from_dict(self):
        # 1. Define test data.
        _data = dict(material="zand", depth=4.2)

        # 2. Run test.
        _layer = KoswatLayer.from_dict(_data)

        # 3. Verify final expectations.
        assert isinstance(_layer, KoswatLayer)
        assert isinstance(_layer.material, KoswatMaterial)
        assert not math.isnan(_layer.depth)


class TestKoswatLayers:
    def test_initialize(self):
        _layers = KoswatLayers()
        assert isinstance(_layers, KoswatLayers)
        assert not _layers.base_layer
        assert not _layers.coating_layers

    def test_initialize_from_dict(self):
        # 1. Define test data
        _data = dict(
            base_layer=dict(material="zand"),
            coating_layers=[
                dict(material="klei", depth=2.4),
                dict(material="gras", depth=4.2),
            ],
        )

        # 2. Run test.
        _layers = KoswatLayers.from_dict(_data)

        # 3. Verify expectations
        assert isinstance(_layers, KoswatLayers)
        # Base layer  (for now) has no depth
        assert isinstance(_layers.base_layer, KoswatLayer)
        assert _layers.base_layer.material.name == "zand"
        assert math.isnan(_layers.base_layer.depth)

        # Verify the coating layers
        assert isinstance(_layers.coating_layers, list)
        for c_layer in _layers.coating_layers:
            assert isinstance(c_layer, KoswatLayer)

        assert len(_layers.coating_layers) == 2
        assert _layers.coating_layers[0].material.name == "klei"
        assert _layers.coating_layers[0].depth == 2.4
        assert _layers.coating_layers[1].material.name == "gras"
        assert _layers.coating_layers[1].depth == 4.2

    def test_initialize_from_dict_without_coating_layers(self):
        # 1. Define test data
        _data = dict(
            base_layer=dict(material="zand"),
        )

        # 2. Run test.
        _layers = KoswatLayers.from_dict(_data)

        # 3. Verify expectations
        assert isinstance(_layers, KoswatLayers)
        # Base layer  (for now) has no depth
        assert isinstance(_layers.base_layer, KoswatLayer)
        assert _layers.base_layer.material.name == "zand"
        assert math.isnan(_layers.base_layer.depth)
