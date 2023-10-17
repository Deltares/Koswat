from tests.acceptance_scenarios.acceptance_test_scenario_dataclasses import (
    AcceptanceTestScenarioCombinations,
)
from tests.acceptance_scenarios.koswat_input_profile_base_cases import (
    AcceptanceTestInputProfileCases,
)
from tests.acceptance_scenarios.koswat_scenario_test_cases import (
    Dijk1ScenarioCases,
    ScenarioCases,
)
from tests.acceptance_scenarios.layers_cases import LayersCases

acceptance_test_combinations = [
    AcceptanceTestScenarioCombinations(
        profile_case=AcceptanceTestInputProfileCases.profile_dijk1,
        layers_cases=[LayersCases.with_acceptance_criteria],
        scenario_cases=[
            Dijk1ScenarioCases.s1a_dh,
            Dijk1ScenarioCases.s1b_ds,
            Dijk1ScenarioCases.s1c_dp,
            Dijk1ScenarioCases.s1d_dhds,
            Dijk1ScenarioCases.s1e_dhdp,
            Dijk1ScenarioCases.s1f_dsdp,
            Dijk1ScenarioCases.s1g_dhdsdp,
            Dijk1ScenarioCases.s2a_dh,
            Dijk1ScenarioCases.s2b_ds,
            Dijk1ScenarioCases.s2c_dp,
            Dijk1ScenarioCases.s2d_dhds,
            Dijk1ScenarioCases.s2e_dhdp,
            Dijk1ScenarioCases.s2f_dsdp,
            Dijk1ScenarioCases.s2g_dhdsdp,
        ],
    ),
    AcceptanceTestScenarioCombinations(
        profile_case=AcceptanceTestInputProfileCases.profile_dijk2,
        layers_cases=[LayersCases.with_acceptance_criteria],
        scenario_cases=[ScenarioCases.default],
    ),
    AcceptanceTestScenarioCombinations(
        profile_case=AcceptanceTestInputProfileCases.profile_dijk3,
        layers_cases=[LayersCases.with_acceptance_criteria],
        scenario_cases=[ScenarioCases.default],
    ),
]
