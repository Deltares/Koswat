from typing import List, Protocol, Type

import pytest
from shapely.geometry.point import Point

from koswat.calculations.outside_slope_reinforcement import CofferDamInputProfile
from koswat.calculations.standard_reinforcement import (
    PipingWallInputProfile,
    SoilInputProfile,
    StabilityWallInputProfile,
)
from koswat.configuration.settings.koswat_scenario import KoswatScenario
from koswat.dike.material.koswat_material_type import KoswatMaterialType
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from tests.acceptance_scenarios.acceptance_test_scenario_dataclasses import (
    LayersTestCase,
)


class CasesProtocol(Protocol):
    cases: List[pytest.param]


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


class LayersCases(CasesProtocol):
    without_layers = LayersTestCase(
        case_name="without_layers",
        layers_dict=dict(
            base_layer=dict(material=KoswatMaterialType.SAND),
            coating_layers=[],
        ),
    )
    with_clay = LayersTestCase(
        case_name="with_clay",
        layers_dict=dict(
            base_layer=dict(material=KoswatMaterialType.SAND),
            coating_layers=[
                dict(material=KoswatMaterialType.CLAY, depth=0.75),
            ],
        ),
    )
    with_clay_and_grass = LayersTestCase(
        case_name="with_clay_and_grass",
        layers_dict=dict(
            base_layer=dict(material=KoswatMaterialType.SAND),
            coating_layers=[
                dict(material=KoswatMaterialType.GRASS, depth=0.5),
                dict(material=KoswatMaterialType.CLAY, depth=0.75),
            ],
        ),
    )
    with_acceptance_criteria = LayersTestCase(
        case_name="with_default_layers",
        layers_dict=dict(
            base_layer=dict(material=KoswatMaterialType.SAND),
            coating_layers=[
                dict(material=KoswatMaterialType.GRASS, depth=0.3),
                dict(material=KoswatMaterialType.CLAY, depth=0.5),
            ],
        ),
    )

    # Only cases that should be 'realistic'.
    cases = [
        pytest.param(with_clay_and_grass.layers_dict, id="With grass and clay layer"),
        pytest.param(
            with_acceptance_criteria.layers_dict, id="With acceptance criteria"
        ),
    ]


class InputProfileCases(CasesProtocol):
    default = KoswatInputProfileBase(
        dike_section="test_data",
        buiten_maaiveld=0,
        buiten_talud=3,
        buiten_berm_hoogte=0,
        buiten_berm_breedte=0,
        kruin_hoogte=6,
        kruin_breedte=5,
        binnen_talud=3,
        binnen_berm_hoogte=0,
        binnen_berm_breedte=0,
        binnen_maaiveld=0,
    )

    profile_case_2 = KoswatInputProfileBase(
        dike_section="test_data",
        buiten_maaiveld=0,
        buiten_talud=4,
        buiten_berm_hoogte=0,
        buiten_berm_breedte=0,
        kruin_hoogte=6.5,
        kruin_breedte=5,
        binnen_talud=5.54,
        binnen_berm_hoogte=2.6,
        binnen_berm_breedte=54,
        binnen_maaiveld=0,
    )

    cases = [pytest.param(default, id="Default Input Profile")]


class InitialPointsLookup(CasesProtocol):
    default = [
        Point(-18.0, 0.0),
        Point(-18.0, 0.0),
        Point(-18.0, 0.0),
        Point(0.0, 6.0),
        Point(5.0, 6.0),
        Point(23.0, 0.0),
        Point(23.0, 0.0),
        Point(23.0, 0.0),
    ]
    calc_profile_scenario_2 = [
        Point(-24, 0),
        Point(-24, 0),
        Point(-24, 0),
        Point(2, 6.5),
        Point(7, 6.5),
        Point(28.60, 2.6),
        Point(82.60, 2.6),
        Point(97, 0),
    ]
    cases = [
        pytest.param(default, id="Default initial profile."),
        pytest.param(calc_profile_scenario_2, id="Scenario 2 calculated profile."),
    ]


class InputProfileScenarioLookup:
    reinforcement_soil_default_default_no_layers = dict(
        input_profile_data=SoilInputProfile(
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
        layers_data=LayersCases.without_layers,
        p4_x_coordinate=3,
    )
    reinforcement_soil_default_scenario_2_no_layers = dict(
        input_profile_data=SoilInputProfile(
            dike_section="test_data",
            buiten_maaiveld=0,
            buiten_talud=4,
            buiten_berm_breedte=0,
            buiten_berm_hoogte=0,
            kruin_hoogte=6.5,
            kruin_breedte=5,
            binnen_talud=5.54,
            binnen_berm_hoogte=2.6,
            binnen_berm_breedte=54,
            binnen_maaiveld=0,
        ),
        layers_data=LayersCases.without_layers,
        p4_x_coordinate=2,
    )
    reinforcement_piping_wall_default_scenario_3_no_layers = dict(
        input_profile_data=PipingWallInputProfile(
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
        layers_data=LayersCases.without_layers,
        p4_x_coordinate=6,
    )
    reinforcement_stability_wall_default_scenario_3_no_layers = dict(
        input_profile_data=StabilityWallInputProfile(
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
        layers_data=LayersCases.without_layers,
        p4_x_coordinate=6,
    )
    reinforcement_coffer_dam_wall_default_scenario_3_no_layers = dict(
        input_profile_data=CofferDamInputProfile(
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
        layers_data=LayersCases.without_layers,
        p4_x_coordinate=0,
    )
