from typing import List, Protocol

import pytest


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

    cases = [pytest.param(default, id="Default Scenario")]


class LayersCases(CasesProtocol):
    without_layers = dict(
        base_layer=dict(material="zand"),
        coating_layers=[],
    )
    with_clay = dict(
        base_layer=dict(material="zand"),
        coating_layers=[
            dict(material="klei", depth=4.2),
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

    cases = [pytest.param(default, id="Default Input Profile")]
