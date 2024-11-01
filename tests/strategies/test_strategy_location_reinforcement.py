from typing import Iterator

import pytest

from koswat.dike_reinforcements.reinforcement_profile.outside_slope.cofferdam_reinforcement_profile import (
    CofferdamReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile import (
    ReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.piping_wall_reinforcement_profile import (
    PipingWallReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.soil_reinforcement_profile import (
    SoilReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.stability_wall_reinforcement_profile import (
    StabilityWallReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.vps_reinforcement_profile import (
    VPSReinforcementProfile,
)
from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)
from koswat.strategies.strategy_step.strategy_step_enum import StrategyStepEnum


class TestStrategyLocationReinforcement:
    def test_initialize(self):
        # 1. Define test data.
        _slr = StrategyLocationReinforcement(location=None)

        # 2. Verify expectations.
        assert isinstance(_slr, StrategyLocationReinforcement)
        assert not _slr.filtered_measures
        assert not _slr.available_measures
        assert _slr.location is None
        assert _slr.current_selected_measure is None
        assert _slr.cheapest_reinforcement is None
        assert _slr.current_cost == 0.0

    @pytest.fixture(name="basic_valid_slr")
    def _get_basic_valid_strategy_location_reinforcement_fixture(
        self,
        example_location_reinforcements_with_buffering: list[
            StrategyLocationReinforcement
        ],
    ) -> Iterator[StrategyLocationReinforcement]:
        assert any(example_location_reinforcements_with_buffering)
        yield example_location_reinforcements_with_buffering[0]

    def test_set_selected_measure_updates_current_selected_measure(
        self, basic_valid_slr: StrategyLocationReinforcement
    ):
        # 1. Define test data.
        _new_selection = CofferdamReinforcementProfile
        assert basic_valid_slr.current_selected_measure != _new_selection

        # 2. Run test.
        basic_valid_slr.set_selected_measure(_new_selection, None)

        # 3. Verify expectations.
        assert basic_valid_slr.current_selected_measure == _new_selection

    def test_given_only_initial_step_get_selected_measure_steps_return_all(
        self, basic_valid_slr: StrategyLocationReinforcement
    ):
        # 1. Define test data.
        assert len(basic_valid_slr._selected_measure_steps) == 1

        # 2. Run test.
        _steps = basic_valid_slr.get_selected_measure_steps()

        # 3. Verify expectations.
        assert len(_steps) == 3
        assert all(_s == basic_valid_slr.current_selected_measure for _s in _steps)

    def _add_extra_steps(
        self,
        slr: StrategyLocationReinforcement,
        step_type: StrategyStepEnum,
        steps: list[type[ReinforcementProfileProtocol]],
    ):
        for _step in steps:
            slr.set_selected_measure(_step, step_type)

    def test_given_extra_ordered_steps_get_selected_measure_steps_return_last_of_them(
        self,
        basic_valid_slr: StrategyLocationReinforcement,
    ):
        # 1. Define test data
        assert len(basic_valid_slr._selected_measure_steps) == 1

        _expected_initial_value = SoilReinforcementProfile
        _new_step_value = CofferdamReinforcementProfile
        assert basic_valid_slr.current_selected_measure == _expected_initial_value

        # 2. Run test.
        self._add_extra_steps(
            basic_valid_slr,
            StrategyStepEnum.ORDERED,
            [
                PipingWallReinforcementProfile,
                StabilityWallReinforcementProfile,
                _new_step_value,
            ],
        )
        _steps = basic_valid_slr.get_selected_measure_steps()

        # 3. Verify expectations.
        assert len(_steps) == 3
        assert _steps[0] == _expected_initial_value
        assert _steps[1] == _new_step_value
        assert _steps[2] == _new_step_value

    def test_given_extra_order_steps_get_selected_measure_steps_return_all(
        self,
        basic_valid_slr: StrategyLocationReinforcement,
    ):
        # 1. Define test data
        assert len(basic_valid_slr._selected_measure_steps) == 1

        _expected_initial_value = SoilReinforcementProfile
        _new_step_value = CofferdamReinforcementProfile
        assert basic_valid_slr.current_selected_measure == _expected_initial_value

        # 2. Run test.
        self._add_extra_steps(
            basic_valid_slr,
            StrategyStepEnum.INFRASTRUCTURE,
            [StabilityWallReinforcementProfile, _new_step_value],
        )
        _steps = basic_valid_slr.get_selected_measure_steps()

        # 3. Verify expectations.
        assert len(_steps) == 3
        assert _steps[0] == _expected_initial_value
        assert _steps[1] == _expected_initial_value
        assert _steps[2] == _new_step_value

    def test_given_extra_order_and_infra_steps_get_selected_measure_steps_return_all(
        self,
        basic_valid_slr: StrategyLocationReinforcement,
    ):
        # 1. Define test data
        assert len(basic_valid_slr._selected_measure_steps) == 1

        _expected_initial_value = SoilReinforcementProfile
        _new_step_value = CofferdamReinforcementProfile
        assert basic_valid_slr.current_selected_measure == _expected_initial_value

        # 2. Run test.
        self._add_extra_steps(
            basic_valid_slr,
            StrategyStepEnum.ORDERED,
            [VPSReinforcementProfile, PipingWallReinforcementProfile],
        )
        self._add_extra_steps(
            basic_valid_slr,
            StrategyStepEnum.INFRASTRUCTURE,
            [StabilityWallReinforcementProfile, _new_step_value],
        )
        _steps = basic_valid_slr.get_selected_measure_steps()

        # 3. Verify expectations.
        assert len(_steps) == 3
        assert _steps[0] == _expected_initial_value
        assert _steps[1] == PipingWallReinforcementProfile
        assert _steps[2] == _new_step_value
