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

    cases = [pytest.param(default, id="Default Input Profile")]


class AcceptanceTestInputProfileCases(CasesProtocol):
    # Equal ground levels waterside and polderside, no berms
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

    # Waterside ground level lower than polderside ground level, no berms
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

    # Waterside ground level higher than polderside ground level, no berms
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

    # Waterside ground level higher than polderside, waterside and polderside berm
    profile_dijk4 = KoswatInputProfileBase(
        dike_section="dijk4",
        waterside_ground_level=6.28,
        waterside_slope=2.74,
        waterside_berm_height=8.9,
        waterside_berm_width=4.42,
        crest_height=10.41,
        crest_width=2.75,
        polderside_slope=2.07,
        polderside_berm_height=9.43,
        polderside_berm_width=14.59,
        polderside_ground_level=5.17,
        ground_price_builtup=322.63,
        ground_price_unbuilt=13.87,
        factor_settlement=1.2,
        pleistocene=3.17,
        aquifer=6.06,
    )

    # Waterside ground level higher than polderside, polderside berm
    profile_dijk5 = KoswatInputProfileBase(
        dike_section="dijk5",
        waterside_ground_level=7.64,
        waterside_slope=2.99,
        waterside_berm_height=7.64,
        waterside_berm_width=0,
        crest_height=11.28,
        crest_width=2.36,
        polderside_slope=2.03,
        polderside_berm_height=10.69,
        polderside_berm_width=13.27,
        polderside_ground_level=6.81,
        ground_price_builtup=322.63,
        ground_price_unbuilt=13.87,
        factor_settlement=1.2,
        pleistocene=3.53,
        aquifer=6.42,
        top_layer_thickness=4.4,
    )
