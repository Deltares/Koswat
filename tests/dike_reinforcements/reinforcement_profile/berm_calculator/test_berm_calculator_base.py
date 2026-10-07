import pytest

from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike_reinforcements.input_profile.input_profile_enum import InputProfileEnum
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.piping_berm_calculator import (
    PipingBermCalculator,
)


class TestBermCalculatorBase:
    @pytest.mark.parametrize(
        "profile_type, expected",
        [
            pytest.param(InputProfileEnum.NONE, 2.1, id="Default"),
            pytest.param(
                InputProfileEnum.STABILITY_WALL_CREST,
                1.372727,
                id="Stability Wall Crest",
            ),
            pytest.param(
                InputProfileEnum.STABILITY_WALL_TOE, 1.372727, id="Stability Wall Toe"
            ),
        ],
    )
    def test__calculate_new_polderside_slope(
        self,
        valid_piping_berm_calculator: PipingBermCalculator,
        valid_input_profile: KoswatInputProfileProtocol,
        profile_type: InputProfileEnum,
        expected: float,
    ):
        # 1. Run test.
        _result = valid_piping_berm_calculator._calculate_new_polderside_slope(
            valid_input_profile, profile_type
        )

        # 2. Verify expectations
        assert _result == pytest.approx(expected, 0.001)

    @pytest.mark.parametrize(
        "steepening_polderside_slope, expected",
        [
            pytest.param(
                1.0,
                1.372727,
                id="Stability Wall Crest (1.0)",
            ),
            pytest.param(
                1.5,
                1.5,
                id="Stability Wall Crest (1.5)",
            ),
        ],
    )
    def test__calculate_new_polderside_slope_for_stability_wall_crest(
        self,
        valid_piping_berm_calculator: PipingBermCalculator,
        valid_input_profile: KoswatInputProfileProtocol,
        steepening_polderside_slope: float,
        expected: float,
    ):
        # 1. Setup test.
        _profile_type = InputProfileEnum.STABILITY_WALL_CREST
        valid_piping_berm_calculator.reinforcement_settings.stability_wall_crest_settings.steepening_polderside_slope = (
            steepening_polderside_slope
        )

        # 2. Run test.
        _result = valid_piping_berm_calculator._calculate_new_polderside_slope(
            valid_input_profile, _profile_type
        )

        # 3. Verify expectations
        assert _result == pytest.approx(expected, 0.001)

    @pytest.mark.parametrize(
        "steepening_polderside_slope, expected",
        [
            pytest.param(
                1.0,
                1.372727,
                id="Stability Wall Toe (1.0)",
            ),
            pytest.param(
                1.5,
                1.5,
                id="Stability Wall Toe (1.5)",
            ),
        ],
    )
    def test__calculate_new_polderside_slope_for_stability_wall_toe(
        self,
        valid_piping_berm_calculator: PipingBermCalculator,
        valid_input_profile: KoswatInputProfileProtocol,
        steepening_polderside_slope: float,
        expected: float,
    ):
        # 1. Setup test.
        _profile_type = InputProfileEnum.STABILITY_WALL_TOE
        valid_piping_berm_calculator.reinforcement_settings.stability_wall_toe_settings.steepening_polderside_slope = (
            steepening_polderside_slope
        )

        # 2. Run test.
        _result = valid_piping_berm_calculator._calculate_new_polderside_slope(
            valid_input_profile, _profile_type
        )

        # 3. Verify expectations
        assert _result == pytest.approx(expected, 0.001)

    @pytest.mark.parametrize(
        "extend_existing, expected",
        [pytest.param(False, 1.5, id="False"), pytest.param(True, 2.0, id="True")],
    )
    def test__calculate_new_polderside_berm_height_piping(
        self,
        valid_piping_berm_calculator: PipingBermCalculator,
        valid_input_profile: KoswatInputProfileProtocol,
        extend_existing: bool,
        expected: float,
    ):
        # 1. Run test.
        _result = (
            valid_piping_berm_calculator._calculate_new_polderside_berm_height_piping(
                valid_input_profile, valid_input_profile, extend_existing
            )
        )

        # 2. Verify expectations
        assert _result == pytest.approx(expected, 0.001)
