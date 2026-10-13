import pytest

from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile import (
    ReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.strategies.strategy_reinforcement_widths import StrategyReinforcementWidths


class TestStrategyReinforcementWidths:

    @pytest.mark.parametrize(
        "max_width_polderside, max_width_waterside, expected",
        [
            pytest.param(
                float("nan"), 40, True, id="polderside_nan, waterside does not exceed"
            ),
            pytest.param(
                float("nan"), 0, False, id="polderside_nan, waterside exceeds"
            ),
            pytest.param(
                40, float("nan"), True, id="waterside_nan, polderside does not exceed"
            ),
            pytest.param(
                0, float("nan"), False, id="waterside_nan, polderside exceeds"
            ),
            pytest.param(15.0, 25.0, True, id="both_within"),
            pytest.param(0.0, 0.0, False, id="both_exceed"),
            pytest.param(0.0, 3.0, False, id="polderside_exceeds"),
            pytest.param(15.0, 0.0, False, id="waterside_exceeds"),
        ],
    )
    def test_when_within_given_other_widths_then_returns_expectation(
        self, max_width_polderside: float, max_width_waterside: float, expected: bool
    ):
        # 1. Define test data
        _widths = StrategyReinforcementWidths(
            width_polderside=15.0, width_waterside=25.0
        )
        other_widths = StrategyReinforcementWidths(
            width_polderside=max_width_polderside, width_waterside=max_width_waterside
        )

        # 2. Run test
        result = _widths.within(other_widths)

        # 3. Verify expectations
        assert result is expected

    @pytest.mark.parametrize(
        "width_polderside, width_waterside",
        [
            pytest.param(float("nan"), float("nan"), id="both nan"),
            pytest.param(
                float("nan"), 1.0, id="polderside_nan, waterside does not exceed"
            ),
            pytest.param(
                1.0, float("nan"), id="waterside_nan, polderside does not exceed"
            ),
        ],
    )
    def test_when_within_given_nan_width_then_returns_false(
        self, width_polderside: float, width_waterside: float
    ):
        # 1. Define test data
        _widths = StrategyReinforcementWidths(
            width_polderside=width_polderside, width_waterside=width_waterside
        )
        other_widths = StrategyReinforcementWidths(
            width_polderside=15.0, width_waterside=25.0
        )

        # 2. Run test
        result = _widths.within(other_widths)

        # 3. Verify expectations
        assert result is False

    def test_when_within_given_unbound_widths_then_returns_true(self):
        # 1. Define test data
        widths = StrategyReinforcementWidths(
            width_polderside=15.0, width_waterside=25.0
        )
        other_widths = StrategyReinforcementWidths(
            width_polderside=float("nan"), width_waterside=float("nan")
        )

        # 2. Run test
        result = widths.within(other_widths)

        # 3. Verify expectations
        assert result is True

    @pytest.mark.parametrize("values", [(float("nan")), (None)])
    def test_when_is_unbound_given_nan_widths_then_returns_true(self, values):
        # 1. Define test data
        _widths = StrategyReinforcementWidths(
            width_polderside=values, width_waterside=values
        )

        # 2. Run test
        result = _widths.is_unbound

        # 3. Verify expectations
        assert result is True

    def test_when_from_reinforcement_profile_given_reinforcement_profile_then_returns_widths(
        self,
    ):
        # 1. Define test data
        class MockedReinforcementProfile(ReinforcementProfileProtocol):
            def __init__(self):
                self.new_ground_polderside = 30.0
                self.new_ground_waterside = 50.0

        # 2. Run test
        result = StrategyReinforcementWidths.from_reinforcement_profile(
            MockedReinforcementProfile()
        )

        # 3. Verify expectations
        assert result.width_polderside == 30.0
        assert result.width_waterside == 50.0
