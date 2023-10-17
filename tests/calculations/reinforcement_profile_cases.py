from dataclasses import dataclass
from koswat.calculations.outside_slope_reinforcement.cofferdam.cofferdam_input_profile import (
    CofferDamInputProfile,
)
from koswat.calculations.outside_slope_reinforcement.cofferdam.cofferdam_reinforcement_profile import (
    CofferdamReinforcementProfile,
)
from koswat.calculations.outside_slope_reinforcement.outside_slope_reinforcement_layers_wrapper_builder import (
    OutsideSlopeReinforcementLayersWrapperBuilder,
)
from koswat.calculations.outside_slope_reinforcement.outside_slope_reinforcement_profile import (
    OutsideSlopeReinforcementProfile,
)

from koswat.calculations.protocols.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.calculations.standard_reinforcement.piping_wall.piping_wall_input_profile import (
    PipingWallInputProfile,
)
from koswat.calculations.standard_reinforcement.piping_wall.piping_wall_reinforcement_profile import (
    PipingWallReinforcementProfile,
)
from koswat.calculations.standard_reinforcement.soil.soil_input_profile import (
    SoilInputProfile,
)
from koswat.calculations.standard_reinforcement.soil.soil_reinforcement_profile import (
    SoilReinforcementProfile,
)
from koswat.calculations.standard_reinforcement.stability_wall.stability_wall_input_profile import (
    StabilityWallInputProfile,
)
from koswat.calculations.standard_reinforcement.stability_wall.stability_wall_reinforcement_profile import (
    StabilityWallReinforcementProfile,
)
from koswat.calculations.standard_reinforcement.standard_reinforcement_layers_wrapper_builder import (
    StandardReinforcementLayersWrapperBuilder,
)
from koswat.calculations.standard_reinforcement.standard_reinforcement_profile import (
    StandardReinforcementProfile,
)
from koswat.configuration.settings.koswat_scenario import KoswatScenario
from koswat.dike.characteristic_points.characteristic_points_builder import (
    CharacteristicPointsBuilder,
)
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike.layers.layers_wrapper.koswat_layers_wrapper_builder import (
    KoswatLayersWrapperBuilder,
)
from koswat.dike.layers.layers_wrapper.koswat_layers_wrapper_builder_protocol import (
    KoswatLayersWrapperBuilderProtocol,
)
from koswat.dike.layers.layers_wrapper.koswat_layers_wrapper_protocol import (
    KoswatLayersWrapperProtocol,
)
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike.profile.koswat_profile_builder import KoswatProfileBuilder
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

    def _get_reinforced_profile(self) -> ReinforcementProfileProtocol:
        _reinforcement = self.reinforcement_profile_type()
        # Input profile data.
        _reinforcement.input_data = self.expectation.input_profile_base
        # Char points
        _char_points_builder = CharacteristicPointsBuilder()
        _char_points_builder.input_profile = _reinforcement.input_data
        _char_points_builder.p4_x_coordinate = self.expectation.p4_x_coordinate
        _reinforcement.characteristic_points = _char_points_builder.build()

        # layers
        def _get_layers(
            builder: KoswatLayersWrapperBuilderProtocol,
            layers_data: dict,
            char_points,
        ) -> KoswatLayersWrapperProtocol:
            builder.layers_data = layers_data
            builder.profile_points = char_points
            return builder.build()

        _layers_wrapper_builder: KoswatLayersWrapperBuilderProtocol = None
        if isinstance(_reinforcement, StandardReinforcementProfile):
            _layers_wrapper_builder = StandardReinforcementLayersWrapperBuilder()
        elif isinstance(_reinforcement, OutsideSlopeReinforcementProfile):
            _layers_wrapper_builder = OutsideSlopeReinforcementLayersWrapperBuilder()

        _initial_layers_wrapper = _get_layers(
            KoswatLayersWrapperBuilder(),
            self.expectation.koswat_layers_case.layers_dict,
            _reinforcement.characteristic_points.points,
        )
        _reinforcement.layers_wrapper = _get_layers(
            _layers_wrapper_builder,
            _initial_layers_wrapper.as_data_dict(),
            _reinforcement.characteristic_points.points,
        )

        return _reinforcement

    def to_reinforcement_profile_case(self) -> ReinforcementProfileCase:
        return ReinforcementProfileCase(
            case_name=self.case_name,
            koswat_input_profile_base_case=KoswatProfileBuilder.with_data(
                dict(
                    input_profile_data=self.input_profile_case,
                    layers_data=self.koswat_layers_case.layers_dict,
                    p4_x_coordinate=self.p4_x_coordinate,
                )
            ).build(),
            koswat_scenario_case=self.koswat_scenario_case,
            expected_reinforcement_profile=self._get_reinforced_profile(),
        )


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
                length_piping_wall=4.5,
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
                length_stability_wall=17,
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
                length_coffer_dam=17,
            ),
            koswat_layers_case=LayersCases.without_layers,
            p4_x_coordinate=0,
        ),
    ),
]
