import pytest

from koswat.builder_protocol import BuilderProtocol
from koswat.calculations.reinforcement_profile_calculation_protocol import (
    ReinforcementInputProfileCalculationProtocol,
)
from koswat.calculations.standard_reinforcement.soil.soil_reinforcement_profile import (
    SoilReinforcementProfile,
)
from koswat.calculations.standard_reinforcement.soil.soil_reinforcement_profile_calculation import (
    SoilReinforcementProfileCalculation,
)
from koswat.configuration.settings import KoswatScenario
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase


class TestSoilReinforcementProfileCalculation:
    def test_initialize(self):
        _calculation = SoilReinforcementProfileCalculation()
        assert _calculation
        assert not _calculation.base_profile
        assert not _calculation.scenario
        assert isinstance(_calculation, SoilReinforcementProfileCalculation)
        assert isinstance(_calculation, ReinforcementInputProfileCalculationProtocol)
        assert isinstance(_calculation, BuilderProtocol)

    def test_calculate_new_binnen_talud(self):
        # 1. Define test data.
        _expected_value = 3.57
        _scenario = KoswatScenario()
        _scenario.d_h = 1
        _scenario.d_s = 10
        _scenario.d_p = 30
        _scenario.kruin_breedte = 5
        _scenario.buiten_talud = 3
        _input_profile = KoswatInputProfileBase()
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
        _old_data = KoswatInputProfileBase()
        _old_data.binnen_berm_hoogte = 0
        _old_data.kruin_hoogte = 6
        _new_data = KoswatInputProfileBase()
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
        _old_data = KoswatInputProfileBase()
        _new_data = KoswatInputProfileBase()
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
        _old_profile = KoswatInputProfileBase()
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
        _new_profile = KoswatInputProfileBase()
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
        _old_data = KoswatInputProfileBase()
        _old_data.kruin_hoogte = 40.04

        # 2. Run test
        _new_kruin_hoogte = (
            SoilReinforcementProfileCalculation()._calculate_new_kruin_hoogte(
                _old_data, _scenario
            )
        )

        # 3. Verify expectations
        assert _new_kruin_hoogte == pytest.approx(_expected_value, 0.001)
