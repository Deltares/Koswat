from koswat.dike.layers.base_layer import KoswatBaseLayer
from koswat.dike.layers.coating_layer import KoswatCoatingLayer
from koswat.dike.layers.layers_wrapper import KoswatLayersWrapper
from koswat.dike.material.koswat_material_type import KoswatMaterialType


class TestKoswatLayersWrapper:
    def test_initialize(self):
        _layers = KoswatLayersWrapper()
        assert isinstance(_layers, KoswatLayersWrapper)
        assert not _layers.base_layer
        assert not _layers.coating_layers

    def test_as_dict(self):
        _layers = KoswatLayersWrapper()
        _material_a = KoswatMaterialType.CLAY
        _material_b = KoswatMaterialType.GRASS
        _layers.base_layer = KoswatBaseLayer()
        _layers.base_layer.material_type = _material_a
        _layers.coating_layers = [KoswatCoatingLayer()]
        _layers.coating_layers[0].depth = 2.4
        _layers.coating_layers[0].material_type = _material_b

        # 2. Run test
        _dict = _layers.as_data_dict()

        # 3. Verify final expectations
        assert _dict == dict(
            base_layer=dict(material=KoswatMaterialType.CLAY, geometry=[]),
            coating_layers=[
                dict(
                    material=KoswatMaterialType.GRASS,
                    depth=2.4,
                    geometry=[],
                )
            ],
        )
