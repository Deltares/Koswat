import pytest

from koswat.calculations.calculation_protocol import CalculationProtocol
from koswat.calculations.profile_reinforcement import ProfileReinforcement
from koswat.koswat_scenario import KoswatScenario
from koswat.profiles.koswat_input_profile import KoswatInputProfile
from koswat.profiles.koswat_profile import KoswatProfile


class TestProfileReinforcement:
    def test_initialize_profile_reinforcement(self):
        _calculation = ProfileReinforcement()
        assert _calculation
        assert isinstance(_calculation, CalculationProtocol)

    def verify_equal_profiles(
        self, new_profile: KoswatProfile, expected_profile: KoswatProfile
    ):
        # 1. Compare input profile data.
        _new_data_dict = new_profile.input_data.__dict__
        _old_data_dict = expected_profile.input_data.__dict__
        _wrong_values = [
            f"Values differ for {key}, got: {_new_data_dict[key]}, expected {value}"
            for key, value in _old_data_dict.items()
            if _new_data_dict[key] != value
        ]
        if _wrong_values:
            _mssg = "\n".join(_wrong_values)
            pytest.fail(_mssg)

        # 2. Compare generated points.
        _new_points = [(p.x, p.y) for p in new_profile.points]
        _expected_points = [(p.x, p.y) for p in expected_profile.points]
        assert _new_points == _expected_points

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
        _new_profile = ProfileReinforcement().calculate_new_geometry(
            _profile, _scenario
        )

        # 3. Verify expectations.
        assert isinstance(_new_profile, KoswatProfile)
        assert isinstance(_new_profile.input_data, KoswatInputProfile)
        self.verify_equal_profiles(_new_profile, _expected_profile)
