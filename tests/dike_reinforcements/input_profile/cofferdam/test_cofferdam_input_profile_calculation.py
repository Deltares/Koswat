import pytest

from koswat.configuration.settings import KoswatScenario
from koswat.configuration.settings.reinforcements.koswat_cofferdam_settings import (
    KoswatCofferdamSettings,
)
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike_reinforcements.input_profile.cofferdam.cofferdam_input_profile import (
    CofferDamInputProfile,
)
from koswat.dike_reinforcements.input_profile.cofferdam.cofferdam_input_profile_calculation import (
    CofferdamInputProfileCalculation,
)
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_protocol import (
    ReinforcementInputProfileCalculationProtocol,
)


class TestCofferdamInputProfileCalculation:
    def test_initialize(self):
        _calculation = CofferdamInputProfileCalculation()
        assert _calculation
        assert not _calculation.base_profile
        assert not _calculation.scenario
        assert isinstance(_calculation, CofferdamInputProfileCalculation)
        assert isinstance(_calculation, ReinforcementInputProfileCalculationProtocol)

    @pytest.mark.parametrize(
        "soil_binnen_berm_breedte, expected",
        [
            pytest.param(0.0, 13.5, id="soil_binnen_berm_breedte=0"),
            pytest.param(30.0, 14.5, id="soil_binnen_berm_breedte=30"),
        ],
    )
    def test_calculate_length_cofferdam(
        self, soil_binnen_berm_breedte: float, expected: float
    ):
        class MockInputData(KoswatInputProfileProtocol):
            pleistoceen: float
            aquifer: float

        class MockSettings(KoswatCofferdamSettings):
            min_lengte_kistdam: float
            max_lengte_kistdam: float

        # 1. Define test data.
        _calculator = CofferdamInputProfileCalculation()
        _input_data = MockInputData()
        _input_data.pleistoceen = -5
        _input_data.aquifer = -2
        _cofferdam_settings = MockSettings()
        _cofferdam_settings.min_lengte_kistdam = 0
        _cofferdam_settings.max_lengte_kistdam = 99
        _soil_binnen_berm_breedte = soil_binnen_berm_breedte
        _new_kruin_hoogte = 8
        _expected_result = expected

        # 2. Run test.
        _result = _calculator._calculate_length_cofferdam(
            _input_data,
            _cofferdam_settings,
            _soil_binnen_berm_breedte,
            _new_kruin_hoogte,
        )

        # 3. Verify expectations
        assert _result == _expected_result

    def test_calculate_new_crest_height(self):
        class MockInputData(KoswatInputProfileProtocol):
            kruin_hoogte: float

        # 1. Define test data.
        _calculator = CofferdamInputProfileCalculation()
        _input_data = MockInputData()
        _input_data.kruin_hoogte = 6
        _scenario = KoswatScenario()
        _scenario.d_h = 2
        _expected_result = 8

        # 2. Run test.
        _result = _calculator._calculate_new_crest_height(_input_data, _scenario)

        # 3. Verify expectations
        assert _result == _expected_result

    def test_calculate_new_waterside_slope(self):
        class MockInputData(KoswatInputProfileProtocol):
            crest_height: float
            waterside_slope: float
            waterside_ground_level: float

        # 1. Define test data.
        _calculator = CofferdamInputProfileCalculation()
        _input_data = MockInputData()
        _input_data.crest_height = 8
        _input_data.waterside_ground_level = 2
        _input_data.waterside_slope = 3
        _scenario = KoswatScenario()
        _scenario.d_h = 2
        _expected_result = 2.25

        # 2. Run test.
        _result = _calculator._calculate_new_buiten_talud(_input_data, _scenario)

        # 3. Verify expectations
        assert _result == _expected_result

    def test_calculate_new_polderside_slope(self):
        class MockInputData(KoswatInputProfileProtocol):
            crest_width: float
            crest_height: float
            polderrside_ground_level: float
            polderside_slope: float

        # 1. Define test data.
        _expected_result = 2.25
        _calculator = CofferdamInputProfileCalculation()
        _input_data = MockInputData()
        _input_data.crest_height = 6
        _input_data.polderrside_ground_level = 0
        _input_data.polderside_slope = 3
        _input_data.crest_width = 5
        _scenario = KoswatScenario()
        _scenario.d_h = 2
        _scenario.crest_width = 5
        _scenario.polderside_slope = 3

        # 2. Run test.
        _result = _calculator._calculate_new_binnen_talud(_input_data, _scenario)

        # 3. Verify expectations
        assert _result == pytest.approx(_expected_result, 0.001)

    def test_calculate_new_input_profile(self):
        class MockInputData(KoswatInputProfileProtocol):
            dike_section: str
            waterside_ground_level: float
            waterside_slope: float
            waterside_berm_height: float
            waterside_berm_width: float
            crest_height: float
            crest_width: float
            polderside_slope: float
            polderside_berm_height: float
            polderside_berm_width: float
            polderside_ground_level: float
            ground_price_builtup: float
            ground_price_unbuilt: float
            factor_settlement: float
            pleistocene: float
            aquifer: float

        class MockSettings(KoswatCofferdamSettings):
            min_lengte_kistdam: float
            max_lengte_kistdam: float

        # 1. Define test data.
        _calculator = CofferdamInputProfileCalculation()
        _input_data = MockInputData()
        _input_data.dike_section = "mocked_section"
        _input_data.waterside_ground_level = 6.7
        _input_data.waterside_slope = 9.9
        _input_data.waterside_berm_height = 7.8
        _input_data.waterside_berm_width = 8.9
        _input_data.crest_height = 30
        _input_data.crest_width = 5.6
        _input_data.polderside_slope = 4.5
        _input_data.polderside_berm_height = 7.8
        _input_data.polderside_berm_width = 9.0
        _input_data.polderside_ground_level = 2.3
        _input_data.ground_price_builtup = 150
        _input_data.ground_price_unbuilt = 10
        _input_data.factor_settlement = 1.2
        _input_data.pleistocene = -6.7
        _input_data.aquifer = -2.3
        _cofferdam_settings = MockSettings()
        _cofferdam_settings.min_lengte_kistdam = 0
        _cofferdam_settings.max_lengte_kistdam = 99
        _scenario = KoswatScenario()
        _scenario.d_h = 12
        _scenario.crest_width = 6.7
        _scenario.polderside_slope = 7.8

        # 2. Run test.
        _result = _calculator._calculate_new_input_profile(
            _input_data, _cofferdam_settings, _scenario
        )

        # 3. Verify expectations
        assert isinstance(_result, CofferDamInputProfile)
        assert isinstance(_result, KoswatInputProfileBase)
        assert isinstance(_result, KoswatInputProfileProtocol)
