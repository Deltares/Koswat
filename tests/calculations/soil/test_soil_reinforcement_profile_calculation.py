from typing import List

import pytest
from shapely.geometry.point import Point

from koswat.calculations.reinforcement_profile_calculation_protocol import (
    ReinforcementProfileCalculationProtocol,
)
from koswat.calculations.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.calculations.soil.soil_reinforcement_profile import SoilReinforcementProfile
from koswat.calculations.soil.soil_reinforcement_profile_calculation import (
    SoilReinforcementProfileCalculation,
)
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.layers.koswat_layers import KoswatLayers
from koswat.dike.profile.koswat_input_profile import KoswatInputProfile
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.dike.profile.koswat_profile_builder import KoswatProfileBuilder
from koswat.koswat_scenario import KoswatScenario
from tests.library_test_cases import (
    InputProfileCases,
    InputProfileScenarioLookup,
    LayersCases,
    ScenarioCases,
)


class TestSoilReinforcementProfileCalculation:
    def test_initialize(self):
        _calculation = SoilReinforcementProfileCalculation()
        assert _calculation
        assert isinstance(_calculation, SoilReinforcementProfileCalculation)
        assert isinstance(_calculation, ReinforcementProfileCalculationProtocol)

    def almost_equal(self, left_value: float, right_value: float) -> bool:
        return abs(left_value - right_value) <= 0.01

    def _compare_points(
        self, new_points: List[Point], expected_points: List[Point]
    ) -> List[str]:
        _new_points = [(p.x, p.y) for p in new_points]
        _expected_points = [(p.x, p.y) for p in expected_points]
        _wrong_points = []
        for idx, (x, y) in enumerate(_expected_points):
            _new_x, _new_y = _new_points[idx]
            if not (self.almost_equal(_new_x, x) and self.almost_equal(_new_y, y)):
                _wrong_points.append(
                    f"Point {idx + 1} differs expected: ({x},{y}), got: ({_new_x},{_new_y})"
                )
        return _wrong_points

    def _compare_koswat_input_profile(
        self, new_profile: KoswatInputProfile, expected_profile: KoswatInputProfile
    ) -> List[str]:
        _new_data_dict = new_profile.__dict__
        _expected_data_dict = expected_profile.__dict__
        assert len(_new_data_dict) >= 10
        assert len(_new_data_dict) == len(_expected_data_dict)
        return [
            f"Values differ for {key}, expected {value}, got: {_new_data_dict[key]}"
            for key, value in _expected_data_dict.items()
            if not self.almost_equal(_new_data_dict[key], value)
        ]

    def _compare_koswat_layers(
        self, new_layers: KoswatLayers, expected_layers: KoswatLayers
    ) -> List[str]:
        _tolerance = 0.001
        if not new_layers.base_layer.geometry.almost_equals(
            expected_layers.base_layer.geometry, _tolerance
        ):
            return [f"Geometries differ for base_layer."]
        _layers_errors = []
        for _idx, _c_layer in enumerate(expected_layers.coating_layers):
            _new_layer = new_layers.coating_layers[_idx]
            if not _new_layer.geometry.almost_equals(_c_layer.geometry, _tolerance):
                _layers_errors.append(
                    f"Geometries differ for layer {_c_layer.material.name}"
                )

        return _layers_errors

    def compare_koswat_profiles(
        self, new_profile: KoswatProfileBase, expected_profile: KoswatProfileBase
    ):
        _found_errors = self._compare_koswat_input_profile(
            new_profile.input_data, expected_profile.input_data
        )
        _found_errors = self._compare_koswat_layers(
            new_profile.layers, expected_profile.layers
        )
        _found_errors.extend(
            self._compare_points(new_profile.points, expected_profile.points)
        )
        if _found_errors:
            _mssg = "\n".join(_found_errors)
            pytest.fail(_mssg)

    @pytest.mark.parametrize(
        "profile_data, scenario_data, expected_profile_data",
        [
            pytest.param(
                InputProfileCases.default,
                ScenarioCases.default,
                InputProfileScenarioLookup.default_default_no_layers,
                id="Default input profile, Default Scenario",
            ),
            pytest.param(
                InputProfileCases.default,
                ScenarioCases.scenario_2,
                InputProfileScenarioLookup.default_scenario_2_no_layers,
                id="Default input profile, Scenario 2",
            ),
        ],
    )
    def test_given_profile_and_scenario_calculate_new_geometry(
        self,
        profile_data: dict,
        scenario_data: dict,
        expected_profile_data: dict,
    ):
        # 1. Define test data.
        _dummy_layers = LayersCases.without_layers
        expected_profile_data["profile_type"] = SoilReinforcementProfile
        _expected_profile = KoswatProfileBuilder.with_data(
            expected_profile_data
        ).build()
        assert isinstance(_expected_profile, SoilReinforcementProfile)
        _profile = KoswatProfileBuilder.with_data(
            dict(
                input_profile_data=profile_data,
                layers_data=_dummy_layers,
                p4_x_coordinate=0,
                profile_type=SoilReinforcementProfile,
            )
        ).build()
        assert isinstance(_profile, SoilReinforcementProfile)
        _scenario = KoswatScenario.from_dict(dict(scenario_data))
        assert isinstance(_scenario, KoswatScenario)

        # 2. Run test.
        _new_profile = SoilReinforcementProfileCalculation().calculate_new_profile(
            _profile, _scenario
        )

        # 3. Verify expectations.
        assert isinstance(_new_profile, SoilReinforcementProfile)
        assert isinstance(_new_profile.input_data, KoswatInputProfile)
        self.compare_koswat_profiles(_new_profile, _expected_profile)

    def test_calculate_new_binnen_talud(self):
        # 1. Define test data.
        _expected_value = 3.57
        _scenario = KoswatScenario()
        _scenario.d_h = 1
        _scenario.d_s = 10
        _scenario.d_p = 30
        _scenario.kruin_breedte = 5
        _scenario.buiten_talud = 3
        _input_profile = KoswatInputProfile()
        _input_profile.kruin_breedte = 5
        _input_profile.kruin_hoogte = 6
        _input_profile.binnen_talud = 3

        # 2. Run test
        _new_binnen_talud = (
            SoilReinforcementProfileCalculation()._calculate_new_binnen_talud(
                _input_profile, _scenario
            )
        )

        # 3. Verify expectations
        assert _new_binnen_talud == pytest.approx(_expected_value, 0.001)

    def test_calculate_new_binnen_berm_hoogte(self):
        # 1. Define test data.
        _expected_value = 1
        _scenario = KoswatScenario()
        _scenario.d_h = 1
        _old_data = KoswatInputProfile()
        _old_data.binnen_berm_hoogte = 0
        _old_data.kruin_hoogte = 6
        _new_data = KoswatInputProfile()
        _new_data.binnen_berm_breedte = 20

        # 2. Run test
        _new_binnen_berm_hoogte = (
            SoilReinforcementProfileCalculation()._calculate_new_binnen_berm_hoogte(
                _old_data, _new_data, _scenario
            )
        )

        # 3. Verify expectations
        assert _new_binnen_berm_hoogte == pytest.approx(_expected_value, 0.001)

    def test_calculate_new_binnen_berm_hoogte_negative_binnen_berm_breedte(self):
        # 1. Define test data.
        _expected_value = 0
        _scenario = KoswatScenario()
        _old_data = KoswatInputProfile()
        _new_data = KoswatInputProfile()
        _new_data.binnen_berm_breedte = -1

        # 2. Run test
        _new_binnen_berm_hoogte = (
            SoilReinforcementProfileCalculation()._calculate_new_binnen_berm_hoogte(
                _old_data, _new_data, _scenario
            )
        )

        # 3. Verify expectations
        assert _new_binnen_berm_hoogte == pytest.approx(_expected_value, 0.001)

    def test_calculate_new_binnen_berm_breedte(self):
        # 1. Define test data.
        _expected_value = 20
        _scenario = KoswatScenario()
        _scenario.d_h = 1
        _scenario.d_p = 30
        _scenario.buiten_talud = 3
        _old_profile = KoswatInputProfile()
        _old_profile.buiten_maaiveld = 0
        _old_profile.buiten_talud = 3
        _old_profile.buiten_berm_hoogte = 0
        _old_profile.buiten_berm_breedte = 0
        _old_profile.kruin_hoogte = 6
        _old_profile.kruin_breedte = 5
        _old_profile.binnen_talud = 3
        _old_profile.binnen_berm_hoogte = 0
        _old_profile.binnen_berm_breedte = 0
        _old_profile.binnen_maaiveld = 0
        _new_profile = KoswatInputProfile()
        _new_profile.binnen_talud = 3.5714
        _new_profile.buiten_berm_breedte = 0
        _new_profile.kruin_breedte = 5

        # 2. Run test
        _new_binnen_berm_breedte = (
            SoilReinforcementProfileCalculation()._calculate_new_binnen_berm_breedte(
                _old_profile, _new_profile, _scenario
            )
        )

        # 3. Verify expectations
        assert _new_binnen_berm_breedte == pytest.approx(_expected_value, 0.001)

    def test_calculate_new_kruin_hoogte(self):
        # 1. Define test data.
        _expected_value = 42.24
        _scenario = KoswatScenario()
        _scenario.d_h = 2.2
        _old_data = KoswatInputProfile()
        _old_data.kruin_hoogte = 40.04

        # 2. Run test
        _new_kruin_hoogte = (
            SoilReinforcementProfileCalculation()._calculate_new_kruin_hoogte(
                _old_data, _scenario
            )
        )

        # 3. Verify expectations
        assert _new_kruin_hoogte == pytest.approx(_expected_value, 0.001)
