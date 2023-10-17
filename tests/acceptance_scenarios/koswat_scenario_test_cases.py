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
