from dataclasses import dataclass

from koswat.configuration.settings.koswat_scenario import KoswatScenario
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike_reinforcements.input_profile import (
    CofferDamInputProfile,
    PipingWallInputProfile,
    SoilInputProfile,
    StabilityWallInputProfile,
)
from koswat.dike_reinforcements.reinforcement_profile import (
    CofferdamReinforcementProfile,
    PipingWallReinforcementProfile,
    SoilReinforcementProfile,
    StabilityWallReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from tests.acceptance_scenarios.acceptance_test_scenario_dataclasses import (
    LayersTestCase,
)
from tests.acceptance_scenarios.koswat_input_profile_base_cases import InputProfileCases
from tests.acceptance_scenarios.koswat_scenario_test_cases import ScenarioCases
from tests.acceptance_scenarios.layers_cases import LayersCases


@dataclass
class ReinforcementProfileCase:
    case_name: str
    koswat_input_profile_base_case: KoswatInputProfileBase
    koswat_scenario_case: KoswatScenario
    reinforcement_profile_type: type[ReinforcementProfileProtocol]
    expected_reinforcement_profile: ReinforcementProfileProtocol


@dataclass
class ReinforcementProfileCaseExpectation:
    input_profile_base: KoswatInputProfileBase
    koswat_layers_case: LayersTestCase
    p4_x_coordinate: int


@dataclass
class ReinforcementProfileCaseCombination:
    case_name: str
    koswat_scenario_case: KoswatScenario
    reinforcement_profile_type: type[ReinforcementProfileProtocol]
    expectation: ReinforcementProfileCaseExpectation
    p4_x_coordinate: int = 0
    koswat_layers_case: LayersTestCase = LayersCases.without_layers
    input_profile_case: KoswatInputProfileProtocol = InputProfileCases.default


reinforcement_profile_cases = [
    ReinforcementProfileCaseCombination(
        case_name="Piping Wall, Default input profile, Scenario 3",
        koswat_scenario_case=ScenarioCases.scenario_3,
        reinforcement_profile_type=PipingWallReinforcementProfile,
        expectation=ReinforcementProfileCaseExpectation(
            input_profile_base=PipingWallInputProfile(
                dike_section="test_data",
                buiten_maaiveld=0,
                buiten_talud=3,
                buiten_berm_breedte=0,
                buiten_berm_hoogte=0,
                kruin_hoogte=8,
                kruin_breedte=5,
                binnen_talud=3,
                binnen_berm_hoogte=0,
                binnen_berm_breedte=0,
                binnen_maaiveld=0,
                pleistoceen=-5,
                aquifer=-2,
                construction_length=6.0,
            ),
            koswat_layers_case=LayersCases.without_layers,
            p4_x_coordinate=6,
        ),
    ),
    ReinforcementProfileCaseCombination(
        case_name="Stability Wall, Default input profile, Scenario 3",
        koswat_scenario_case=ScenarioCases.scenario_3,
        reinforcement_profile_type=StabilityWallReinforcementProfile,
        expectation=ReinforcementProfileCaseExpectation(
            input_profile_base=StabilityWallInputProfile(
                dike_section="test_data",
                buiten_maaiveld=0,
                buiten_talud=3,
                buiten_berm_breedte=0,
                buiten_berm_hoogte=0,
                kruin_hoogte=8,
                kruin_breedte=5,
                binnen_talud=2.00,
                binnen_berm_hoogte=0,
                binnen_berm_breedte=0,
                binnen_maaiveld=0,
                pleistoceen=-5,
                aquifer=-2,
                construction_length=13.8,
            ),
            koswat_layers_case=LayersCases.without_layers,
            p4_x_coordinate=6,
        ),
    ),
    ReinforcementProfileCaseCombination(
        case_name="Soil, Default input profile, Default Scenario",
        koswat_scenario_case=ScenarioCases.default,
        reinforcement_profile_type=SoilReinforcementProfile,
        expectation=ReinforcementProfileCaseExpectation(
            input_profile_base=SoilInputProfile(
                dike_section="test_data",
                buiten_maaiveld=0,
                buiten_talud=3,
                buiten_berm_breedte=0,
                buiten_berm_hoogte=0,
                kruin_hoogte=7,
                kruin_breedte=5,
                binnen_talud=3.57,
                binnen_berm_hoogte=1,
                binnen_berm_breedte=20,
                binnen_maaiveld=0,
                pleistoceen=-5,
                aquifer=-2,
            ),
            koswat_layers_case=LayersCases.without_layers,
            p4_x_coordinate=3,
        ),
    ),
    ReinforcementProfileCaseCombination(
        case_name="Cofferdam, default input scenario",
        koswat_scenario_case=ScenarioCases.scenario_3,
        reinforcement_profile_type=CofferdamReinforcementProfile,
        expectation=ReinforcementProfileCaseExpectation(
            input_profile_base=CofferDamInputProfile(
                dike_section="test_data",
                buiten_maaiveld=0,
                buiten_talud=2.25,
                buiten_berm_breedte=0,
                buiten_berm_hoogte=0,
                kruin_hoogte=8,
                kruin_breedte=5,
                binnen_talud=2.25,
                binnen_berm_hoogte=0,
                binnen_berm_breedte=0,
                binnen_maaiveld=0,
                pleistoceen=-5,
                aquifer=-2,
                construction_length=14.5,
            ),
            koswat_layers_case=LayersCases.without_layers,
            p4_x_coordinate=0,
        ),
    ),
]
