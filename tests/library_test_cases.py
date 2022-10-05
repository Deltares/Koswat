from typing import Dict, List, Protocol, Tuple

import pytest
from shapely.geometry.point import Point

from koswat.profiles.koswat_profile import KoswatProfileBase
from koswat.profiles.koswat_profile_builder import KoswatProfileBuilder


class CasesProtocol(Protocol):
    cases: List[pytest.param]


class ScenarioCases(CasesProtocol):
    default = dict(
        d_h=1,
        d_s=10,
        d_p=30,
        kruin_breedte=5,
        buiten_talud=3,
    )
    scenario_2 = dict(
        d_h=0.5,
        d_s=20,
        d_p=80,
        kruin_breedte=5,
        buiten_talud=4,
    )

    cases = [
        pytest.param(default, id="Default Scenario"),
        pytest.param(scenario_2, id="Scenario 2"),
    ]


class LayersCases(CasesProtocol):
    without_layers = dict(
        base_layer=dict(material="zand"),
        coating_layers=[],
    )
    with_clay = dict(
        base_layer=dict(material="zand"),
        coating_layers=[
            dict(material="klei", depth=0.75),
        ],
    )

    cases = [
        pytest.param(without_layers, id="Without layers"),
        pytest.param(with_clay, id="With clay layer"),
    ]


class InputProfileCases(CasesProtocol):
    default = dict(
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

    profile_case_2 = dict(
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
    default_default_no_layers = dict(
        input_profile_data=dict(
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
    default_scenario_2_no_layers = dict(
        input_profile_data=dict(
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
