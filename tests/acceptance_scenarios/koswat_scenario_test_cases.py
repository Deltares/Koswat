import pytest

from koswat.configuration.settings.koswat_scenario import KoswatScenario
from tests.acceptance_scenarios.cases_protocol import CasesProtocol


class ScenarioCases(CasesProtocol):
    default = KoswatScenario(
        d_h=1,
        d_s=10,
        d_p=30,
        crest_width=5,
    )
    scenario_2 = KoswatScenario(
        d_h=0.5,
        d_s=20,
        d_p=80,
        crest_width=5,
        waterside_slope=4,
    )
    scenario_3 = KoswatScenario(
        d_h=2,
        d_s=10,
        d_p=30,
        crest_width=5,
        waterside_slope=3,
    )
    # TODO: not used
    scenario_infra = KoswatScenario(
        d_h=0,
        d_s=20,
        d_p=50,
        crest_width=8,
    )

    cases = [
        pytest.param(default, id="Default Scenario"),
        pytest.param(scenario_2, id="Scenario 2"),
        pytest.param(scenario_3, id="Scenario 3"),
    ]


class ScenarioCasesAB(CasesProtocol):
    cases = [
        KoswatScenario(
            scenario_name="1a_dh",
            d_h=0.5,
            d_s=0,
            d_p=0,
            crest_width=5,
            waterside_slope=3,
        ),
        KoswatScenario(
            scenario_name="1b_ds",
            d_h=0,
            d_s=6,
            d_p=0,
        ),
        KoswatScenario(
            scenario_name="1c_dp",
            d_h=0,
            d_s=0,
            d_p=20,
        ),
        KoswatScenario(
            scenario_name="1d_dhds",
            d_h=0.5,
            d_s=9.5,
            d_p=0,
        ),
        KoswatScenario(
            scenario_name="1e_dhdp",
            d_h=0.5,
            d_s=0,
            d_p=23,
        ),
        KoswatScenario(
            scenario_name="1f_dsdp",
            d_h=0,
            d_s=6,
            d_p=26,
        ),
        KoswatScenario(
            scenario_name="1g_dhdsdp",
            d_h=0.5,
            d_s=9.5,
            d_p=29.5,
        ),
        KoswatScenario(
            scenario_name="2a_dh",
            d_h=1,
            d_s=0,
            d_p=0,
        ),
        KoswatScenario(
            scenario_name="2b_ds",
            d_h=0,
            d_s=9,
            d_p=0,
        ),
        KoswatScenario(
            scenario_name="2c_dp",
            d_h=0,
            d_s=0,
            d_p=50,
        ),
        KoswatScenario(
            scenario_name="2d_dhds",
            d_h=1,
            d_s=16.5,
            d_p=0,
        ),
        KoswatScenario(
            scenario_name="2e_dhdp",
            d_h=1,
            d_s=0,
            d_p=56,
        ),
        KoswatScenario(
            scenario_name="2f_dsdp",
            d_h=0,
            d_s=9,
            d_p=59,
        ),
        KoswatScenario(
            scenario_name="2g_dhdsdp",
            d_h=1,
            d_s=16.5,
            d_p=66.5,
        ),
        # KoswatScenario(
        #     scenario_name="3a_dh_bt",
        #     d_h=0.5,
        #     d_s=0,
        #     d_p=0,
        #     buiten_talud=4,
        # ),
        # KoswatScenario(
        #     scenario_name="3b_ds_bt",
        #     d_h=0,
        #     d_s=6,
        #     d_p=0,
        #     buiten_talud=4,
        # ),
        # KoswatScenario(
        #     scenario_name="3c_dp_bt",
        #     d_h=0,
        #     d_s=0,
        #     d_p=26,
        #     buiten_talud=4,
        # ),
        # KoswatScenario(
        #     scenario_name="3d_dhds_bt",
        #     d_h=0.5,
        #     d_s=10,
        #     d_p=0,
        #     buiten_talud=4,
        # ),
        # KoswatScenario(
        #     scenario_name="3e_dhdp_bt",
        #     d_h=0.5,
        #     d_s=0,
        #     d_p=29.5,
        #     buiten_talud=4,
        # ),
        # KoswatScenario(
        #     scenario_name="3f_dsdp_bt",
        #     d_h=0,
        #     d_s=6,
        #     d_p=32,
        #     buiten_talud=4,
        # ),
        # KoswatScenario(
        #     scenario_name="3g_dhdsdp_bt",
        #     d_h=0.5,
        #     d_s=10,
        #     d_p=36,
        #     buiten_talud=4,
        # ),
        # KoswatScenario(
        #     scenario_name="3h_bt",
        #     d_h=0,
        #     d_s=0,
        #     d_p=0,
        #     buiten_talud=4,
        # ),
        # KoswatScenario(
        #     scenario_name="4a_dh_kb",
        #     d_h=0.5,
        #     d_s=0,
        #     d_p=0,
        #     kruin_breedte=10,
        # ),
        # KoswatScenario(
        #     scenario_name="4b_ds_kb",
        #     d_h=0,
        #     d_s=11,
        #     d_p=0,
        #     kruin_breedte=10,
        # ),
        # KoswatScenario(
        #     scenario_name="4c_dp_kb",
        #     d_h=0,
        #     d_s=0,
        #     d_p=25,
        #     kruin_breedte=10,
        # ),
        # KoswatScenario(
        #     scenario_name="4d_dhds_kb",
        #     d_h=0.5,
        #     d_s=14.5,
        #     d_p=0,
        #     kruin_breedte=10,
        # ),
        # KoswatScenario(
        #     scenario_name="4e_dhdp_kb",
        #     d_h=0.5,
        #     d_s=0,
        #     d_p=28,
        #     kruin_breedte=10,
        # ),
        # KoswatScenario(
        #     scenario_name="4f_dsdp_kb",
        #     d_h=0,
        #     d_s=11,
        #     d_p=31,
        #     kruin_breedte=10,
        # ),
        # KoswatScenario(
        #     scenario_name="4g_dhdsdp_kb",
        #     d_h=0.5,
        #     d_s=14.5,
        #     d_p=34.5,
        #     kruin_breedte=10,
        # ),
        # KoswatScenario(
        #     scenario_name="4h_kb",
        #     d_h=0,
        #     d_s=0,
        #     d_p=0,
        #     kruin_breedte=10,
        # ),
    ]


