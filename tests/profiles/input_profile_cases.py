import pytest

from koswat.profiles.koswat_input_profile import KoswatInputProfile


def get_koswat_input_profile(input_data: dict) -> KoswatInputProfile:
    _input_profile = KoswatInputProfile()
    _input_profile.buiten_maaiveld = input_data["buiten_maaiveld"]
    _input_profile.buiten_talud = input_data["buiten_talud"]
    _input_profile.buiten_berm_hoogte = input_data["buiten_berm_hoogte"]
    _input_profile.buiten_berm_breedte = input_data["buiten_berm_breedte"]
    _input_profile.kruin_hoogte = input_data["kruin_hoogte"]
    _input_profile.kruin_breedte = input_data["kruin_breedte"]
    _input_profile.binnen_talud = input_data["binnen_talud"]
    _input_profile.binnen_berm_hoogte = input_data["binnen_berm_hoogte"]
    _input_profile.binnen_berm_breedte = input_data["binnen_berm_breedte"]
    _input_profile.binnen_maaiveld = input_data["binnen_maaiveld"]
    return _input_profile


default_case = get_koswat_input_profile(
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

profile_cases = [
    pytest.param(
        default_case,
        id="Default profile case",
    )
]
