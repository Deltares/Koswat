from typing import Iterator

import pytest

from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase


@pytest.fixture
def valid_input_data() -> Iterator[KoswatInputProfileProtocol]:
    yield KoswatInputProfileBase(
        dike_section="mocked_section",
        waterside_ground_level=6.7,
        waterside_slope=9.9,
        waterside_berm_height=7.8,
        waterside_berm_width=8.9,
        crest_height=30,
        crest_width=5.6,
        polderside_slope=4.5,
        polderside_berm_height=7.8,
        polderside_berm_width=9.0,
        polderside_ground_level=2.3,
        ground_price_builtup=150,
        ground_price_unbuilt=10,
        factor_settlement=1.2,
        pleistocene=-6.7,
        aquifer=-2.3,
    )