class ScenarioCasesC(CasesProtocol):
    cases = [
        KoswatScenario(
            scenario_name="1a_dh",
            d_h=0.5,
            d_s=0,
            d_p=0,
        ),
        KoswatScenario(
            scenario_name="1b_ds",
            d_h=0,
            d_s=8,
            d_p=0,
        ),
        KoswatScenario(
            scenario_name="1c_dp",
            d_h=0,
            d_s=0,
            d_p=20,
        ),
        KoswatScenario(
            scenario_name="1d_dhds",
            d_h=0.5,
            d_s=11.5,
            d_p=0,
        ),
        KoswatScenario(
            scenario_name="1e_dhdp",
            d_h=0.5,
            d_s=0,
            d_p=23,
        ),
        KoswatScenario(
            scenario_name="1f_dsdp",
            d_h=0,
            d_s=8,
            d_p=28,
        ),
        KoswatScenario(
            scenario_name="1g_dhdsdp",
            d_h=0.5,
            d_s=11.5,
            d_p=31.5,
        ),
        KoswatScenario(
            scenario_name="2a_dh",
            d_h=1,
            d_s=0,
            d_p=0,
        ),
        KoswatScenario(
            scenario_name="2b_ds",
            d_h=0,
            d_s=12,
            d_p=0,
        ),
        KoswatScenario(
            scenario_name="2c_dp",
            d_h=0,
            d_s=0,
            d_p=50,
        ),
        KoswatScenario(
            scenario_name="2d_dhds",
            d_h=1,
            d_s=19.5,
            d_p=0,
        ),
        KoswatScenario(
            scenario_name="2e_dhdp",
            d_h=1,
            d_s=0,
            d_p=56,
        ),
        KoswatScenario(
            scenario_name="2f_dsdp",
            d_h=0,
            d_s=12,
            d_p=62,
        ),
        KoswatScenario(
            scenario_name="2g_dhdsdp",
            d_h=1,
            d_s=19.5,
            d_p=69.5,
        ),
        # KoswatScenario(
        #     scenario_name="3a_dh_bt",
        #     d_h=0.5,
        #     d_s=0,
        #     d_p=0,
        #     buiten_talud=4,
        # ),
        # KoswatScenario(
        #     scenario_name="3b_ds_bt",
        #     d_h=0,
        #     d_s=8,
        #     d_p=0,
        #     buiten_talud=4,
        # ),
        # KoswatScenario(
        #     scenario_name="3c_dp_bt",
        #     d_h=0,
        #     d_s=0,
        #     d_p=28,
        #     buiten_talud=4,
        # ),
        # KoswatScenario(
        #     scenario_name="3d_dhds_bt",
        #     d_h=0.5,
        #     d_s=12,
        #     d_p=0,
        #     buiten_talud=4,
        # ),
        # KoswatScenario(
        #     scenario_name="3e_dhdp_bt",
        #     d_h=0.5,
        #     d_s=0,
        #     d_p=31.5,
        #     buiten_talud=4,
        # ),
        # KoswatScenario(
        #     scenario_name="3f_dsdp_bt",
        #     d_h=0,
        #     d_s=8,
        #     d_p=36,
        #     buiten_talud=4,
        # ),
        # KoswatScenario(
        #     scenario_name="3g_dhdsdp_bt",
        #     d_h=0.5,
        #     d_s=12,
        #     d_p=40,
        #     buiten_talud=4,
        # ),
        # KoswatScenario(
        #     scenario_name="3h_bt",
        #     d_h=0,
        #     d_s=0,
        #     d_p=0,
        #     buiten_talud=4,
        # ),
        # KoswatScenario(
        #     scenario_name="4a_dh_kb",
        #     d_h=0.5,
        #     d_s=0,
        #     d_p=0,
        #     kruin_breedte=10,
        # ),
        # KoswatScenario(
        #     scenario_name="4b_ds_kb",
        #     d_h=0,
        #     d_s=13,
        #     d_p=0,
        #     kruin_breedte=10,
        # ),
        # KoswatScenario(
        #     scenario_name="4c_dp_kb",
        #     d_h=0,
        #     d_s=0,
        #     d_p=25,
        #     kruin_breedte=10,
        # ),
        # KoswatScenario(
        #     scenario_name="4d_dhds_kb",
        #     d_h=0.5,
        #     d_s=16.5,
        #     d_p=0,
        #     kruin_breedte=10,
        # ),
        # KoswatScenario(
        #     scenario_name="4e_dhdp_kb",
        #     d_h=0.5,
        #     d_s=0,
        #     d_p=28,
        #     kruin_breedte=10,
        # ),
        # KoswatScenario(
        #     scenario_name="4f_dsdp_kb",
        #     d_h=0,
        #     d_s=13,
        #     d_p=33,
        #     kruin_breedte=10,
        # ),
        # KoswatScenario(
        #     scenario_name="4g_dhdsdp_kb",
        #     d_h=0.5,
        #     d_s=16.5,
        #     d_p=36.5,
        #     kruin_breedte=10,
        # ),
        # KoswatScenario(
        #     scenario_name="4h_kb",
        #     d_h=0,
        #     d_s=0,
        #     d_p=0,
        #     kruin_breedte=10,
        # ),
    ]


class ScenarioCasesDijk4(CasesProtocol):
    cases = [
        KoswatScenario(
            scenario_name="scen1",
            d_h=0.29,
            d_s=12.07,
            d_p=50,
        ),
        KoswatScenario(
            scenario_name="scen2",
            d_h=0.29,
            d_s=12.07,
            d_p=50,
            waterside_slope=2.75,
        ),
    ]


class ScenarioCasesDijk5(CasesProtocol):
    cases = [
        KoswatScenario(
            scenario_name="scen1",
            d_h=0.62,
            d_s=13.14,
            d_p=50,
        ),
        KoswatScenario(
            scenario_name="scen2",
            d_h=0.62,
            d_s=13.14,
            d_p=50,
            waterside_slope=3.00,
        ),
    ]
