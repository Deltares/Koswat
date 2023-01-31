import pytest

from koswat.calculations.protocols.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.calculations.reinforcement_layers_wrapper import (
    ReinforcementBaseLayer,
    ReinforcementCoatingLayer,
    ReinforcementLayersWrapper,
)
from koswat.calculations.standard_reinforcement.soil.soil_reinforcement_profile import (
    SoilReinforcementProfile,
)
from koswat.calculations.standard_reinforcement.standard_reinforcement_profile import (
    StandardReinforcementProfile,
)
from koswat.configuration.settings.costs.dike_profile_costs_settings import (
    DikeProfileCostsSettings,
)
from koswat.configuration.settings.costs.koswat_costs import KoswatCostsSettings
from koswat.core.protocols.builder_protocol import BuilderProtocol
from koswat.cost_report.profile.volume_cost_parameters import (
    VolumeCostParameter,
    VolumeCostParameters,
)
from koswat.cost_report.profile.volume_cost_parameters_builder import (
    VolumeCostParametersBuilder,
)
from koswat.cost_report.profile.volume_cost_parameters_calculator import (
    VolumeCostParametersCalculator,
)
from koswat.dike.material.koswat_material_type import KoswatMaterialType


class TestVolumeCostParametersBuilder:
    def test_initialize(self):
        _builder = VolumeCostParametersBuilder()
        assert isinstance(_builder, VolumeCostParametersBuilder)
        assert isinstance(_builder, BuilderProtocol)
        assert _builder.reinforced_profile is None
        assert _builder.koswat_costs is None

    def test_no_reinforced_profile_raises(self):
        _expected_mssg = "No reinforced profile provided."
        with pytest.raises(ValueError) as exc_value:
            _builder = VolumeCostParametersBuilder()
            _builder.koswat_costs = None
            _builder.reinforced_profile = None
            _builder.build()

        assert str(exc_value.value) == _expected_mssg

    def test_no_koswat_costs_raises(self):
        _expected_mssg = "No koswat costs provided."
        with pytest.raises(ValueError) as exc_value:
            _builder = VolumeCostParametersBuilder()
            _builder.koswat_costs = None
            _builder.reinforced_profile = 42
            _builder.build()

        assert str(exc_value.value) == _expected_mssg

    def test__get_volume_cost_parameter(self):
        _builder = VolumeCostParametersBuilder()
        _vc_parameter = _builder._get_volume_cost_parameter(4.2, 2.4)
        assert isinstance(_vc_parameter, VolumeCostParameter)
        assert _vc_parameter.volume == 4.2
        assert _vc_parameter.cost == 2.4

    def test__get_volume_cost_calculator_no_reinforced_profile_returns_none(self):
        _builder = VolumeCostParametersBuilder()
        _builder.reinforced_profile = SoilReinforcementProfile()
        _builder.reinforced_profile.layers_wrapper = ReinforcementLayersWrapper()
        _calculator = _builder._get_volume_cost_calculator()
        assert _calculator is None

    def _get_mocked_layer(
        self, material_type: KoswatMaterialType, area: float, length: float
    ):
        class MockLayerProperties:
            def __init__(self) -> None:
                self.area = area
                self.length = length

        _mocked_layer = ReinforcementCoatingLayer()
        _mocked_layer.material_type = material_type
        _properties = MockLayerProperties()
        _mocked_layer.new_layer_geometry = _properties
        _mocked_layer.new_layer_surface = _properties
        _mocked_layer.removal_layer_geometry = _properties
        return _mocked_layer

    def _get_mocked_reinforcement(self) -> ReinforcementProfileProtocol:
        class MockedReinforcement(StandardReinforcementProfile):
            @property
            def new_ground_level_surface(self) -> float:
                return 42.0

        return MockedReinforcement()

    def test__get_volume_cost_calculator_with_valid_data(self):
        # 1. Define test data.
        _builder = VolumeCostParametersBuilder()
        _builder.reinforced_profile = self._get_mocked_reinforcement()

        # Set layers wrapper
        _wrapper = ReinforcementLayersWrapper()
        _builder.reinforced_profile.layers_wrapper = _wrapper
        _wrapper.base_layer = self._get_mocked_layer(KoswatMaterialType.SAND, 1.2, 2.1)
        _clay_layer = self._get_mocked_layer(KoswatMaterialType.CLAY, 2.4, 4.2)
        _grass_layer = self._get_mocked_layer(KoswatMaterialType.GRASS, 4.8, 8.4)
        _wrapper.coating_layers = [_clay_layer, _grass_layer]

        # 2. Run test
        _vcp = _builder._get_volume_cost_calculator()

        # 3. Verify expectations.
        assert isinstance(_vcp, VolumeCostParametersCalculator)
        assert _vcp.grass_layer_removal_volume == 4.8
        assert _vcp.clay_layer_removal_volume == 2.4
        assert _vcp.new_core_layer_volume == 1.2
        assert _vcp.new_core_layer_surface == 2.1
        assert _vcp.new_clay_layer_volume == 2.4
        assert _vcp.new_clay_layer_surface == 4.2
        assert _vcp.new_grass_layer_volume == 4.8
        assert _vcp.new_grass_layer_surface == 8.4
        assert _vcp.new_maaiveld_surface == 42

    def test_build_with_valid_data(self):
        # 1. Define test data.
        _builder = VolumeCostParametersBuilder()
        _builder.reinforced_profile = self._get_mocked_reinforcement()

        # Set layers wrapper
        _wrapper = ReinforcementLayersWrapper()
        _builder.reinforced_profile.layers_wrapper = _wrapper
        _wrapper.base_layer = self._get_mocked_layer(KoswatMaterialType.SAND, 1.2, 2.1)
        _clay_layer = self._get_mocked_layer(KoswatMaterialType.CLAY, 2.4, 4.2)
        _grass_layer = self._get_mocked_layer(KoswatMaterialType.GRASS, 4.8, 8.4)
        _wrapper.coating_layers = [_clay_layer, _grass_layer]

        # Set default dike profile costs.
        _costs = KoswatCostsSettings()
        _builder.koswat_costs = _costs

        _costs.dike_profile_costs = DikeProfileCostsSettings()
        _costs.dike_profile_costs.added_layer_grass_m3 = 12.44
        _costs.dike_profile_costs.added_layer_clay_m3 = 18.05
        _costs.dike_profile_costs.added_layer_sand_m3 = 10.98
        _costs.dike_profile_costs.reused_layer_grass_m3 = 6.04
        _costs.dike_profile_costs.reused_layer_core_m3 = 4.67
        _costs.dike_profile_costs.disposed_material_m3 = 7.07
        _costs.dike_profile_costs.profiling_layer_grass_m2 = 0.88
        _costs.dike_profile_costs.profiling_layer_clay_m2 = 0.65
        _costs.dike_profile_costs.profiling_layer_sand_m2 = 0.60
        _costs.dike_profile_costs.bewerken_maaiveld_m2 = 0.25

        # 2. Run test
        _vcp = _builder.build()

        # 3. Verify expectations.
        def evaluate_cost_and_volume(
            vcp_param: VolumeCostParameter, expected_cost: float, expected_volume: float
        ):
            assert vcp_param.cost == pytest.approx(expected_cost, 0.01)
            assert vcp_param.volume == pytest.approx(expected_volume, 0.01)

        assert isinstance(_vcp, VolumeCostParameters)
        evaluate_cost_and_volume(_vcp.reused_grass_volume, 6.04, 4.8)
        evaluate_cost_and_volume(_vcp.aanleg_grass_volume, 12.44, 0)
        evaluate_cost_and_volume(_vcp.aanleg_clay_volume, 18.05, 2.4)
        evaluate_cost_and_volume(_vcp.reused_core_volume, 4.67, 1.2)
        evaluate_cost_and_volume(_vcp.aanleg_core_volume, 10.98, 0)
        evaluate_cost_and_volume(_vcp.new_grass_layer_surface, 0.88, 8.4)
        evaluate_cost_and_volume(_vcp.new_clay_layer_surface, 0.65, 4.2)
        evaluate_cost_and_volume(_vcp.new_core_layer_surface, 0.6, 2.1)
        evaluate_cost_and_volume(_vcp.new_maaiveld_surface, 0.25, 42)
        evaluate_cost_and_volume(_vcp.removed_material_volume, 7.07, 1.2)
