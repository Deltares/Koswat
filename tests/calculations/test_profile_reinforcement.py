from typing import List

import pytest
from shapely.geometry.point import Point

from koswat.calculations.profile_calculation_protocol import ProfileCalculationProtocol
from koswat.calculations.profile_reinforcement import ProfileReinforcement
from koswat.koswat_scenario import KoswatScenario
from koswat.profiles.koswat_input_profile import KoswatInputProfile
from koswat.profiles.koswat_profile import KoswatProfile


class TestProfileReinforcement:
    def test_initialize_profile_reinforcement(self):
        _calculation = ProfileReinforcement()
        assert _calculation
        assert isinstance(_calculation, ProfileCalculationProtocol)

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
        _old_data_dict = expected_profile.__dict__
        assert len(_new_data_dict) >= 10
        assert len(_new_data_dict) == len(_old_data_dict)
        return [
            f"Values differ for {key}, expected {value}, got: {_new_data_dict[key]}"
            for key, value in _old_data_dict.items()
            if not self.almost_equal(_new_data_dict[key], value)
        ]

    def verify_equal_profiles(
        self, new_profile: KoswatProfile, expected_profile: KoswatProfile
    ):
        _found_errors = self._compare_koswat_input_profile(
            new_profile.input_data, expected_profile.input_data
        )
        _found_errors.extend(
            self._compare_points(new_profile.points, expected_profile.points)
        )
        if _found_errors:
            _mssg = "\n".join(_found_errors)
            pytest.fail(_mssg)

    def test_given_profile_and_scenario_calculate_new_geometry(self):
        # 1. Define test data.
        _input_profile_data = KoswatInputProfile.from_dict(
            dict(
                buiten_maaiveld=0,
                buiten_talud=3,
                buiten_berm_hoogte=0,
                buiten_berm_breedte=0,
                kruin_hoogte=6,
                kruin_breedte=5,
                binnen_talud=3,
                binnen_berm_hoogte=0,
                binnen_berm_breedte=0,
                binnen_maaiveld=0,
            )
        )
        assert isinstance(_input_profile_data, KoswatInputProfile)

        _profile = KoswatProfile.from_koswat_input_profile(_input_profile_data)
        assert isinstance(_profile, KoswatProfile)
        _scenario = KoswatScenario.from_dict(
            dict(
                d_h=1,
                d_s=10,
                d_p=30,
                kruin_breedte=5,
                buiten_talud=3,
            )
        )
        assert isinstance(_scenario, KoswatScenario)
        _expected_new_data = KoswatInputProfile.from_dict(
            dict(
                buiten_maaiveld=0,
                buiten_talud=3,
                buiten_berm_breedte=0,
                buiten_berm_hoogte=0,
                kruin_hoogte=7,
                kruin_breedte=5,
                binnen_talud=3.57,
                binnen_berm_hoogte=1,
                binnen_berm_breedte=20,
                binnen_maaiveld=0,
            )
        )
        _expected_profile = KoswatProfile.from_koswat_input_profile(_expected_new_data)

        # 2. Run test.
        _new_profile = ProfileReinforcement().calculate_new_profile(_profile, _scenario)

        # 3. Verify expectations.
        assert isinstance(_new_profile, KoswatProfile)
        assert isinstance(_new_profile.input_data, KoswatInputProfile)
        self.verify_equal_profiles(_new_profile, _expected_profile)

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
        _new_binnen_talud = ProfileReinforcement()._calculate_new_binnen_talud(
            _input_profile, _scenario
        )

        # 3. Verify expectations
        assert _new_binnen_talud == pytest.approx(_expected_value, 0.001)

    def test_calculate_new_binnen_berm_hoogte(self):
        # 1. Define test data.
        _exepcted_value = 1
        _scenario = KoswatScenario()
        _scenario.d_h = 1
        _old_data = KoswatInputProfile()
        _old_data.binnen_berm_hoogte = 0
        _old_data.kruin_hoogte = 6
        _new_data = KoswatInputProfile()
        _new_data.binnen_berm_breedte = 20

        # 2. Run test
        _new_binnen_berm_hoogte = (
            ProfileReinforcement()._calculate_new_binnen_berm_hoogte(
                _old_data, _new_data, _scenario
            )
        )

        # 3. Verify expectations
        assert _new_binnen_berm_hoogte == pytest.approx(_exepcted_value, 0.001)

    def test_calculate_new_binnen_berm_hoogte_negative_binnen_berm_breedte(self):
        # 1. Define test data.
        _exepcted_value = 0
        _scenario = KoswatScenario()
        _old_data = KoswatInputProfile()
        _new_data = KoswatInputProfile()
        _new_data.binnen_berm_breedte = -1

        # 2. Run test
        _new_binnen_berm_hoogte = (
            ProfileReinforcement()._calculate_new_binnen_berm_hoogte(
                _old_data, _new_data, _scenario
            )
        )

        # 3. Verify expectations
        assert _new_binnen_berm_hoogte == pytest.approx(_exepcted_value, 0.001)

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
            ProfileReinforcement()._calculate_new_binnen_berm_breedte(
                _old_profile, _new_profile, _scenario
            )
        )

        # 3. Verify expectations
        assert _new_binnen_berm_breedte == pytest.approx(_expected_value, 0.001)

    def test_calculate_new_kruin_hoogte(self):
        # 1. Define test data.
        _exepcted_value = 42.24
        _scenario = KoswatScenario()
        _scenario.d_h = 2.2
        _old_data = KoswatInputProfile()
        _old_data.kruin_hoogte = 40.04

        # 2. Run test
        _new_kruin_hoogte = ProfileReinforcement()._calculate_new_kruin_hoogte(
            _old_data, _scenario
        )

        # 3. Verify expectations
        assert _new_kruin_hoogte == pytest.approx(_exepcted_value, 0.001)
