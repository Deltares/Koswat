from tests.acceptance_scenarios.acceptance_test_scenario_dataclasses import (
    AcceptanceTestScenarioCombinations,
)
from tests.acceptance_scenarios.koswat_input_profile_base_cases import InputProfileCases
from tests.acceptance_scenarios.koswat_scenario_test_cases import ScenarioCases
from tests.acceptance_scenarios.layers_cases import LayersCases


acceptance_test_combinations = [
    AcceptanceTestScenarioCombinations(
        profile_case=InputProfileCases.default,
        layers_cases=[LayersCases.with_acceptance_criteria],
        scenario_cases=[ScenarioCases.default],
    ),
]
