import pytest

from koswat.configuration.settings.koswat_scenario import KoswatScenario
from tests.acceptance_scenarios.cases_protocol import CasesProtocol


class ScenarioCases(CasesProtocol):
    default = KoswatScenario(
        d_h=1,
        d_s=10,
        d_p=30,
        kruin_breedte=5,
        buiten_talud=3,
        scenario_name="default_scenario",
    )
    scenario_2 = KoswatScenario(
        d_h=0.5,
        d_s=20,
        d_p=80,
        kruin_breedte=5,
        buiten_talud=4,
    )
    scenario_3 = KoswatScenario(
        d_h=2,
        d_s=10,
        d_p=30,
        kruin_breedte=5,
        buiten_talud=3,
    )

    cases = [
        pytest.param(default, id="Default Scenario"),
        pytest.param(scenario_2, id="Scenario 2"),
        pytest.param(scenario_3, id="Scenario 3"),
    ]


class Dijk1ScenarioCases(CasesProtocol):
    s1a_dh = KoswatScenario(
        scenario_name="s1a_dh",
        d_h=0.5,
        d_s=0,
        d_p=0,
    )
    s1b_ds = KoswatScenario(
        scenario_name="s1b_ds",
        d_h=0,
        d_s=6,
        d_p=0,
    )
    s1c_dp = KoswatScenario(
        scenario_name="s1c_dp",
        d_h=0,
        d_s=0,
        d_p=20,
    )
    s1d_dhds = KoswatScenario(
        scenario_name="s1d_dhds",
        d_h=0.5,
        d_s=9.5,
        d_p=0,
    )
    s1e_dhdp = KoswatScenario(
        scenario_name="s1e_dhdp",
        d_h=0.5,
        d_s=0,
        d_p=23,
    )
    s1f_dsdp = KoswatScenario(
        scenario_name="s1f_dsdp",
        d_h=0,
        d_s=6,
        d_p=26,
    )
    s1g_dhdsdp = KoswatScenario(
        scenario_name="s1g_dhdsdp",
        d_h=0.5,
        d_s=9.5,
        d_p=29.5,
    )
    s2a_dh = KoswatScenario(
        scenario_name="s2a_dh",
        d_h=1,
        d_s=0,
        d_p=0,
    )
    s2b_ds = KoswatScenario(
        scenario_name="s2b_ds",
        d_h=0,
        d_s=9,
        d_p=0,
    )
    s2c_dp = KoswatScenario(
        scenario_name="s2c_dp",
        d_h=0,
        d_s=0,
        d_p=50,
    )
    s2d_dhds = KoswatScenario(
        scenario_name="s2d_dhds",
        d_h=1,
        d_s=16.5,
        d_p=0,
    )
    s2e_dhdp = KoswatScenario(
        scenario_name="s2e_dhdp",
        d_h=1,
        d_s=0,
        d_p=56,
    )
    s2f_dsdp = KoswatScenario(
        scenario_name="s2f_dsdp",
        d_h=0,
        d_s=9,
        d_p=59,
    )
    s2g_dhdsdp = KoswatScenario(
        scenario_name="s2g_dhdsdp",
        d_h=1,
        d_s=16.5,
        d_p=66.5,
    )

    cases = []
