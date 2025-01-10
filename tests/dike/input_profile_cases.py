import pytest

from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase

default_case = KoswatInputProfileBase.from_dict(
    dict(
        waterside_ground_level=0,
        waterside_slope=3,
        waterside_berm_height=0,
        waterside_berm_width=0,
        crest_height=6,
        crest_width=5,
        polderside_slope=3,
        polderside_berm_height=0,
        polderside_berm_width=0,
        polderside_ground_level=0,
        ground_price_builtup=150,
        ground_price_unbuilt=10,
        factor_settlement=1.2,
        pleistocene=-5,
        aquifer=-2,
    )
)

profile_cases = [
    pytest.param(
        default_case,
        id="Default profile case",
    )
]
