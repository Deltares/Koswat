from koswat.profiles.koswat_layers import KoswatLayer, KoswatLayers


class TestKoswatLayer:
    def test_initialize(self):
        _layer = KoswatLayer()
        assert isinstance(_layer, KoswatLayer)
        assert not _layer.material
        assert not _layer.geometry


class TestKoswatLayers:
    def test_initialize(self):
        _layers = KoswatLayers()
        assert isinstance(_layers, KoswatLayers)
        assert not _layers.base_layer
        assert not _layers.coating_layers
