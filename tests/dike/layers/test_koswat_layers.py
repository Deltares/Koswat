from koswat.dike.layers import KoswatBaseLayer, KoswatCoatingLayer, KoswatLayers
from koswat.dike.material.koswat_material import KoswatMaterial


class TestKoswatLayers:
    def test_initialize(self):
        _layers = KoswatLayers()
        assert isinstance(_layers, KoswatLayers)
        assert not _layers.base_layer
        assert not _layers.coating_layers

    def test_as_dict(self):
        _layers = KoswatLayers()
        _material_a = KoswatMaterial()
        _material_a.name = "a material"
        _material_b = KoswatMaterial()
        _material_b.name = "b material"
        _layers.base_layer = KoswatBaseLayer()
        _layers.base_layer.material = _material_a
        _layers.coating_layers = [KoswatCoatingLayer()]
        _layers.coating_layers[0].depth = 2.4
        _layers.coating_layers[0].material = _material_b

        # 2. Run test
        _dict = _layers.as_data_dict()

        # 3. Verify final expectations
        assert _dict == dict(
            base_layer=dict(material="a material"),
            coating_layers=[dict(material="b material", depth=2.4)],
        )
