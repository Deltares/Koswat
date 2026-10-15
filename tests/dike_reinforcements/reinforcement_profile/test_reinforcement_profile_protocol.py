import pytest

from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_protocol import (
    ReinforcementInputProfileProtocol,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)


class TestReinforcementProfileProtocol:
    def test_initialize_reinforcement_profile_raises(self):
        with pytest.raises(TypeError) as exc_err:
            ReinforcementProfileProtocol()

        assert str(exc_err.value) == "Protocols cannot be instantiated"

    @pytest.mark.parametrize(
        "waterside_slope, waterside_berm_height, waterside_berm_width, expected_value",
        [
            pytest.param(1.0, 2.0, 5.0, False, id="No change"),
            pytest.param(2.0, 2.0, 5.0, True, id="Slope changed"),
            pytest.param(1.0, 3.0, 5.0, True, id="Berm height changed"),
            pytest.param(1.0, 2.0, 6.0, True, id="Berm width changed"),
            pytest.param(2.0, 3.0, 6.0, True, id="All changed"),
        ],
    )
    def test_when_waterside_changed_given_profile_then_returns_expected_value(
        self,
        waterside_slope: float,
        waterside_berm_height: float,
        waterside_berm_width: float,
        expected_value: bool,
    ):
        class DummyInputData(ReinforcementInputProfileProtocol):
            waterside_slope = 1.0
            waterside_berm_height = 2.0
            waterside_berm_width = 5.0

        class DummyInputProfile(KoswatInputProfileProtocol):
            input_data = DummyInputData()

        class DummyReinforcementProfile(ReinforcementProfileProtocol):
            old_profile = DummyInputProfile()
            input_data = DummyInputData()

        # 1. Define test data
        _profile = DummyReinforcementProfile()
        _profile.input_data.waterside_slope = waterside_slope
        _profile.input_data.waterside_berm_height = waterside_berm_height
        _profile.input_data.waterside_berm_width = waterside_berm_width

        # 2. Run test
        _result = _profile.waterside_changed

        # 3. Verify result
        assert _result is expected_value
