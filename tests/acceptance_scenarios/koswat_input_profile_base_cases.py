import pytest

from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from tests.acceptance_scenarios.cases_protocol import CasesProtocol


class InputProfileCases(CasesProtocol):
    default = KoswatInputProfileBase(
        dike_section="test_data",
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

    profile_case_2 = KoswatInputProfileBase(
        dike_section="test_data",
        waterside_ground_level=0,
        waterside_slope=4,
        waterside_berm_height=0,
        waterside_berm_width=0,
        crest_height=6.5,
        crest_width=5,
        polderside_slope=5.54,
        polderside_berm_height=2.6,
        polderside_berm_width=54,
        polderside_ground_level=0,
        ground_price_builtup=150,
        ground_price_unbuilt=10,
        factor_settlement=1.2,
        pleistocene=-5,
        aquifer=-2,
    )

    infra = KoswatInputProfileBase(
        dike_section="test_data",
        waterside_ground_level=0,
        waterside_slope=3,
        waterside_berm_height=0,
        waterside_berm_width=0,
        crest_height=6,
        crest_width=8,
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

    cases = [pytest.param(default, id="Def Input Profile")]


class AcceptanceTestInputProfileCases(CasesProtocol):
    profile_dijk1 = KoswatInputProfileBase(
        dike_section="dijk1",
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

    profile_dijk2 = KoswatInputProfileBase(
        dike_section="dijk2",
        waterside_ground_level=-2,
        waterside_slope=3,
        waterside_berm_height=-2,
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

    profile_dijk3 = KoswatInputProfileBase(
        dike_section="dijk3",
        waterside_ground_level=0,
        waterside_slope=3,
        waterside_berm_height=0,
        waterside_berm_width=0,
        crest_height=6,
        crest_width=5,
        polderside_slope=3,
        polderside_berm_height=-2,
        polderside_berm_width=0,
        polderside_ground_level=-2,
        ground_price_builtup=150,
        ground_price_unbuilt=10,
        factor_settlement=1.2,
        pleistocene=-5,
        aquifer=-2,
    )
