from tests.acceptance_scenarios.acceptance_test_scenario_dataclasses import (
    AcceptanceTestScenarioCombinations,
)
from tests.acceptance_scenarios.koswat_input_profile_base_cases import (
    AcceptanceTestInputProfileCases,
)
from tests.acceptance_scenarios.koswat_scenario_test_cases import (
    ScenarioCasesAB,
    ScenarioCasesC,
    ScenarioCasesDijk4,
    ScenarioCasesDijk5,
)
from tests.acceptance_scenarios.layers_cases import LayersCases

acceptance_test_combinations = [
    AcceptanceTestScenarioCombinations(
        profile_case=AcceptanceTestInputProfileCases.profile_dijk1,
        layers_cases=[LayersCases.with_acc_crit],
        scenario_cases=ScenarioCasesAB.cases,
    ),
    AcceptanceTestScenarioCombinations(
        profile_case=AcceptanceTestInputProfileCases.profile_dijk2,
        layers_cases=[LayersCases.with_acc_crit],
        scenario_cases=ScenarioCasesAB.cases,
    ),
    AcceptanceTestScenarioCombinations(
        profile_case=AcceptanceTestInputProfileCases.profile_dijk3,
        layers_cases=[LayersCases.with_acc_crit],
        scenario_cases=ScenarioCasesC.cases,
    ),
    AcceptanceTestScenarioCombinations(
        profile_case=AcceptanceTestInputProfileCases.profile_dijk4,
        layers_cases=[LayersCases.with_acc_crit],
        scenario_cases=ScenarioCasesDijk4.cases,
    ),
    AcceptanceTestScenarioCombinations(
        profile_case=AcceptanceTestInputProfileCases.profile_dijk5,
        layers_cases=[LayersCases.with_acc_crit],
        scenario_cases=ScenarioCasesDijk5.cases,
    ),
]
