import pytest

from koswat.configuration.settings import KoswatScenario
from koswat.configuration.settings.koswat_general_settings import ConstructionTypeEnum
from koswat.configuration.settings.reinforcements.koswat_stability_wall_settings import (
    KoswatStabilityWallSettings,
)
from koswat.core.protocols import BuilderProtocol
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike_reinforcements.input_profile import StabilityWallInputProfile
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_protocol import (
    ReinforcementInputProfileCalculationProtocol,
)
from koswat.dike_reinforcements.input_profile.stability_wall.stability_wall_input_profile_calculation import (
    StabilityWallInputProfileCalculation,
)


class TestStabilityWallInputProfileCalculation:
    def test_initialize(self):
        _calculation = StabilityWallInputProfileCalculation()
        assert _calculation
        assert not _calculation.base_profile
        assert not _calculation.scenario
        assert isinstance(_calculation, StabilityWallInputProfileCalculation)
        assert isinstance(_calculation, ReinforcementInputProfileCalculationProtocol)
        assert isinstance(_calculation, BuilderProtocol)

    @pytest.mark.parametrize(
        "soil_binnen_berm_breedte, expected",
        [
            pytest.param(
                0,
                (13.5, ConstructionTypeEnum.DAMWAND_VERANKERD),
                id="soil_binnen_berm_breedte=0",
            ),
            pytest.param(
                30.0,
                (14.5, ConstructionTypeEnum.DIEPWAND),
                id="soil_binnen_berm_breedte=30",
            ),
        ],
    )
    def test_calculate_length_type_stability_wall(
        self,
        soil_binnen_berm_breedte: float,
        expected: tuple[float, ConstructionTypeEnum],
    ):
        class MockInputData(KoswatInputProfileProtocol):
            pleistoceen: float
            aquifer: float

        class MockSettings(KoswatStabilityWallSettings):
            min_length_stability_wall: float
            max_length_stability_wall: float

        # 1. Define test data.
        _calculator = StabilityWallInputProfileCalculation()
        _input_data = MockInputData()
        _input_data.pleistoceen = -5
        _input_data.aquifer = -2
        _stability_wall_settings = MockSettings()
        _stability_wall_settings.min_length_stability_wall = 0
        _stability_wall_settings.max_length_stability_wall = 99
        _stability_wall_settings.transition_sheetpile_diaphragm_wall = 14
        _soil_binnen_berm_breedte = soil_binnen_berm_breedte
        _new_kruin_hoogte = 8

        # 2. Run test.
        _length = _calculator._calculate_length_stability_wall(
            _input_data,
            _stability_wall_settings,
            _soil_binnen_berm_breedte,
            _new_kruin_hoogte,
        )
        _type = _calculator._determine_construction_type(
            _stability_wall_settings.transition_sheetpile_diaphragm_wall, _length
        )
        _result = (_length, _type)

        # 3. Verify expectations
        assert _result == expected

    def test_calculate_new_kruin_hoogte(self):
        class MockInputData(KoswatInputProfileProtocol):
            kruin_hoogte: float

        # 1. Define test data.
        _calculator = StabilityWallInputProfileCalculation()
        _input_data = MockInputData()
        _input_data.kruin_hoogte = 30
        _scenario = KoswatScenario()
        _scenario.d_h = 12
        _expected_result = 42

        # 2. Run test.
        _result = _calculator._calculate_new_kruin_hoogte(_input_data, _scenario)

        # 3. Verify expectations
        assert _result == _expected_result

    def test_calculate_new_binnen_talud(self):
        class MockInputData(KoswatInputProfileProtocol):
            kruin_hoogte: float
            binnen_maaiveld: float
            binnen_talud: float
            kruin_breedte: float

        # 1. Define test data.
        _calculator = StabilityWallInputProfileCalculation()
        _input_data = MockInputData()
        _input_data.kruin_hoogte = 30
        _input_data.binnen_maaiveld = 2.3
        _input_data.binnen_talud = 4.5
        _input_data.kruin_breedte = 5.6
        _scenario = KoswatScenario()
        _scenario.d_h = 12
        _scenario.crest_width = 6.7
        _scenario.waterside_slope = 7.8
        _expected_result = 2

        # 2. Run test.
        _result = _calculator._calculate_new_binnen_talud(_input_data, _scenario)

        # 3. Verify expectations
        assert _result == _expected_result

    def test_calculate_new_input_profile(self):
        class MockInputData(KoswatInputProfileProtocol):
            dike_section: str
            kruin_hoogte: float
            binnen_berm_breedte: float
            binnen_maaiveld: float
            binnen_talud: float
            kruin_breedte: float
            buiten_berm_breedte: float
            buiten_talud: float
            grondprijs_bebouwd: float
            grondprijs_onbebouwd: float
            factor_zetting: float
            pleistoceen: float
            aquifer: float

        class MockSettings(KoswatStabilityWallSettings):
            min_length_stability_wall: float
            max_length_stability_wall: float

        # 1. Define test data.
        _calculator = StabilityWallInputProfileCalculation()
        _input_data = MockInputData()
        _input_data.dike_section = "mocked_section"
        _input_data.kruin_hoogte = 30
        _input_data.binnen_berm_breedte = 8.9
        _input_data.binnen_maaiveld = 2.3
        _input_data.binnen_talud = 4.5
        _input_data.kruin_breedte = 5.6
        _input_data.buiten_maaiveld = 6.7
        _input_data.buiten_berm_hoogte = 7.8
        _input_data.buiten_berm_breedte = 8.9
        _input_data.buiten_talud = 3.4
        _input_data.grondprijs_bebouwd = 150
        _input_data.grondprijs_onbebouwd = 10
        _input_data.factor_zetting = 1.2
        _input_data.pleistoceen = -6.7
        _input_data.aquifer = -2.3
        _stability_wall_settings = MockSettings()
        _stability_wall_settings.min_length_stability_wall = 0
        _stability_wall_settings.max_length_stability_wall = 99
        _scenario = KoswatScenario()
        _scenario.d_h = 12
        _scenario.crest_width = 6.7
        _scenario.waterside_slope = 7.8

        # 2. Run test.
        _result = _calculator._calculate_new_input_profile(
            _input_data, _stability_wall_settings, _scenario
        )

        # 3. Verify expectations
        assert isinstance(_result, StabilityWallInputProfile)
        assert isinstance(_result, KoswatInputProfileBase)
        assert isinstance(_result, KoswatInputProfileProtocol)
