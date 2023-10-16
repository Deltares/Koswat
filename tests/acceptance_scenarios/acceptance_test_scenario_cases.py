from tests.acceptance_scenarios.acceptance_test_scenario_dataclasses import (
    AcceptanceTestScenarioCombinations,
)
from tests.library_test_cases import InputProfileCases, LayersCases, ScenarioCases


acceptance_test_combinations = [
    AcceptanceTestScenarioCombinations(
        profile_case=InputProfileCases.default,
        layers_cases=[LayersCases.with_acceptance_criteria],
        scenario_cases=[ScenarioCases.default],
    )
]
