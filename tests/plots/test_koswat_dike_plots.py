import pytest

from koswat.dike.material.koswat_material_type import KoswatMaterialType
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.dike.profile.koswat_profile_builder import KoswatProfileBuilder
from koswat.plots.dike.koswat_profile_plot import KoswatProfilePlot
from koswat.plots.geometries.highlight_geometry_plot import HighlightGeometryPlot
from koswat.plots.koswat_figure_context_handler import KoswatFigureContextHandler
from tests import get_test_results_dir
from tests.library_test_cases import InputProfileCases, LayersCases


class TestKoswatDikePlots:
    def test_plot_koswat_profile_plot_simple_dike_with_layers(
        self, request: pytest.FixtureRequest
    ):
        # 1. Define test data.
        _test_dir = get_test_results_dir(request)
        _test_file = _test_dir / "base_profile_layers.png"
        _base_koswat_profile = KoswatProfileBuilder.with_data(
            dict(
                input_profile_data=InputProfileCases.default,
                layers_data=LayersCases.with_clay_and_grass.layers_dict,
                profile_type=KoswatProfileBase,
            )
        ).build()
        assert isinstance(_base_koswat_profile, KoswatProfileBase)
        assert not _test_file.exists()

        # 2. Run test
        with KoswatFigureContextHandler(_test_file, 180) as _koswat_figure:
            _profile_plot = KoswatProfilePlot()
            _profile_plot.subplot = _koswat_figure.add_subplot()
            _profile_plot.koswat_object = _base_koswat_profile
            _profile_plot.plot(unique_color="#fc0303")

        # 3. Verify results.
        assert _test_file.exists()

    def test_plot_highlight_geometry_plot_simple_dike_with_layers(
        self, request: pytest.FixtureRequest
    ):
        # 1. Define test data.
        _test_dir = get_test_results_dir(request)
        _base_koswat_profile = KoswatProfileBuilder.with_data(
            dict(
                input_profile_data=InputProfileCases.default,
                layers_data=LayersCases.with_clay_and_grass.layers_dict,
                profile_type=KoswatProfileBase,
            )
        ).build()
        assert isinstance(_base_koswat_profile, KoswatProfileBase)
        assert not any(_test_dir.glob("*.png"))

        # 2. Run test
        for layer in _base_koswat_profile.layers_wrapper.layers:
            _test_file = _test_dir / "base_profile_{}.png".format(
                layer.material_type.name.lower()
            )
            with KoswatFigureContextHandler(_test_file, 180) as _koswat_figure:
                _subplot = _koswat_figure.add_subplot()
                # Profile plot.
                _profile_plot = KoswatProfilePlot()
                _profile_plot.koswat_object = _base_koswat_profile
                _profile_plot.subplot = _subplot
                _profile_plot.plot(unique_color="#fc0303")

                # Highlight plot
                _highlight_plot = HighlightGeometryPlot()
                _highlight_plot.koswat_object = layer.material_geometry
                if layer.material_type == KoswatMaterialType.SAND:
                    _highlight_plot.koswat_object = layer.outer_geometry
                _highlight_plot.subplot = _subplot
                _highlight_plot.plot()

        # 3. Verify results.
        assert _test_dir.exists()
        assert len(list(_test_dir.glob("*.png"))) == 3
