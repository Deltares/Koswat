import pytest

from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase

default_case = KoswatInputProfileBase.from_dict(
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
        pleistoceen=-5,
        aquifer=-2,
    )
)

profile_cases = [
    pytest.param(
        default_case,
        id="Default profile case",
    )
]
