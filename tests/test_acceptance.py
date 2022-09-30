import math

import pytest

from koswat.calculations.profile_reinforcement import ProfileReinforcement
from koswat.calculations.profile_volume_calculator import ProfileVolumeCalculator
from koswat.koswat_scenario import KoswatScenario
from koswat.profiles.koswat_input_profile import KoswatInputProfile
from koswat.profiles.koswat_layers import KoswatLayers
from koswat.profiles.koswat_profile import KoswatProfile
from koswat.profiles.koswat_profile_builder import KoswatProfileBuilder


class TestAcceptance:
    def test_koswat_package_can_be_imported(self):
        """
        Import test. Not really necessary given the current way we are testing (directly to the cli). But better safe than sorry.
        """

        try:
            import koswat
            import koswat.main
        except ImportError as exc_err:
            pytest.fail(f"It was not possible to import required packages {exc_err}")

    def test_given_default_case_returns_costs(self):
        # 1. Define test data.
        _layers = dict(
            base_layer=dict(material="zand"),
            coating_layers=[
                # dict(material="klei", depth=2.4),
                # dict(material="gras", depth=4.2),
            ],
        )
        _input_profile = dict(
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

        _profile = KoswatProfileBuilder.with_data(_input_profile, _layers).build()
        assert isinstance(_profile, KoswatProfile)

        # 2. Run test.
        _new_profile = ProfileReinforcement().calculate_new_profile(_profile, _scenario)
        _total_volume = ProfileVolumeCalculator().calculate_total_volume(
            _profile, _new_profile
        )

        # 3. Verify eexpectations.
        assert not math.isnan(_total_volume)
        assert _total_volume > 0
