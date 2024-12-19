from dataclasses import dataclass

from koswat.configuration.settings.koswat_general_settings import ConstructionTypeEnum
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
                waterside_ground_level=0.0,
                waterside_slope=3.0,
                waterside_berm_width=0.0,
                waterside_berm_height=0.0,
                crest_height=8.0,
                crest_width=5.0,
                polderside_slope=3.0,
                polderside_berm_height=0.0,
                polderside_berm_width=0.0,
                polderside_ground_level=0.0,
                ground_price_builtup=150.0,
                ground_price_unbuilt=10.0,
                factor_settlement=1.2,
                pleistocene=-5.0,
                aquifer=-2.0,
                construction_length=6.0,
                construction_type=ConstructionTypeEnum.CB_DAMWAND,
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
                waterside_ground_level=0.0,
                waterside_slope=3.0,
                waterside_berm_width=0.0,
                waterside_berm_height=0.0,
                crest_height=8.0,
                crest_width=5.0,
                polderside_slope=1.5,
                polderside_berm_height=0.0,
                polderside_berm_width=0.0,
                polderside_ground_level=0.0,
                ground_price_builtup=150.0,
                ground_price_unbuilt=10.0,
                factor_settlement=1.2,
                pleistocene=-5.0,
                aquifer=-2.0,
                construction_length=14.5,
                construction_type=ConstructionTypeEnum.DAMWAND_VERANKERD,
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
                waterside_ground_level=0.0,
                waterside_slope=3.0,
                waterside_berm_width=0.0,
                waterside_berm_height=0.0,
                crest_height=7.0,
                crest_width=5.0,
                polderside_slope=3.57,
                polderside_berm_height=1.0,
                polderside_berm_width=20.0,
                polderside_ground_level=0.0,
                ground_price_builtup=150.0,
                ground_price_unbuilt=10.0,
                factor_settlement=1.2,
                pleistocene=-5.0,
                aquifer=-2.0,
                construction_length=0.0,
                construction_type=None,
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
                waterside_ground_level=0.0,
                waterside_slope=2.25,
                waterside_berm_width=0.0,
                waterside_berm_height=0.0,
                crest_height=8.0,
                crest_width=5.0,
                polderside_slope=2.25,
                polderside_berm_height=0.0,
                polderside_berm_width=0.0,
                polderside_ground_level=0.0,
                ground_price_builtup=150.0,
                ground_price_unbuilt=10.0,
                factor_settlement=1.2,
                pleistocene=-5.0,
                aquifer=-2.0,
                construction_length=14.5,
                construction_type=ConstructionTypeEnum.KISTDAM,
            ),
            koswat_layers_case=LayersCases.without_layers,
            p4_x_coordinate=0,
        ),
    ),
]
